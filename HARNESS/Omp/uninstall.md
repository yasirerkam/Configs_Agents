
---

### Kapsamlı Derin Temizlik Betiği (PowerShell)

Aşağıdaki komut bloğu, hem kurulum betiğinin hem de Bun ve çalışma zamanının oluşturduğu tüm ek izleri tarayıp temizler:

```powershell
# 1. Aktif süreçleri zorla kapat
Get-Process -Name "omp*" -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Kurulum ve çalışma zamanı dizinlerini kaldır
$pathsToRemove = @(
    "$env:LOCALAPPDATA\omp",
    "$env:USERPROFILE\.omp",
    "$env:USERPROFILE\.bun\bin\omp*",
    "$env:USERPROFILE\.bun\install\global\node_modules\@oh-my-pi"
)

foreach ($target in $pathsToRemove) {
    if (Test-Path $target) {
        Remove-Item -Path $target -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "[Silindi] $target" -ForegroundColor Yellow
    }
}

# 3. Bun önbelleğini temizle (Bun yüklüyse)
if (Get-Command bun -ErrorAction SilentlyContinue) {
    bun pm cache rm 2>$null
    bun remove -g @oh-my-pi/pi-coding-agent 2>$null
    Write-Host "[Temizlendi] Bun paket ve önbellek girdileri." -ForegroundColor Yellow
}

# 4. TEMP dizinindeki yükleyici kalıntılarını temizle
Get-ChildItem -Path $env:TEMP -Filter "*omp*" -Recurse -ErrorAction SilentlyContinue | 
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 5. Ortam değişkenlerini (PATH) temizle
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$installDir = if ($env:PI_INSTALL_DIR) { $env:PI_INSTALL_DIR } else { "$env:LOCALAPPDATA\omp" }
$newPath = ($userPath -split ';' | Where-Object { 
    $_ -and 
    $_.TrimEnd('\') -ne $installDir.TrimEnd('\')
}) -join ';'
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")

Write-Host "Derin temizlik tamamlandı." -ForegroundColor Green

```

---

### Sistemin Tamamen Temizlendiğini Doğrulama

Her bir adımın başarıyla tamamlandığını doğrulamak için yeni bir PowerShell penceresi açıp şu komutları çalıştırabilirsiniz:

1. **Komutun/Çalıştırılabilir Dosyaların Varlığını Kontrol Etme:**
```powershell
Get-Command omp -ErrorAction SilentlyContinue

```


*Doğrulama:* Hiçbir çıktı dönmemelidir. Eğer bir yol dönüyorsa, dosyanın bulunduğu konumu silmeniz gerekir.
2. **Dizin Kontrolü:**
```powershell
Test-Path "$env:LOCALAPPDATA\omp", "$env:USERPROFILE\.omp", "$env:USERPROFILE\.bun\bin\omp.exe"

```


*Doğrulama:* Tüm dönen değerlerin `False` olması gerekir.
3. **Proje İçi Kalıntı Kontrolü:**
OMP'yi çalıştırdığınız bir çalışma klasörünüz varsa, o dizinde gizli klasörleri listeleyin:
```powershell
Get-ChildItem -Path . -Filter ".omp" -Hidden

```


*Doğrulama:* Proje kök dizininde `.omp` klasörü listeleniyorsa `Remove-Item -Recurse -Force .omp` komutuyla manuel olarak kaldırabilirsiniz.