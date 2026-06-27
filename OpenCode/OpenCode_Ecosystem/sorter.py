import re
import os
import time
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# Optional GitHub Personal Access Token. Set GITHUB_TOKEN in .env or environment to avoid rate limits.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

RAW_URL = (
    "https://raw.githubusercontent.com/awesome-opencode/awesome-opencode/main/README.md"
)

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "raw", "README.md")
OUTPUT_FILE = os.path.join(DATA_DIR, "processed", "README_SORTED.md")
STARS_CACHE_FILE = os.path.join(DATA_DIR, "raw", "stars_cache.json")

CACHE_TTL_SECONDS = 6 * 60 * 60
STARS_CACHE_TTL_SECONDS = 24 * 60 * 60

# Hem markdown linklerini ([ad](https://github.com/...)) hem de HTML linklerini (href="https://github.com/...") yakalar
GITHUB_URL_PATTERN = r'(?:\]\(|href=")(https://github\.com/[^/"\s)]+/[^/"\s)]+)'
REPO_FROM_URL = re.compile(r"github\.com/([^/\s)]+)/([^\s)\"]+)")

# <details> açılış ve kapanışlarını yakala (iç içe bloklar için)
DETAILS_OPEN_RE = re.compile(r"<details\b[^>]*>", re.IGNORECASE)
DETAILS_CLOSE_RE = re.compile(r"</details\s*>", re.IGNORECASE)


def fetch_remote_readme():
    print(f"   [*] Downloading raw README: {RAW_URL}")
    resp = requests.get(RAW_URL, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"README could not be downloaded (HTTP {resp.status_code}). Check your internet connection."
        )
    return resp.text


def load_cached_readme():
    """data/raw/README.md 6 saatten eskiyse yeniden indir, değilse yerel dosyayı oku."""
    os.makedirs(os.path.dirname(RAW_FILE), exist_ok=True)

    if os.path.exists(RAW_FILE):
        age = time.time() - os.path.getmtime(RAW_FILE)
        if age < CACHE_TTL_SECONDS:
            remaining_min = (CACHE_TTL_SECONDS - age) / 60
            print(
                f"   [*] Local cache valid (age={age/3600:.1f}h, remaining~{remaining_min:.0f}m). Skipping download."
            )
            with open(RAW_FILE, "r", encoding="utf-8") as f:
                return f.read()

    try:
        content = fetch_remote_readme()
    except Exception as e:
        if os.path.exists(RAW_FILE):
            print(f"   [!] Download failed ({e}). Using existing cache.")
            with open(RAW_FILE, "r", encoding="utf-8") as f:
                return f.read()
        raise

    with open(RAW_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"   [*] Raw file saved: {RAW_FILE}")
    return content


def load_stars_cache():
    """Yıldız cache'ini yükler. {owner/repo: (stars, timestamp)}"""
    if not os.path.exists(STARS_CACHE_FILE):
        return {}
    try:
        with open(STARS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Eski format elemesini atla
        now = time.time()
        valid = {
            k: (v, ts)
            for k, (v, ts) in data.items()
            if now - ts < STARS_CACHE_TTL_SECONDS
        }
        return valid
    except Exception:
        return {}


def save_stars_cache(cache):
    """Yıldız cache'ini diske yazar."""
    os.makedirs(os.path.dirname(STARS_CACHE_FILE), exist_ok=True)
    tmp = STARS_CACHE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f)
    os.replace(tmp, STARS_CACHE_FILE)


def get_repo_stars(repo_url, stars_cache, stop_on_rate_limit=True):
    """Verilen GitHub URL'sinin yıldız sayısını çeker (cache destekli)."""
    match = REPO_FROM_URL.search(repo_url)
    if not match:
        return -1

    owner, repo = match.groups()
    repo = repo.replace(".git", "").strip()
    key = f"{owner}/{repo}"

    # Cache kontrolü
    if key in stars_cache:
        cached_stars, cached_ts = stars_cache[key]
        return cached_stars

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            stars = response.json().get("stargazers_count", 0)
            stars_cache[key] = (stars, time.time())
            return stars
        elif response.status_code in (403, 429):
            if stop_on_rate_limit:
                print(
                    f"   [!] API rate limit hit! Stopping further fetches. "
                    f"Set GITHUB_TOKEN env var to avoid this. "
                    f"Using cache + -1 for unsorted items."
                )
                raise RateLimitError()
            retry_after = response.headers.get("Retry-After", "60")
            try:
                wait_sec = int(retry_after)
            except ValueError:
                wait_sec = 60
            time.sleep(min(wait_sec, 5))
    except RateLimitError:
        raise
    except Exception as e:
        print(f"   [!] Network error fetching {repo}: {e}")

    return -1


