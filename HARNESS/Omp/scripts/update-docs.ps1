param(
    [string]$RepoUrl = 'https://github.com/can1357/oh-my-pi',
    [string]$Branch = 'main'
)

$ErrorActionPreference = 'Stop'

$OmpRoot = Split-Path -Parent $PSScriptRoot
$Dest = Join-Path $OmpRoot 'docs'
$Marker = Join-Path $OmpRoot 'docs-source.txt'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git PATH uzerinde bulunamadi'
}

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('omp-oh-my-pi-' + [guid]::NewGuid().ToString('N'))

try {
    git clone --depth 1 --filter=blob:none --sparse $RepoUrl $tmp
    if ($LASTEXITCODE -ne 0) { throw "git clone basarisiz (exit $LASTEXITCODE)" }

    git -C $tmp sparse-checkout set docs
    if ($LASTEXITCODE -ne 0) { throw "sparse-checkout basarisiz (exit $LASTEXITCODE)" }

    $rev = (git -C $tmp rev-parse HEAD).Trim()
    if ($rev -notmatch '^[0-9a-f]{40}$') { throw "rev cozumlenemedi: '$rev'" }

    $UpDocs = Join-Path $tmp 'docs'
    $upFiles = (Get-ChildItem -Path $UpDocs -Recurse -File -Force | Measure-Object).Count
    if ($upFiles -eq 0) { throw 'yukaridan docs agaci bos geldi' }
    if (-not (Test-Path (Join-Path $UpDocs 'models.md'))) { throw 'docs\models.md bulunamadi (cipa dosyasi)' }

    if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
    Move-Item (Join-Path $tmp 'docs') $Dest

    $newFiles = (Get-ChildItem -Path $Dest -Recurse -File -Force | Measure-Object).Count
    if ($newFiles -ne $upFiles) { throw "ayna eksik: $newFiles/$upFiles" }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $markerText = "source: $RepoUrl`nbranch: $Branch`nrev: $rev`nfetched: $(Get-Date -Format 'yyyy-MM-dd')`n"
    [System.IO.File]::WriteAllText($Marker, $markerText, $utf8NoBom)

    Write-Host "OK: docs/ guncellendi -> $rev ($newFiles dosya)"
}
finally {
    if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
}
