# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///

import requests
import json
import sys
import os
import time

# Aratmak istediğiniz hedef modeller
TARGET_MODELS = [
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "kimi-k2.6",
    "kimi-k2.7-code",
    "qwen3.7-max",
    "qwen3.7-pro",
    "glm-5.2",
    "glm-5.1",
    "mimo-v2.5-pro",
    "mimo-v2.5",
    "minimax-m3",
]
API_URL = "https://g4f.space/v1/models"

# Dosya isimleri ve önbellek süresi (saniye cinsinden)
FILTERED_OUTPUT_FILE_NAME = "opencode_models.json"
RAW_OUTPUT_FILE_NAME = "raw_models.json"
CACHE_DURATION_SEC = 300  # 5 dakika


def generate_config():
    try:
        # Scriptin bulunduğu klasörü tespit et
        script_dir = os.path.dirname(os.path.abspath(__file__))
        raw_output_path = os.path.join(script_dir, RAW_OUTPUT_FILE_NAME)
        filtered_output_path = os.path.join(script_dir, FILTERED_OUTPUT_FILE_NAME)

        raw_data = None
        use_cache = False

        # Önbellek geçerlilik kontrolü
        if os.path.exists(raw_output_path):
            file_mod_time = os.path.getmtime(raw_output_path)
            current_time = time.time()

            # Eğer aradaki fark 5 dakikadan az ise önbelleği kullan
            if current_time - file_mod_time < CACHE_DURATION_SEC:
                use_cache = True

        if use_cache:
            print(
                "Yerel önbellek geçerli. Veriler 'raw_models.json' dosyasından okunuyor...",
                file=sys.stderr,
            )
            with open(raw_output_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        else:
            print(
                "Önbellek süresi doldu veya dosya yok. Güncel veriler internetten çekiliyor...",
                file=sys.stderr,
            )
            # Ağ kilitlenmelerine karşı 10 saniyelik timeout (fail-fast)
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()

            raw_data = response.json()

            # Yenilenen ham veriyi hemen diske yaz
            with open(raw_output_path, "w", encoding="utf-8") as f:
                json.dump(raw_data, f, indent=2, ensure_ascii=False)
            print(f"[Başarılı] Yeni ham API yanıtı diske kaydedildi.", file=sys.stderr)

        data = raw_data.get("data", [])

        # Filtreleme mantığı
        models_config = {}
        for item in data:
            model_id = item.get("id", "")
            model_name = item.get("model", "")
            label = item.get("label", "")

            if any(
                target in model_id or target in model_name for target in TARGET_MODELS
            ):
                models_config[model_id] = {"name": label if label else model_id}

        final_output = {"models": models_config}
        filtered_json_bytes = json.dumps(final_output, indent=2, ensure_ascii=False)

        # Standart çıktı olarak saf JSON'ı terminale bas
        print(filtered_json_bytes)

        # Filtrelenmiş veriyi opencode_models.json olarak kaydet/güncelle
        with open(filtered_output_path, "w", encoding="utf-8") as f:
            f.write(filtered_json_bytes)

        print(
            f"[Başarılı] Filtrelenmiş model dosyası güncellendi: {filtered_output_path}",
            file=sys.stderr,
        )

    except Exception as e:
        print(f"Hata oluştu: {e}", file=sys.stderr)


if __name__ == "__main__":
    generate_config()
