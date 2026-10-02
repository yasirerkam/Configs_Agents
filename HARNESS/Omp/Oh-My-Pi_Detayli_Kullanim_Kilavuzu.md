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
- `/advisor status`, `/advisor on`, `/advisor off` ile yönetilir.

---

### 3\. Kod İnceleme ve Canlı Eşli Çalışma

#### A. `/review` ve `/annotate`

- **`/review`:** Kod değişikliklerini denetleyen özel alt ajanlar başlatır. Sorunları P0 (kritik) ile P3 (küçük öneri) arasında sınıflandırır.  
- **`/annotate`:** İnceleme başlamadan önce diff veya yanıtlar üzerine satır bazında not iliştirmeyi sağlar (`/annotate code-review`, `/annotate last`).

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