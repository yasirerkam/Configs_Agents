#requires -Version 5.1
<#
.SYNOPSIS
    Generates air-gapped (intranet) variants of opencode configs from the live files.

.DESCRIPTION
    Produces intranet-specific config variants by applying two deltas:
      1. Model endpoints are swapped to local servers (LiteLLM / OpenWebUI).
      2. Air-Gapped operational constraints are appended to markdown prompts.

    Default mode: writes <name>.intranet.<ext> variants next to the live configs
    (e.g. AGENTS.md -> AGENTS.intranet.md). Generated variants are tracked in the
    repo and treated as generated artifacts: manual edits are overwritten on the
    next run.

    NOTE: On the intranet machine the files under agents\*.intranet.md register
    as extra subagents (architect.intranet, etc.) because opencode loads every
    markdown file in the agents dir. Benign: they mirror the -Apply'd live agents.

    NOTE: opencode.intranet.jsonc intentionally keeps the @mohak34/opencode-notifier
    npm plugin; the script prints a red warning for the air-gapped startup fetch.
    The flat reasoningEffort/textVerbosity keys match the current opencode schema.

    -Apply mode:  overwrites the live configs directly (intended on intranet machines).

    Intranet machine deployment:
      git fetch origin
      git reset --hard origin/main
      powershell -ExecutionPolicy Bypass -File .\scripts\generate-intranet.ps1 -Apply -Backup

    Re-running on an already-intranet machine is a safe no-op (no cloud model ids
    remain and the marker block is already present). .bak backups are refused on
    second run unless -Force is given.

    NOTE: agents/committer_gitFlow.md is deliberately NOT touched (still carries a
    cloud model) -- it has no intranet variant by design.

.EXAMPLE
    .\generate-intranet.ps1

.EXAMPLE
    .\generate-intranet.ps1 -Apply -Backup

.EXAMPLE
    .\generate-intranet.ps1 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$Apply,
    [switch]$Backup,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---- Config (adjust per deployment) ----
$PrimaryModel = 'LiteLLM-glm-5.2/glm-5.2'
$FallbackModel = 'OpenWebUI/glm-5.2'
$MarkerBegin = '<!-- INTRANET-BEGIN -->'
$MarkerEnd = '<!-- INTRANET-END -->'

$AirGappedSection = @'
**CRITICAL:** You are operating within a strictly isolated, internal air-gapped network with **ZERO internet access**. You must strictly adhere to the following environmental rules:

* **No External Execution:** Do not write scripts, commands, or code that attempt to reach out to the internet (e.g., `curl` to web URLs, external API calls, or web scraping).
* **Anti-Hallucination & Documentation Request:** Do NOT generate responses based on memorization, guessing, or assumptions. If you are uncertain about the specific workings, syntax, updates, or best practices of a framework, library, or software, **halt immediately**. Explicitly notify the user: *"I am uncertain about the specifics of [Framework/Software] and cannot access the internet to verify."* Then, request the user to download the official documentation or relevant guides from an external network and provide it to you before proceeding.
* **Dependency Request Protocol:** If your proposed solution requires ANY external resource (e.g., a package via `pip install`, an external npm/PowerShell module, or a framework):
1. **Halt & Notify:** Do NOT provide instructions assuming the user can simply run an install command.
2. **List Requirements:** Provide a precise, exact list of the required package names or versions.
3. **Delegation:** Explicitly ask the user to download these files from an external network and transfer them into the internal environment before you proceed with integration instructions.
'@

$ConfigDir = Split-Path $PSScriptRoot -Parent
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-FileRaw {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { throw "Girdi dosyasi yok: $Path" }
    return [System.IO.File]::ReadAllText($Path)
}

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-Eol {
    param([string]$Text)
    if ($Text.Contains("`r`n")) { return "`r`n" }
    return "`n"
}

function Assert-NoCloudModels {
    param([string]$Text, [string]$Label)
    if ($Text -match 'opencode-go/') {
        throw "$Label : cikti icinde 'opencode-go/' model kalintisi var - donusum eksik"
    }
}

