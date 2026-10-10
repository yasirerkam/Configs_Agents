# Oh-My-Pi (OMP) Kurulum ve Yapılandırma Kılavuzu

Oh-My-Pi (OMP), terminal-yerel çalışan, IDE düzeyinde araçlarla donatılmış açık kaynaklı bir yapay zeka kodlama ajanı harness'ıdır.

## 1\. Ön Koşullar

- **İşletim Sistemleri:** macOS (Intel & Apple Silicon), Linux (x86\_64, aarch64), Windows (WSL gerektirmeden yerel çalışabilir).  
- **Çalışma Zamanı (Opsiyonel):** Paket yöneticisi ile kurulum için Bun (\>= 1.3.14) veya Node.js (\>= 18).  
- **Git** ve temel derleme araçları.  
- Desteklenen bir LLM sağlayıcısından geçerli API anahtarı (OpenAI, Anthropic, DeepSeek, xAI vb.).  
- **Terminal yazı tipi (Windows):** OMP TUI ikonları için kurulu bir Nerd Font ve Windows Terminal `settings.json` ayarı gerekir — bkz. [Oh-My-Pi\_Terminal\_Nerd\_Font\_Notu.md](./Oh-My-Pi_Terminal_Nerd_Font_Notu.md).

---

## 2\. İşletim Sistemine Göre Kurulum Yöntemleri

### A. macOS ve Linux (Önerilen Hızlı Kurulum)

Resmi tek satırlık kurulum betiği ile en güncel ikili dosyayı indirebilirsiniz:

curl \-fsSL https\://omp.sh/install | sh

> **Önemli (Apple Silicon Mac):** Sistemin x86\_64 Rosetta yerine yerel ARM64 ikili dosyasını (`omp-darwin-arm64`) indirdiğinden emin olun.

### B. Alpine Linux (musl)

Önceden derlenmiş musl ikili dosyası `libstdc++` ve `libgcc` kütüphanelerini dinamik olarak bağlar:

apk add libstdc++ libgcc

curl \-fsSL https\://omp.sh/install | sh

### C. Homebrew (macOS / Linux)

brew install can1357/tap/omp

### D. Bun (Önerilen Paket Yöneticisi)

bun install \-g @oh-my-pi/pi-coding-agent

### E. npm ile Kurulum

npm install \-g @oh-my-pi/pi-coding-agent

### F. Windows (PowerShell)

irm https\://omp.sh/install.ps1 | iex

### G. Nix ile Kurulum ve Çalıştırma

Kurulum yapmadan doğrudan denemek için:

nix run github:can1357/oh-my-pi

Aktif profile kalıcı olarak yüklemek için:

nix profile install github:can1357/oh-my-pi

Flake ve Home Manager kullanıcıları için bildirimsel (`declarative`) kurulum:

{

  inputs.omp.url \= "github:can1357/oh-my-pi";

  imports \= \[ inputs.omp.homeManagerModules.default \];

  programs.omp \= {

    enable \= true;

    settings.startup.quiet \= true;

  };

}

### H. Sürüm Yöneticileri (mise)

mise use \-g github:can1357/oh-my-pi

---

## 3\. Kabuk Otomatik Tamamlama (Shell Completions)

OMP, dinamik bayrak ve model isimleri için otomatik tamamlama betikleri üretir.

- **Zsh:** `~/.zshrc` dosyanıza ekleyin:  
    
  eval "\$(omp completions zsh)"  
    
- **Bash:** `~/.bashrc` dosyanıza ekleyin:  
    
  eval "\$(omp completions bash)"  
    
- **Fish:**  
    
  omp completions fish \> \~/.config/fish/completions/omp.fish

---

## 4\. Model Sağlayıcıları ve API Anahtarları

### A. Ortam Değişkenleri

Ortam değişkenlerini kabuk profilinize (`~/.bashrc` veya `~/.zshrc`) ekleyebilirsiniz:

export ANTHROPIC\_API\_KEY="sk-ant-..."

export OPENAI\_API\_KEY="sk-..."

export DEEPSEEK\_API\_KEY="sk-..."

export XAI\_API\_KEY="xai-..."

export PERPLEXITY\_API\_KEY="pplx-..."

### B. Özel Sağlayıcılar (`~/.omp/agent/models.yml`)

Yerel (vLLM, Ollama, LM Studio) veya özel OpenAI uyumlu sunucular tanımlayabilirsiniz:

providers:

  local-vllm:

    baseUrl: http\://localhost:8000/v1

    api: openai-completions

    apiKey: dummy

    models:

      \- id: qwen-2.5-coder

        name: Qwen 2.5 Coder

        contextWindow: 128000

        maxTokens: 16000

Tanımı doğrulamak için:

omp models local-vllm

---

## 5\. Araç Onay Modları (Approval Modes)

OMP üç güvenlik seviyesi sunar:

- **`yolo` (Varsayılan):** Okuma (`read`), yazma (`write`) ve komut çalıştırma (`exec`) işlemlerini sormadan otomatik onaylar.  
- **`write`:** Okuma ve yazmayı onaylar, komut yürütme (`exec`) öncesi onay ister.  
- **`always-ask`:** Okuma hariç tüm yazma ve çalıştırma işlemlerinde onay ister.

