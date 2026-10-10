# Oh-My-Pi (OMP) — Windows Terminal Nerd Font Notu

OMP TUI'si nerd sembol setiyle ikon çizer. İkonların bozuk kutu (tofu) yerine doğru görünmesi için iki şey gerekir:

1. Terminal yazı tipi bir **Nerd Font** olmalı ve **sistemde kurulu** olmalı.
2. Windows Terminal bu yazı tipini kullanacak şekilde ayarlanmalı (`settings.json`).

> Font kurulu değilse Windows Terminal `face` değerini sessizce yok sayar ve varsayılan
> yazı tipine düşer; hata vermez. Bu yüzden "ayar yapıldı ama ikonlar yine bozuk" durumu
> tipik olarak fontun kurulu olmamasından kaynaklanır.

## 1. Fontu kur

Yöntem A — winget:

```powershell
winget install -e --id DEVCOM.JetBrainsMonoNerdFont
```

Yöntem B — elle: Nerd Fonts → JetBrainsMono paketini indir (`JetBrainsMono.zip`), `.ttf`
dosyalarını seç → sağ tık → **Install for all users** (yönetici) ya da **Install**
(yalnız bu kullanıcı).

- Tercih: **NFM** = *Nerd Font Mono* (tek genişlikli/monospace terminal glifleri). Düz `Nerd Font`
  veya `... Propo` varyantı yerine NFM seç.
- Kurulumdan sonra **yeni bir terminal penceresi** aç; açık oturumlar font listesini yenilemez.

Kurulu aile adını doğrula (kayıt defteri font listesi):

```powershell
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts').PSObject.Properties.Name |
  Select-String 'JetBrains'
(Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts').PSObject.Properties.Name |
  Select-String 'JetBrains'
```

`HKLM` = tüm kullanıcılar, `HKCU` = yalnız bu kullanıcı. Görünen adın sonundaki `(TrueType)`
ekini at; kalan metin `settings.json` içindeki `face` ile birebir aynı olmalı.

## 2. Windows Terminal `settings.json`

Paket (Mağaza) sürümü yolu:

```
%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json
```

Dosyayı bulmanın kısayolu: Windows Terminal'de **Settings**'a `Shift` basılı tutarak tıkla;
`settings.json` varsayılan metin düzenleyicide açılır.

Diğer kurulumlar:

| Kurulum | Yol |
|---|---|
| Mağaza — Preview | `%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe\LocalState\settings.json` |
| Paketsiz (winget/scoop zip) | `%LOCALAPPDATA%\Microsoft\Windows Terminal\settings.json` |

Değişiklikten önce yedek al (`settings.json` → `settings.json.bak`):

```powershell
$p = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
Copy-Item $p "$p.bak"
```

Tüm profillere uygulamak için `profiles.defaults` altına ekle:

```json
"profiles": {
    "defaults": {
        "font": { "face": "JetBrainsMono NFM" }
    }
}
```

`face` değeri kurulu yazı tipinin aile adıyla **birebir** aynı olmalı; `JetBrainsMono NFM`
Nerd Fonts dokümantasyonundaki örnektir, yerel kurulumda kayıtlı ad farklı olabilir.
Adı doğrulamak için: **Ayarlar → Profiller → Varsayılanlar → Görünüm → Yazı tipi** açılır
listesi, Windows "Yazı tipleri" ayarı veya §1'deki kayıt defteri komutu. Listede
`JetBrainsMono NFM` yoksa kurulu fontun tam adını yaz (ör. `JetBrainsMono Nerd Font` ya da
`JetBrainsMono Nerd Font Mono`).

## 3. OMP tarafı (`config.yml`)

OMP'de nerd ikonlarını `symbolPreset` anahtarı seçer:

```yaml
symbolPreset: unicode   # unicode, nerd, ascii
```

- Dosyada **açıkça** yazılı bir değer (mevcut `unicode` gibi) otomatik yükseltilmez.
- Nerd ikonlarını zorlamak için `symbolPreset: nerd` yap.
- Ayar `default` provenansındayken, etkileşimli modda başarılı bir Glyph Protocol el sıkışması
  Unicode preset'i Nerd ikonlarına yükseltir (kayıtlı ayarı değiştirmez). Açıkça yazılı
  `unicode` bu yükseltmeyi almaz.
- `statusLine.preset: nerd` de durum çubuğunda nerd glifleri kullanır.

Kaynak: `USER/.omp/agent/config.yml`, `HARNESS/Omp/docs/theme.md`, `HARNESS/Omp/docs/settings.md`.

## 4. Doğrulama

1. Yeni bir Windows Terminal penceresi aç.
2. `omp` çalıştır.
3. İkonlar bozuk kutu / `?` (tofu) yerine şekil olarak görünmeli; satır yüksekliği kaymamalı.
4. Hâlâ bozuksa: `face` adı kurulu adla eşleşmiyor ya da font kurulumu için terminal yeniden
   başlatılmadı.

## Referanslar

- Nerd Fonts: https://github.com/ryanoasis/nerd-fonts (NFM = Nerd Font Mono)
- Windows Terminal görünüm ayarları: https://learn.microsoft.com/windows/terminal/customize-settings/profile-appearance