function Set-FrontmatterModel {
    param([string]$Text, [string]$Model, [string]$Label)
    $block = [regex]::Match($Text, '(?s)^---\r?\n.*?\r?\n---')
    if (-not $block.Success) { throw "$Label : frontmatter blogu bulunamadi" }
    $new = $block.Value -replace '(?m)^model:\s*.*?(?=\r?\n)', "model: `"$Model`""
    if ($new -eq $block.Value) { throw "$Label : frontmatter icinde 'model:' satiri bulunamadi" }
    return $Text.Replace($block.Value, $new)
}

function Add-AirGappedSection {
    param([string]$Text, [string]$Heading, [string]$Label)
    $eol = Get-Eol $Text
    $escapedBegin = [regex]::Escape($MarkerBegin)
    $escapedEnd = [regex]::Escape($MarkerEnd)
    $clean = [regex]::Replace($Text, "(?s)\r?\n?\s*$escapedBegin.*?$escapedEnd", '')
    $clean = $clean.TrimEnd("`r", "`n")
    $section = $AirGappedSection -replace "`r?`n", $eol
    $block = $MarkerBegin + $eol + $Heading + $eol + $eol + $section + $eol + $MarkerEnd
    $result = $clean + $eol + $eol + $block + $eol
    if ($result -match [regex]::Escape($MarkerBegin)) {
        $count = ([regex]::Matches($result, [regex]::Escape($MarkerBegin))).Count
        if ($count -gt 1) { throw "$Label : air-gapped blogu birden fazla kez eklendi" }
    }
    return $result
}

function ConvertTo-IntranetMd {
    param([string]$Path, [string]$Heading, [bool]$AddSection, [string]$Label)
    $text = Read-FileRaw $Path
    if ($text -match '(?m)^---\r?\n') {
        $text = Set-FrontmatterModel $text $PrimaryModel $Label
    }
    if ($AddSection) { $text = Add-AirGappedSection $text $Heading $Label }
    Assert-NoCloudModels $text $Label
    return $text
}

function ConvertTo-IntranetJson {
    param([string]$Path, [string]$Label)
    $json = Read-FileRaw $Path | ConvertFrom-Json
    $expectedAgents = @($json.agents.PSObject.Properties).Count
    $expectedCategories = @($json.categories.PSObject.Properties).Count
    foreach ($prop in $json.agents.PSObject.Properties) {
        $agent = $prop.Value
        $agent.model = $PrimaryModel
        if ($null -ne $agent.fallback_models) {
            $agent.fallback_models = @(@{ model = $FallbackModel })
        }
    }
    foreach ($prop in $json.categories.PSObject.Properties) {
        $cat = $prop.Value
        $cat.model = $PrimaryModel
        if ($null -ne $cat.fallback_models) {
            $cat.fallback_models = @(@{ model = $FallbackModel })
        }
    }
    $out = $json | ConvertTo-Json -Depth 10
    $check = $out | ConvertFrom-Json
    $actualAgents = @($check.agents.PSObject.Properties).Count
    $actualCategories = @($check.categories.PSObject.Properties).Count
    if ($actualAgents -ne $expectedAgents -or $actualCategories -ne $expectedCategories) {
        throw "$Label : JSON donusumu veri kaybetti (agent $expectedAgents->$actualAgents, kategori $expectedCategories->$actualCategories)"
    }
    $fbOut = [regex]::Matches($out, '"fallback_models":\s*(\[|\{)') | ForEach-Object { $_.Groups[1].Value }
    if ($fbOut | Where-Object { $_ -ne '[' }) {
        throw "$Label : fallback_models dizi olarak korunamadi (PS 5.1 serializer tek elemani object'e indirdi)"
    }
    $out = $out -replace 'opencode-go/[\w.-]+', $PrimaryModel
    Assert-NoCloudModels $out $Label
    return $out
}

function ConvertTo-IntranetJsonc {
    param([string]$Path, [string]$Label)
    $text = Read-FileRaw $Path
    $matches = [regex]::Matches($text, 'opencode-go/[\w.-]+')
    if ($matches.Count -eq 0) {
        if ($text -notmatch [regex]::Escape($PrimaryModel)) {
            throw "$Label : 'opencode-go/' model eslesmesi yok ve hedef model zaten mevcut degil"
        }
    }
    $out = $text -replace 'opencode-go/[\w.-]+', $PrimaryModel
    Assert-NoCloudModels $out $Label
    return $out
}

try {
    $targets = @(
        @{ Src = 'AGENTS.md';            Out = 'AGENTS.intranet.md';                  Heading = '# OPERATIONAL ENVIRONMENT CONSTRAINTS (AIR-GAPPED NETWORK)'; AddSection = $true;  Type = 'md' },
        @{ Src = 'agents\architect.md';  Out = 'agents\architect.intranet.md';        Heading = '## Operational Environment Constraints (Air-Gapped Network)'; AddSection = $true;  Type = 'md' },
        @{ Src = 'agents\reviewer.md';   Out = 'agents\reviewer.intranet.md';         Heading = '### 4. Operational Environment Constraints (Air-Gapped Network)'; AddSection = $true;  Type = 'md' },
        @{ Src = 'agents\committer.md';  Out = 'agents\committer.intranet.md';        Heading = '';                                                             AddSection = $false; Type = 'md' },
        @{ Src = 'oh-my-openagent.jsonc'; Out = 'oh-my-openagent.intranet.jsonc';     Heading = '';                                                             AddSection = $false; Type = 'json' },
        @{ Src = 'opencode.jsonc';       Out = 'opencode.intranet.jsonc';             Heading = '';                                                             AddSection = $false; Type = 'jsonc' }
    )

    if ($Apply -and -not $Force) {
        foreach ($t in $targets) {
            $srcPath = Join-Path $ConfigDir $t.Src
            $src = Read-FileRaw $srcPath
            if ($src -match 'opencode-go/[\w.-]+') {
                throw "Dev makine korumasi: -Apply, '$($t.Src)' icinde hala bulut modeli varken calisamaz. -Force kullan."
            }
        }
    }

    foreach ($t in $targets) {
        $srcPath = Join-Path $ConfigDir $t.Src
        $targetPath = if ($Apply) { $srcPath } else { Join-Path $ConfigDir $t.Out }
        $label = if ($Apply) { $t.Src } else { $t.Out }

        switch ($t.Type) {
            'md'   { $content = ConvertTo-IntranetMd $srcPath $t.Heading $t.AddSection $label }
            'json' { $content = ConvertTo-IntranetJson $srcPath $label }
            'jsonc' { $content = ConvertTo-IntranetJsonc $srcPath $label }
        }

        $existing = $null
        if (Test-Path -LiteralPath $targetPath) { $existing = Read-FileRaw $targetPath }
        if ($null -ne $existing -and $existing -eq $content) {
            Write-Host "SKIP (degismemis): $label" -ForegroundColor DarkGray
            continue
        }

        if (-not $PSCmdlet.ShouldProcess($targetPath, 'intranet varyantini yaz')) { continue }

        if ($Apply -and $Backup) {
            $bak = $targetPath + '.bak'
            if (Test-Path -LiteralPath $bak) {
                if (-not $Force) { throw "Yedek zaten var: $bak (ucune yazmamak icin -Force gerek)" }
                Write-Host "UYARI: mevcut yedegin uzerine yazildi: $bak" -ForegroundColor Yellow
            }
            Copy-Item -LiteralPath $targetPath -Destination $bak -Force
            Write-Host "BACKUP: $bak" -ForegroundColor Cyan
        }

        Write-Utf8NoBom $targetPath $content
        Write-Host "YAZILDI: $label" -ForegroundColor Green
        if ($t.Out -eq 'opencode.intranet.jsonc') {
            Write-Host "UYARI: opencode.intranet.jsonc icinde '@mohak34/opencode-notifier@latest' plugin'i duruyor. Air-gapped makinede opencode baslangicta npm erisimi deneyecek (basarisiz olabilir). Gerekirse plugin'i manuel kaldirin." -ForegroundColor Red
        }
    }

    Write-Host "Tamam. Intranet makinelerinde: git fetch origin; git reset --hard origin/main; .\scripts\generate-intranet.ps1 -Apply -Backup" -ForegroundColor Magenta
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
