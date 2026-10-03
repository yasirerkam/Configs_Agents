# Oh-My-Pi (OMP) Detaylı Kullanım Kılavuzu

## 1\. Temel Mimari ve Güvenli Düzenleme

Oh-My-Pi (OMP), terminal-yerel bir yapay zeka kodlama ajanı harness'ıdır.

- **Süreç İçi (In-Process) Araçlar:** `ripgrep`, AST ayrıştırıcılar ve 46 yerel coreutil aracı (sed, jq, xargs vb.) fork/exec yapmadan doğrudan OMP süreci içinde çalışır.  
- **Hashline Güvenli Düzenleme:** Satır içerik hash imzaları (`hashline`) ile dosya düzenlenir. Dosya güncel değilse veya hash uyuşmazlığı varsa yama otomatik reddedilir.  
- **Çift Çekirdekli Yürütme (Eval Bridge):** Sürekli çalışan Python ve Bun çalışma alanları üzerinden model kendi araçlarını hücreler içinden çağırabilir.

---

## 2\. Oturum ve Çalışma Modları (Session Controls)

### A. Vibe Modu (`/vibe`)

- **Yönetici/Direktör Konumu:** Ana ajan doğrudan kod yazmaz; salt okunur araçlarla çalışarak tüm kodlama işlerini paralel alt ajanlara (`task` subagents) devreder.  
- **İzole Çalışma Ağaçları:** Alt ajanlar bağımsız Git worktree'lerinde çalışır; merge çakışmaları ve çakışan düzenlemeler önlenir.  
- **Agent Hub (`Alt+A`):** Çalışan ve bekleyen tüm alt ajanların canlı kayıtları izlenebilir, durdurulabilir veya yönlendirilebilir.

### B. Planlama Modu (`/plan` veya `Alt+Shift+P`)

- Kod üzerinde değişiklik yapmadan önce mimari analiz çıkarır.  
- Yazma araçları kilitlenir; plan onaylandığında uygulama aşamasına geçilir.

### C. Danışman Modeli (`/advisor`)

- **Dual-Model İnceleme:** Ana geliştirici ajan çalışırken, ikinci bir model (`advisor`) her adımı bağımsız bağlamda denetler.  
- Hata veya sapma algılandığında satır içi uyarı veya engelleyici blok notu düşer.  
- `/advisor status`, `/advisor on`, `/advisor off` ile yönetilir. Tam alt komut seti (dump/configure dahil): Bölüm 9-G.

---

### 3\. Kod İnceleme ve Canlı Eşli Çalışma

#### A. `/green`, `/review` ve `/annotate`

