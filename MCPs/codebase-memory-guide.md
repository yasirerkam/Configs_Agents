
# Codebase Memory MCP — Proje Yönetimi Rehberi

> Kaynak: [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)
> Kapsam: Proje listeleme, proje silme, indeks sıfırlama

---

## 1. Nedir?

**Codebase Memory MCP**, bir kod tabanını tree-sitter ile ayrıştırıp SQLite destekli bir **knowledge graph** (bilgi grafiği) olarak saklayan, yerel çalışan bir MCP sunucusudur. İndeksler `~/.cache/codebase-memory-mcp/` altında `.db` dosyaları olarak tutulur.

İki şekilde kullanılır:

| Yöntem | Açıklama |
|--------|----------|
| **MCP aracı** | Claude Code / OpenCode gibi bir asistanda `delete_project` vb. araçlar |
| **CLI modu** | Terminalden `codebase-memory-mcp cli <tool> ...` komutları |

Bu rehber her iki yöntemi de kapsar.

---

## 2. Ön Koşullar

- `codebase-memory-mcp` binary'si PATH'te olmalı.
- Kurulum kanalları: npm, PyPI, Homebrew, Scoop, Winget, Chocolatey, `go install`.

```powershell
# Sürüm ve yardım kontrolü
codebase-memory-mcp --version
codebase-memory-mcp --help
```

---

## 3. İndeksli Projeleri Listeleme

Hangi projelerin indeksli olduğunu görmek (node/edge sayılarıyla):

```powershell
# CLI
codebase-memory-mcp cli list_projects
```

Örnek çıktı:

```json
[
  { "name": "D:/Projects/Google Play Console", "nodes": 1234, "edges": 5678 }
]
```

> **Not:** CLI, çıktıyı makine-okunur (bitişik/tek satır) olarak basar — bu normaldir. Okunaklı görüntülemek için PowerShell'de (kurulum gerekmez):
>
> ```powershell
> codebase-memory-mcp cli list_projects | ConvertFrom-Json | ConvertTo-Json -Depth 10
> ```
>
> jq kuruluysa alternatif: `codebase-memory-mcp cli list_projects | jq`

> Silme işleminde kullanılacak proje adı, `list_projects` çıktısındaki **`name` alanıdır** — tahmin yürütme, listeyi kontrol et.

Asistan üzerinden (MCP):

```
list_projects  →  indeksli projelerin listesi döner
```

---

## 4. Proje Silme

Bir projeyi **indeksten** tamamen kaldırır (grafik verisi + `.db` dosyası). Kaynak koda dokunmaz.

### 4.1 CLI (önerilen)

```powershell
# Bayrak stili
codebase-memory-mcp cli delete_project --project "PROJE_ADI"

# JSON stili (PowerShell'de tek tırnak önemli)
codebase-memory-mcp cli delete_project '{"project": "PROJE_ADI"}'
```

Örnek:

```powershell
codebase-memory-mcp cli delete_project --project "D:/Projects/Google Play Console"
```

### 4.2 MCP aracı (asistan üzerinden)

```
delete_project(project: "PROJE_ADI")
```

### 4.3 Doğrulama

```powershell
codebase-memory-mcp cli list_projects
```

Silinen proje listede görünmemelidir.

---

## 5. Tüm İndeksi Sıfırlama (nükleer seçenek)

Tüm indeksleri toptan silmek istersen (ör. bozuk/şişmiş indeks):

```powershell
# PowerShell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cache\codebase-memory-mcp"

# Bash / WSL
rm -rf ~/.cache/codebase-memory-mcp/
```

> Uyarı: Bu komut **tüm projelerin** indeksini siler. Sonrasında her repo için `index_repository` çağrısı gerekir.

---

## 6. Silme Sonrası Yeniden İndeksleme

Yanlışlıkla sildiysen ya da yeni baştan indekslemek istiyorsan:

```powershell
# CLI
codebase-memory-mcp cli index_repository --repo-path "C:/path/to/repo"

# JSON stili
codebase-memory-mcp cli index_repository '{"repo_path": "C:/path/to/repo"}'
```

Asistan üzerinden:

```
index_repository(repo_path: "C:/path/to/repo")
```

---

## 7. Uninstall (paketi tamamen kaldırma)

Ajan konfigürasyonlarını, skill'leri, hook'ları ve binary'yi kaldırır (indeksleri onayınla siler):

```powershell
codebase-memory-mcp uninstall
```

> Kurulum scripti dosyası silinmez; uninstall yolu ve `rm` komutunu yazdırır (sahipliği kanıtlanamadığı için bilinçli olarak).

---

## 8. Hızlı Başvuru Tablosu

| İşlem | CLI Komutu | MCP Aracı |
|-------|-----------|-----------|
| Projeleri listele | `cli list_projects` | `list_projects` |
| Proje sil | `cli delete_project --project ADI` | `delete_project` |
| İndeks durumu | `cli index_status --project ADI` | `index_status` |
| İndeksle | `cli index_repository --repo-path YOL` | `index_repository` |
| Tümünü sıfırla | `Remove-Item ...\.cache\codebase-memory-mcp` | — |
| Paketi kaldır | `codebase-memory-mcp uninstall` | — |

---

## 9. Gotcha'lar

1. **Proje adı birebir olmalı** — `list_projects` çıktısındaki `name` değerini kullan; yaklaşık eşleşme yok, olmayan proje "project not found" döner.
2. **CLI komutları daemon başlatmaz** — tek seferlik çalışır, arka planda süreç bırakmaz.
3. **Silme kalıcıdır** — grafik verisi geri döndürülemez; gerekirse `index_repository` ile yeniden indekslenir.
4. **İndeksler diskte kalır** — silme yalnızca indeksi kaldırır; reponun kendisine dokunulmaz.
5. **Windows / PowerShell** — JSON stili kullanırken argümanı **tek tırnak** ile sar (çift tırnak PowerShell'de ayrıştırma sorunları çıkarabilir).