class RateLimitError(Exception):
    pass


def extract_repo_url(text):
    """Bir metin parçasından ilk geçerli GitHub repo URL'sini çıkarır."""
    for m in re.finditer(GITHUB_URL_PATTERN, text):
        if REPO_FROM_URL.search(m.group(1)):
            return m.group(1)
    return None


def parse_into_units(text):
    """
    Metni sıralanabilir birimler + sabit metin olarak ayırır.
    İç içe <details> bloklarını doğru handle eder (depth tracking).

    Birim türleri:
      - ('container', dış <details> bloğunun kendisi - sıralanmaz)
      - ('details', iç <details> bloğu - sıralanır)
      - ('row', tablo veya liste satırı - sıralanır)
    Aradaki her şey ('text', ...) olarak eklenir.

    Döner: [('text', '...'), ('container', '...'), ('text', '...'), ('details', '...'), ...]
    """
    units = []
    cursor = 0
    depth = 0
    block_start = None

    i = 0
    while i < len(text):
        # En yakın <details> açılışı
        open_m = DETAILS_OPEN_RE.search(text, i)
        close_m = DETAILS_CLOSE_RE.search(text, i)

        if not open_m and not close_m:
            break

        if open_m and (not close_m or open_m.start() <= close_m.start()):
            if depth == 0:
                if cursor < open_m.start():
                    units.extend(_split_chunk_to_rows(text[cursor : open_m.start()]))
                block_start = open_m.start()
            depth += 1
            i = open_m.end()
        else:
            depth -= 1
            i = close_m.end()
            if depth == 0 and block_start is not None:
                # Dış blok: sadece ilk satırı ("<details open>") ve kapanışı al,
                # içindekileri ayrı birimler olarak döndür
                container_full = text[block_start:i]
                # İlk satır: <details ...>
                first_newline = container_full.find("\n")
                header = (
                    container_full[: first_newline + 1]
                    if first_newline >= 0
                    else container_full
                )
                # İçerik: ilk satırdan son </details>'tan önce
                inner = container_full[len(header) :]
                # Sondaki </details>\n kısmını at
                last_close = inner.rfind("</details>")
                if last_close >= 0:
                    # Son </details>'tan önceki kısmı al (kapanış newline'ı dahil etme)
                    # newline dahil et
                    end_of_last_close = last_close + len("</details>")
                    # Sondaki newline'ları at
                    inner_content = inner[:end_of_last_close]
                    trailing = inner[end_of_last_close:]
                else:
                    inner_content = inner
                    trailing = ""

                units.append(("container_open", header))
                # İçeriği parse et (iç içe blokları ayrı birimler olarak)
                units.extend(parse_inner_content(inner_content))
                units.append(("container_close", "</details>\n"))

                cursor = i
                block_start = None

    if cursor < len(text):
        units.extend(_split_chunk_to_rows(text[cursor:]))

    return units


def parse_inner_content(inner):
    """
    Bir dış <details> bloğunun içeriğini parse eder.
    İçindeki <details> bloklarını ('details') ve aralardaki metni ('text') ayırır.
    """
    units = []
    cursor = 0
    depth = 0
    block_start = None

    i = 0
    while i < len(inner):
        open_m = DETAILS_OPEN_RE.search(inner, i)
        close_m = DETAILS_CLOSE_RE.search(inner, i)

        if not open_m and not close_m:
            break

        if open_m and (not close_m or open_m.start() <= close_m.start()):
            if depth == 0:
                if cursor < open_m.start():
                    units.extend(_split_chunk_to_rows(inner[cursor : open_m.start()]))
                block_start = open_m.start()
            depth += 1
            i = open_m.end()
        else:
            depth -= 1
            i = close_m.end()
            if depth == 0 and block_start is not None:
                units.append(("details", inner[block_start:i]))
                cursor = i
                block_start = None

    if cursor < len(inner):
        units.extend(_split_chunk_to_rows(inner[cursor:]))

    return units


def _split_chunk_to_rows(chunk):
    """
    Bir metin parçasını satırlara böler.
      - Ardışık sortable satırları (tablo/liste) tek bir ('row_group', joined_text) olarak birleştirir.
      - Boş satırları atlar.
      - Diğer satırları ('text', line) olarak döner.
    """
    out = []
    sortable_buffer = []

    def flush_sortable():
        if sortable_buffer:
            out.append(("row_group", "\n".join(sortable_buffer)))
            sortable_buffer.clear()

    for line in chunk.splitlines():
        if not line.strip():
            # Boş satır: sortable buffer'ı bitir, ama text olarak ekleme
            flush_sortable()
            continue
        if _is_sortable_row(line):
            sortable_buffer.append(line)
        else:
            flush_sortable()
            out.append(("text", line))
    flush_sortable()
    return out