- **`/review`:** Kod değişikliklerini denetleyen özel alt ajanlar başlatır. Sorunları P0 (kritik) ile P3 (küçük öneri) arasında sınıflandırır. Hedef: yerel diff (base branch'e göre) veya GitHub PR (`pr://owner/repo/N`). Diff bir kez çözülüp `ResolvedReviewTarget` olarak dondurulur; overlay ve reviewer prompt'u aynı snapshot'ı okur. **GitHub'a hiçbir şey postalanmaz.**
- **`/annotate`:** İnceleme başlamadan önce diff veya yanıtlar üzerine satır bazında not iliştirmeyi sağlar (`/annotate code-review`, `/annotate last`). Kaynaklar: `code-review [focus]` (yerel diff veya PR), `last` (son asistan yanıtı), `session` (`/copy` seçicisinden mesaj), dosya yolu, tırnak içinde literal metin. Notlar **composer'a yapıştırılır**, otomatik gönderilmez. Overlay'de "Continue with LLM review" seçilirse notlar `/review`'e odak (focus) olarak gider; etkileşimsiz ortamda `code-review` doğrudan `/review`'e delege olur.
- **`/green` (ci-green):** "Generate a prompt to iterate on CI failures until the branch is green." Agent'a GitHub Actions hatalı run'larını izleyen, hataları düzelten ve **branch yeşile gelene kadar** tekrarlayan bir döngü prompt'u üretir (`run_watch` izlemesi üzerinden).
- Üçü de yerleşik kayıtta değil, **bundled custom command** olarak kayıtlıdır (`src/extensibility/custom-commands/bundled/{ci-green,review,annotate}/`) — bkz. Bölüm 9-A.

#### B. Canlı Oturum Paylaşımı (`/collab`)

- Oturumu uçtan uca şifreli (E2EE) röleye aktarır. Link ve QR kod üretir.  
- Takım arkadaşları `omp join <link>` ile terminalden veya tarayıcıdan (`my.omp.sh`) bağlanabilir.  
- `/collab view` ile salt okunur izleme linki verilebilir.

---

## 4\. Özel İstek Sözcükleri (Prompt Controls)

İstek metninde bağımsız ve küçük harfle kullanıldığında **yalnızca o tura özel** davranış değişikliği tetikler:

- **`ultrathink`:** O tur için modelin desteklediği en yüksek düşünme seviyesini seçer ve özel çok adımlı akıl yürütme direktifi enjekte eder.  
- **`orchestrate`:** Görevi paralel alt ajanlara dağıtan ve her fazı doğrulayan orkestrasyon sözleşmesini devreye alır.  
- **`workflowz`:** Görev aracıyla deterministik çoklu alt ajan iş akışı zinciri kurar.

---

## 5\. Model Yönetimi ve 9 Niyet Bazlı Rol (Model Roles)

### A. Kalıcı Konfigürasyon (`~/.omp/agent/config.yml`)

modelRoles:

  default: anthropic/claude-3-5-sonnet  \# Normal turlar ve genel geliştirme

  smol: openai/gpt-4o-mini              \# Düşük maliyetli hızlı alt ajan dağıtımları

  slow: anthropic/claude-3-7-sonnet     \# Derin akıl yürütme ve karmaşık mimari

  plan: anthropic/claude-3-7-sonnet     \# /plan modunda mimari tasarım

  commit: openai/gpt-4o-mini            \# Commit mesajları ve değişiklik günlükleri

  vision: openai/gpt-4o                 \# Ekran görüntüsü ve UI/UX analizi

  task: anthropic/claude-3-5-haiku      \# Alt ajanlarda işçi kodlayıcı

  advisor: openai/o3-mini               \# Adım adım denetleyen gözlemci model

  tiny: meta/llama-3.2-1b-instruct      \# Başlık üretme ve mikro görevler

### B. Hızlı Kısayollar ve Komutlar

- **`Ctrl+P`:** Aktif rol için tanımlı modeller arasında anlık geçiş yapar.  
- **`/model` (`Alt+M`):** Kalıcı Model Hub arayüzünü açar.  
- **`/switch` (`Alt+P`):** Yalnızca aktif oturum için geçici model seçer.  
- **Başlatma Bayrakları:** `omp --smol <model> --slow <model> --plan <model>`

---

## 6\. Dahili Özel URL Protokolleri (Internal Schemes)

- **`pr://` ve `issue://`:** GitHub PR ve issue'larını dosya gibi okur (`read pr://1428`).  
- **`conflict://N` ve `conflict://*`:** Merge çakışmalarını `@theirs`, `@ours` veya `@base` yazarak tek satırda çözer.  
- **`agent://`:** Alt ajan çıktılarından JSON verisi ayıklar (`agent://<id>/findings.0.path`).  
- **`xd://`:** Harici ve nadir kullanılan geliştirici araçlarına erişim sağlar.

---

## 7\. Kalıcı Proje Hafızası (Memory Bank)

Oturumlar kapansa dahi projenin mimari kurallarını hatırlar:

- `retain`: Önemli kararları hafızaya yazar.  
- `recall` ve `reflect`: Bilgileri arar ve sentezler.  
- `learn`: Yeniden kullanılabilir bir tecrübeyi hafızaya alıp gerekirse yönetilen bir yeteneğe (`skill`) dönüştürür.  
- Desteklenen arka uçlar: `Mnemopi` (yerel SQLite), `local`, `Hindsight`.

---

## 8\. Sıfır Geçiş Maliyeti (Zero-Migration)

OMP, mevcut kural dosyalarını dönüştürme gerekmeksizin doğrudan okur:

- Cursor: `.cursorrules`, `.cursor/rules/*.mdc`  
- Cline: `.clinerules`  
- Codex: `AGENTS.md`  
- GitHub Copilot: `.github/copilot-instructions.md`, `applyTo`  
- Claude ve VS Code kural tanımları

---

## 9\. Slash Komutları — Tam Envanteri

Ekim 2026 itibarıyla doğrulanmış envanter. Kaynaklar: `docs/` referans dokümanları ve kurulu `omp` (v18.4.10) komut kaydı. Komutlar üç kaynaktan gelir: **yerleşik (built-in)** kayıtlar, **bundled custom commands** (`custom-commands/bundled/*`) ve **dosya komutları** (`commands/*.md` + `commands/` dizinleri).

### A. Kod İnceleme Üçlüsü (`/green`, `/review`, `/annotate`)

Genişletilmiş davranışsal anlatım **Bölüm 3-A**'da (şimdi üçüyle güncellendi). Tamamlama bilgisi: üçü de **bundled custom command** olarak kayıtlıdır (`custom-commands/bundled/{ci-green,review,annotate}/`) — yerleşik registry bloğunda bulunmazlar, bu yüzden envanter taramasında kolay atlanabilirler.

### B. Modlar (birbirini dışlayan)

- **`/plan [prompt]`** — Plan modu toggle: agent planlayıp onaya sunar. `/plan-review` ile son planın inceleme overlay'i yeniden açılır (yalnız plan modunda).
- **`/vibe`** — Director/worker orkestrasyonu (bkz. Bölüm 2A). `/vibe <prompt>` girip ilk directive'i aynı anda gönderir.
- **`/goal <objective>`** + alt komutlar:
  - `/goal set <objective>` — hedefi koy/değiştir
  - `/goal show` — mevcut hedef detayları
  - `/goal pause`, `/goal resume`, `/goal drop`
  - `/goal budget <N|off>` — token bütçesi
  - Şart: `goal.enabled`, plan modu kapalı; abort edilen goal pause olur, sadece `resume` devam ettirir. Restore edilen goal başlangıçta paused gelir.
- **`/guided-goal [kaba hedef]`** — Agent önce sohbet içinde seni mülakatla hedefi netleştirir (`guided-goal-interview` şablonu), sonra goal modunu kurar. CLI flag'i yoktur; `--goal` bunun değil `/goal`'un karşılığıdır.
- `/plan`, `/goal`, `/vibe` karşılıklı dışlanır; pause edilmiş goal bile vibe'ı engeller.

### C. Servis Hızı Katmanları

- **`/fast [on|ultra|off|status]`** — Hızlı servis: OpenAI'a `service_tier: priority` (kodex destekliyse `ultrafast`), direct Anthropic'e `speed: fast`, Google'a `priority`. `tier.*` ayarlarının UI karşılığı.
- **`/slow [on|off|status]`** — Yavaş/ucuz servis: OpenAI/Google'da **flex tier**; direct Anthropic'te 5 saatlik abonelik limitine ulaşıldığında **düşük öncelikli şeritten devam etme** izni (`providers.anthropic.slowMode` ayarı). `/slow auto` = "OpenAI/Google'da flex; Anthropic'te limit sonrası düşük öncelikli şerit". `modelRoles.slow` ile karıştırılmamalı — rol, derin muhakemede kullanılan ikinci modeldir; komut ise şerit seçimidir.

### D. Model Yönetimi

Kalıcı rol konfigürasyonu ve başlatma bayrakları: Bölüm 5-A / 5-B. Oturum içi komutlar:
- **`/model`** — Model seçim arayüzü (Roles görünümü dahil; `Ctrl+P` cycleOrder'da döner).
- **`/smodel`** — Sadece bu oturum için model değiştir (persist etmez).
- **`/modelpreset [list|save|switch|delete] [name]`** — Rol modelleri + thinking seviyesini preset olarak kaydet/uygula.
- **`/queue <message>`** — Agent yield ettikten sonrasına mesaj kuyruklar.
- **`/loop [count|duration] [--while|--until '<cmd>'] [prompt]`** — Koşullu/tekrarlı turn döngüsü.
- **`/prewalk` / `/prewalk restart`** — Tek atımlık handoff arm/disarm: aktif model → `@smol`; restart `@default`'a dönüp yeniden silahlandırır (AYRINTI: prewalk.md).

### E. Oturum İşlemleri

| Komut | Etki |
| --- | --- |
| `/new` | Boş yeni konuşma |
| `/fresh` | Provider tarafı kimliği tazele, dosya/kimliği koru |
| `/clear` | Canlı/model konuşma bağlamını temizle |
| `/delete` | Oturumu sil, yenisine geç |
| `/fork` | Aktif oturumdan kopya oluştur ve geç |
| `/resume [id\|@claude\|@codex]` | Oturuma dön veya dışarıdan içe aktar |
| `/restart` | Süreci yeniden başlat |
| `/export [--themes] [yol]` | Oturumu dışa aktar |
| `/share` | Şifreli paylaşım linki üret (share sunucusu veya authenticated `gh` ile secret gist; gist başarısızsa share sunucusuna düşer) |
| `/copy` | Konuşmadan metin/kod seçicisi aç; `/annotate session` ve "son linki aç" akışı bunu kaynaştırır |

### F. Yardımcı Yerleşikler

- **`/pause`** (sadece TUI) — Tüm agent'ları (main + subagent + advisor) global duraklat; akış güvenli sınırda biter, hiçbir şey iptal edilmez. Esc/Enter/Space/Ctrl+C ile devam.
- **`/btw <soru>`** — İzlenen oturum hakkında bağımsız yan soru: kendi transcript'ine karışmaz, kendi konuşma kimliğiyle koşar. Boş `/btw` geçmişini açar; `Esc` çalışanı iptal eder.

### G. Araç ve Özellik Toggle'ları

- **`/advisor [on|off|status|dump [raw]|configure]`** — Danışman alt sistemi: her turu pasif inceleyen ikinci model. `configure` etkileşimli `WATCHDOG.yml` editörü açar. Oturum kapsamlıdır, config'e yazmaz.
- **`/skills`** — Sistem prompt'unda skill listesi gösterme/gizleme (yalnız oturum).
- **`/skill:<name> [args]`** — Skill içeriğini custom message olarak enjekte eder (`skills.enableSkillCommands`).
- **`/extended-context`** — Genişletilmiş bağlam penceresi toggle.
- **`/computer` [on|off|status]** — Native computer-use eval prelude toggle.
- **`/memory [view|stats|diagnose|queue|sync|clear|enqueue|rebuild|mm …]`** — Hafıza arka ucu idamesi (mm sadece Hindsight; ACP'de yok).
- **`/mcp <alt>`** — MCP sunucu yönetimi; alt komutlar: `add` (interactive wizard), `add <name> [--scope project|user] [--url <url> --transport http|sse] [--token <token>] [-- <command...>]`, `list`, `remove <name>`, `test <name>`, `reauth <name>`, `unauth <name>`, `enable <name>`, `disable <name>`, `smithery-search <keyword> [--semantic]`, `smithery-login`, `smithery-logout`, `reconnect <name>`, `reload`, `resources`, `prompts`, `notifications`, `help`.
- **`/collab [start|view|list|stop|status] [relayUrl]`** — Canlı paylaşım: şifreli röle linki + QR; `view` salt-okunur izleyici linki, `list` yerel host listesi (link yok; `omp collab link` kullanılır), `status` link + katılımcılar, `stop` paylaşımı durdurur; bölüm ayrıca host tarafını **katılma** (`<link>`) ve **ayrılma** alt komutlarıyla yönetir.
- **Transcript/izleme komutları** — oturum transcript'ini panoya kopyalama (LLM istek JSON'unu tmp'ye yazar) ve oturum izini istatistik panelinde açma; komut adları registry'de biçimsel olarak çözülemedi, davranışlar binary'den doğrulandı.
- **Browser prelude headless/visible toggle** — tarayıcı ön ucunun görünür/headless modunu oturum bazında değiştirir; komut adı registry'de biçimsel olarak çözülemedi.
- **`/settings`** — Ayarlar menüsünü açar (binary: "Open settings menu"). Ayar değişiklikleri oturumda anında geçerli olur.
- **`/login [provider]` / `/logout`** — OAuth/API-key kimlik seçici; `/login <provider>` doğrudan o sağlayıcıya atlar, callback'i `omp login <redirect-url>` ile tamamlanabilir (providers.md).
- **`/usage`** — Abonelik/quota kullanımı raporlar (`omp usage` CLI'ının oturum içi karşılığı; cli-reference.md `usage` satırı).

### H. Dosya ve Kural Komutları

- `commands/*.md` — proje/kullanıcı dizinlerindeki dosya komutları; komuttan sonraki tüm metin `rawArgs` olarak komuta geçer (slash-command-internals.md §6).
- Kural komutları `rules/*.{md,mdc}` ve kök `RULES.md` komut değildir; kalıcı prompt'a gider.
- Profil dizinleri (`~/.omp/profiles/<name>/`) komutları kendi kökünden çeker.
- RPC/ACP istemcileri yerleşikler ve bundled komutlara erişir; UI-only overlay tabanlı olanlar (`/plan-review`, `/advisor configure`) TUI'a mahsustur.

> Not: `security` alt komut kümesi (`plan|scan|status|cancel|scans|show|import|export|validate|compare|disposition`) binary komut kaydında `omp` alt komutu imzasıyla kayıtlı; vendor dokümanlarda TUI slash `/security` olarak ayrıca belgelenmiyor — inceleme çıktıları `security://` kaynağı okunarak görüntülenir (tools/security_scan.md).