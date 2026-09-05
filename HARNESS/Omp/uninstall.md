OMP (Oh-My-Pi) kodlama asistanını sisteminizden tamamen kaldırmak için kurulum betiğinin oluşturduğu ikili dosyaları, yapılandırma klasörünü, ortam değişkeni (PATH) girdisini ve varsa Bun küresel paketini temizlemeniz gerekir.

### Olası Darboğazlar ve Kısıtlar

* **Dosya Kilidi (Process Lock):** Arka planda veya açık bir terminalde çalışan aktif bir `omp` süreci varsa, Windows dosyaların silinmesini engeller (`Access Denied`). Silme işlemine başlamadan önce süreç sonlandırılmalıdır.
* **Terminal PATH Önbelleği:** Ortam değişkeni temizlense bile o an açık olan PowerShell oturumu eski PATH değerini bellekte tutar. Değişikliğin geçerli olması için terminalin yeniden başlatılması gerekir.

---

### Tek Seferde Tam Temizlik (PowerShell)

Tüm adımları tek seferde çalıştırmak için PowerShell penceresini açıp aşağıdaki bloğu yapıştırabilirsiniz:

```powershell
# 1. Çalışan süreçleri durdur
Stop-Process -Name "omp" -Force -ErrorAction SilentlyContinue

# 2. Bun ile kurulduysa küresel paketi kaldır
if (Get-Command bun -ErrorAction SilentlyContinue) {
    bun remove -g @oh-my-pi/pi-coding-agent 2>$null
}

# 3. İkili dosya dizinini sil ($env:LOCALAPPDATA\omp)
$installDir = if ($env:PI_INSTALL_DIR) { $env:PI_INSTALL_DIR } else { "$env:LOCALAPPDATA\omp" }
if (Test-Path $installDir) {
    Remove-Item -Path $installDir -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Ayar ve oturum klasörünü sil (~/.omp)
$configDir = Join-Path $env:USERPROFILE ".omp"
if (Test-Path $configDir) {
    Remove-Item -Path $configDir -Recurse -Force -ErrorAction SilentlyContinue
}

# 5. Kullanıcı PATH değişkeninden kaldır
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -like "*$installDir*") {
    $newPath = ($userPath -split ';' | Where-Object { $_ -and $_.TrimEnd('\') -ne $installDir.TrimEnd('\') }) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
}

# 6. Kalan geçici yükleme dosyalarını temizle
Get-ChildItem -Path $env:TEMP -Filter "omp-install-*" -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "OMP ve ilişkili tüm dosyalar başarıyla temizlendi." -ForegroundColor Green

```

---

### Adım Adım Manuel Kaldırma ve Doğrulama

Süreci adım adım kontrol ederek ilerletmek isterseniz:

1. **Çalışan Süreçleri Kapatma**
```powershell
Stop-Process -Name "omp" -Force -ErrorAction SilentlyContinue

```


*Doğrulama:* `Get-Process omp -ErrorAction SilentlyContinue` komutunu çalıştırın; hiçbir çıktı dönmemelidir.
2. **Bun Küresel Paketini Kaldırma** (Kaynak koddan / Bun ile yüklendiyse)
```powershell
bun remove -g @oh-my-pi/pi-coding-agent

```


*Doğrulama:* `bun pm ls -g` komutunu çalıştırın; paket listesinde `@oh-my-pi/pi-coding-agent` yer almamalıdır.
3. **Yükleme Dizinini Silme**
Varsayılan konum `C:\Users\<KullanıcıAdı>\AppData\Local\omp` dizinidir:
```powershell
Remove-Item -Path "$env:LOCALAPPDATA\omp" -Recurse -Force

```


*Doğrulama:* `Test-Path "$env:LOCALAPPDATA\omp"` komutunu çalıştırın; sonuç `False` dönmelidir.
4. **Yapılandırma ve Verileri Temizleme**
Terminal yapılandırması ve ayarlar `C:\Users\<KullanıcıAdı>\.omp` içinde tutulur:
```powershell
Remove-Item -Path "$env:USERPROFILE\.omp" -Recurse -Force

```


*Doğrulama:* `Test-Path "$env:USERPROFILE\.omp"` komutunu çalıştırın; sonuç `False` dönmelidir.
5. **PATH Ortam Değişkenini Güncelleme**
Kullanıcı ortam değişkeninde kayıtlı dizin yolunu kaldırın:
```powershell
$installDir = "$env:LOCALAPPDATA\omp"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = ($userPath -split ';' | Where-Object { $_ -and $_.TrimEnd('\') -ne $installDir.TrimEnd('\') }) -join ';'
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")

```


*Doğrulama:* `[Environment]::GetEnvironmentVariable("Path", "User") -split ';' | Select-String "omp"` komutunu çalıştırın; boş dönmelidir.

İşlem tamamlandıktan sonra terminal oturumunuzu kapatıp yeniden açın. `omp` komutunu yazdığınızda komutun tanınmadığına dair hata alıyorsanız kaldırma işlemi başarıyla tamamlanmıştır.