omp \--approval-mode write

---

## 6\. Dört Çalıştırma Giriş Noktası (Entry Points)

1. **İnteraktif TUI:** Standart tam ekran terminal arayüzü:  
     
   omp  
     
2. **Tek Turluk Komut (One-Shot):**  
     
   omp \-p "Mevcut repodaki unit testleri çalıştır ve hata raporu ver"  
     
3. **RPC Modu:** Harici programlar veya arayüzler için stdio JSON-RPC köprüsü:  
     
   omp \--mode rpc  
     
4. **ACP (Agent Client Protocol):** Zed ve benzeri editörlere entegre ajan olarak bağlanma:  
     
   omp acp

---

## 7\. İlk Başlatma ve Model Bayrakları

\# Belirli modellerle başlatma

omp \--model anthropic/claude-3-7-sonnet \--advisor openai/o3-mini

\# Görev rollerini başlatma sırasında geçersiz kılma (launch overrides)

omp \--smol openai/gpt-4o-mini \--slow anthropic/claude-3-7-sonnet \--plan anthropic/claude-3-7-sonnet

---

## 8\. Güncelleme ve Sorun Giderme

- **Güncelleme:**  
    
  omp update  
    
- **Önbellek Temizleme:** Paket yöneticisi ile yapılan güncellemelerde sürüm takılması yaşanırsa:  
    
  bun pm cache rm  
    
- **Versiyon Kontrolü:**  
    
  omp \--version

---

## 9\. Resmî Dokümantasyon (Referanslar)

**GitHub deposu:** https://github.com/can1357/oh-my-pi

**Dokümantasyon klasörü:** https://github.com/can1357/oh-my-pi/tree/main/docs

Öne çıkanlar:

- `docs/models.md` — `models.yml` / `models.yaml` sağlayıcı-model yapılandırması: env var auth çözümlemesi (`apiKey` önce ortam değişkeni adı olarak okunur, yoksa literal token olur), `discovery`, `compat`, merge sırası, command-resolved secrets (`!komut`)
- `docs/environment-variables.md` — env yükleme sırası, sağlayıcı kimlik değişkenleri, proxy yönlendirme
- `docs/compaction.md` — context compaction seçenekleri

Tüm docs dizini (2026-10 itibarıyla, 82 dosya):

- **Model & sağlayıcı:** `adding-a-provider.md`, `models.md`, `local-models.md`, `providers.md`, `provider-compat-reference.md`, `provider-endpoint-constraints.md`, `provider-quirks.md`, `provider-streaming-internals.md`, `compaction.md`, `non-compaction-retry-policy.md`, `environment-variables.md`, `secrets.md`
- **Oturum & bellek:** `session.md`, `session-operations-export-share-fork-resume.md`, `session-switching-and-recent-listing.md`, `session-tree-plan.md`, `context-files.md`, `memory.md`, `mnemosyne-memory-backend.md`, `handoff-generation-pipeline.md`, `tree.md`
- **Araçlar & çalışma zamanı:** `bash-tool-runtime.md`, `notebook-tool-runtime.md`, `resolve-tool-runtime.md`, `python-repl.md`, `computer-use.md`, `custom-tools.md`, `lsp-config.md`, `fs-scan-cache-architecture.md`, `prewalk.md`, `ai-schema-normalize.md`, `stream.md`
- **MCP & eklenti/uzantı:** `mcp-config.md`, `mcp-protocol-transports.md`, `mcp-runtime-lifecycle.md`, `mcp-server-tool-authoring.md`, `extensions.md`, `extension-loading.md`, `plugin-manager-installer-plumbing.md`, `hooks.md`, `task-agent-discovery.md`, `agent-hub.md`, `marketplace.md`, `advisor-watchdog.md`, `skills.md`, `system-prompt-customization.md`
- **TUI & tema:** `tui.md`, `tui-core-renderer.md`, `tui-runtime-internals.md`, `theme.md`, `keybindings.md`, `magic-keywords.md`, `slash-command-internals.md`, `vibe-mode.md`
- **Kimlik & güvenlik:** `approval-mode.md`, `auth-broker-gateway.md`, `install-id.md`, `macos-signing-notarization.md`
- **CLI & yapılandırma:** `cli-reference.md`, `config-usage.md`, `settings.md`, `rpc.md`, `sdk.md`, `omptype-guide.md`, `collab.md`, `gemini-manifest-extensions.md`, `ERRATA-GPT5-HARMONY.md`
- **Natives & iç mimari:** `native-crates.md`, `natives-architecture.md`, `natives-addon-loader-runtime.md`, `natives-binding-contract.md`, `natives-build-release-debugging.md`, `natives-media-system-utils.md`, `natives-rust-task-cancellation.md`, `natives-shell-pty-process.md`, `natives-text-search-pipeline.md`, `blob-artifact-architecture.md`, `rulebook-matching-pipeline.md`, `ttsr-injection-lifecycle.md`, `porting-from-pi-mono.md`, `porting-to-natives.md`, `user-facing-packages.md`