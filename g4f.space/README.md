
# OpenCode Model Konfigürasyon Oluşturucu

Bu Python betiği, `g4f.space` (veya benzeri OpenAI uyumlu bir API) uç noktasından sunulan geniş yapay zeka model listesini otomatik olarak çeker. İşlem sonucunda hem ham veriyi yedekler hem de belirlediğiniz modellere göre filtreleme yaparak [OpenCode](https://github.com/opencode) yapılandırmasına tam uyumlu bir `models` JSON dosyası üretir.

## 🚀 Özellikler

- **Sıfır Kurulum (Zero-Setup):** Astral `uv` aracı ile PEP 723 standartlarında çalışır. Manuel sanal ortam (`venv`) oluşturmanıza veya `pip install` yapmanıza gerek kalmaz; bağımlılıklar anında yönetilir.
- **İkili Kayıt Sistemi (Dual Save):** 
  - Uç noktadan gelen API yanıtını hiçbir değişikliğe uğratmadan `raw_models.json` olarak kaydeder.
  - Yalnızca belirlediğiniz hedeflere uyan modelleri filtreleyerek `opencode_models.json` olarak kaydeder.
- **Odaklı Filtreleme:** Yüzlerce gereksiz model yerine, sadece aktif olarak kullandığınız (ör. `deepseek-v4-pro`, `kimi`) modelleri aratır.
- **Güvenli Hata Yakalama:** API tarafında bir çökme veya bağlantı sorunu olduğunda akışı bozmadan terminal üzerinden bilgi verir.

## 📋 Gereksinimler

Betiği çalıştırmak için bilgisayarınızda **Python 3.11+** ve **`uv`** kurulu olmalıdır. 

Eğer `uv` kurulu değilse, işletim sisteminize göre aşağıdaki komutla kurabilirsiniz:

**macOS ve Linux:**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

```

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

```

## 🛠️ Kurulum ve Kullanım

1. `generate_config.py` dosyasını bilgisayarınıza indirin.
2. Terminalinizi açın ve dosyanın bulunduğu dizine gidin.
3. Betiği doğrudan `uv` ile çalıştırın:

```bash
uv run generate_config.py

```

İşlem tamamlandığında scriptin bulunduğu klasörde şu iki dosya otomatik olarak oluşturulacaktır:

* **`raw_models.json`**: API'den dönen tüm modellerin ham ve eksiksiz listesi.
* **`opencode_models.json`**: Uygulamanıza doğrudan kopyalayabileceğiniz, filtrelenmiş model konfigürasyonu.

## ⚙️ Konfigürasyon (Hedef Modelleri Değiştirme)

Sisteme yeni modeller eklemek veya çıkarmak isterseniz, `generate_config.py` dosyasını bir metin editörüyle açın ve `TARGET_MODELS` listesini güncelleyin:

```python
# Aratmak istediğiniz hedef modeller
TARGET_MODELS = [
    "deepseek-v4-pro", 
    "deepseek-v4-flash",
    "kimi-k2.6",      # Yeni model ekleyebilirsiniz
    "claude-3.5"      # Yeni model ekleyebilirsiniz
]

```

Betik bir sonraki çalışmasında, uç noktadaki model isimlerinde veya ID'lerinde bu metinleri arayacak ve eşleşenleri `opencode_models.json` dosyasına dahil edecektir.

## 📄 Çıktı Örneği (`opencode_models.json`)

Betik çalıştıktan sonra üretilen dosyanın içeriği `opencode.json` dosyanızdaki `models` nesnesiyle birebir aynı yapıdadır:

```json
{
  "models": {
    "srv_mkombumpae45db46dcb8:deepseek-ai/deepseek-v4-pro": {
      "name": "nvidia.com:deepseek-ai/deepseek-v4-pro"
    },
    "srv_mp1v9cyha31b95fa8c9a:deepseek-ai/deepseek-v4-pro": {
      "name": "KTAI - Free - Models:deepseek-ai/deepseek-v4-pro"
    }
  }
}