def _is_sortable_row(line):
    """Markdown tablo satırı veya liste satırı + GitHub linki içeriyor mu?"""
    # Tablo başlık/ayraç satırlarını atla
    if "|---" in line or re.match(r"^\s*\|?\s*:?-+:?\s*\|", line):
        return False
    is_table = bool(re.match(r"^\s*\|.*\|", line))
    is_list = bool(re.match(r"^\s*[-*]\s+\[", line))
    if not (is_table or is_list):
        return False
    return bool(re.search(GITHUB_URL_PATTERN, line))


def sort_row_group_content(content, stars_cache):
    """
    row_group içindeki satırları kendi aralarında yıldız sayısına göre sıralar.
    Başlık ve ayraç satırları (_is_sortable_row False döndüren) orijinal sırasını korur.
    """
    lines = content.split("\n")
    scored_lines = []
    header_lines = []

    for line in lines:
        if not _is_sortable_row(line):
            header_lines.append(line)
            continue
        url = extract_repo_url(line)
        if url:
            try:
                stars = get_repo_stars(url, stars_cache)
            except RateLimitError:
                stars = -1
            scored_lines.append((line, stars))
        else:
            scored_lines.append((line, -1))

    # Yıldız sayısına göre azalan sırada sırala
    scored_lines.sort(key=lambda x: x[1], reverse=True)
    sorted_rows = [line for line, _ in scored_lines]

    # Başlık satırları üstte, sıralanmış veri satırları altta
    return "\n".join(header_lines + sorted_rows)


def sort_units(units):
    """
    Birimleri işler. Sıralama mantığı:
      - Sabit birimler ('text', 'container_open', 'container_close') geçilir.
      - Sortable birimler ('details', 'row_group') birikir; araya sabit birim girene kadar
        yıldız sayısına göre azalan sırada sıralanır.
      - 'row_group' içindeki tüm satırlar tek bir birim olarak sıralanır ve orijinal
        satır yapısı korunur.
    """
    result = []
    pending = []  # [(content, stars)]
    stars_cache = load_stars_cache()

    def flush():
        if not pending:
            return
        pending.sort(key=lambda x: x[1], reverse=True)
        for content, _ in pending:
            result.append(content)
        pending.clear()

    for kind, content in units:
        if kind == "details":
            url = extract_repo_url(content)
            if url:
                try:
                    stars = get_repo_stars(url, stars_cache)
                except RateLimitError:
                    repo_name = url.split("github.com/")[-1]
                    print(f"   -> skipped (rate limit): {repo_name}")
                    pending.append((content, -1))
                    continue
                print(f"   -> {stars:5} stars | {url.split('github.com/')[-1]}")
                pending.append((content, stars))
                continue
        elif kind == "row_group":
            # Tablo satırlarını kendi aralarında sırala
            sorted_content = sort_row_group_content(content, stars_cache)
            # Sıralanmış grubun ilk satırının yıldız sayısını temsili olarak kullan
            url = extract_repo_url(sorted_content)
            if url:
                try:
                    stars = get_repo_stars(url, stars_cache)
                except RateLimitError:
                    stars = -1
                print(f"   -> {stars:5} stars | {url.split('github.com/')[-1]} (table)")
                pending.append((sorted_content, stars))
                continue
        # Sabit birim
        flush()
        result.append(content)

    flush()
    save_stars_cache(stars_cache)
    return result


def main():
    print("1. Loading raw README (with 6h cache)...")
    text = load_cached_readme()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    if not GITHUB_TOKEN:
        cache = load_stars_cache()
        if not cache:
            print(
                "   [!] No GITHUB_TOKEN set and no star cache found. "
                "Anonymous GitHub API allows only 60 requests/hour, "
                "which is not enough for ~200 repos. Sorting will be incomplete. "
                "Set GITHUB_TOKEN env var for best results.\n"
            )

    print("2. Parsing units and fetching stars...\n")
    units = parse_into_units(text)
    sorted_units = sort_units(units)

    # Birimleri birleştir: ardışık sortable birimler arasına çift newline
    # (markdown okunabilirliği için), row_group içinde satırları koru
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        parts = []
        for content in sorted_units:
            if (
                "\n" in content
                and not content.startswith("<")
                and not content.startswith("|")
            ):
                # Multi-line içerik (row_group gibi) - olduğu gibi ekle
                parts.append(content)
            else:
                parts.append(content)
        f.write("\n\n".join(parts) + "\n")

    print(f"\nDone! Sorted file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
