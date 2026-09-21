<#
.SYNOPSIS
    Sistema di compilazione intelligente e multilingua (IT/EN) per appunti universitari.
.DESCRIPTION
    Compila le dispense LaTeX in italiano e in inglese.
    Rileva automaticamente le modifiche per lingua e materia, supporta
    la selezione interattiva, la scelta della lingua e la sincronizzazione
    dei PDF nella cartella 'pdf/'.
.PARAMETER Subject
    Specifica il nome di una o più materie (es. "Algorithm-Engineering", "Data-Mining").
.PARAMETER Lang
    Specifica la lingua da compilare: "IT", "EN" o "ALL" (default: "ALL").
.PARAMETER All
    Forza la compilazione di tutte le materie e lingue.
.PARAMETER Force
    Forza la ricompilazione anche se non sono rilevate modifiche.
.PARAMETER Interactive
    Apre un menu interattivo nel terminale.
.PARAMETER DistributeToPdfFolder
    Copia i PDF compilati in 'pdf/' con suffisso lingua (es. Data-Mining-IT.pdf).
#>
[CmdletBinding(DefaultParameterSetName = "Smart")]
param(
    [Parameter(ParameterSetName = "Specific", Position = 0)]
    [string[]]$Subject,

    [ValidateSet("IT", "EN", "ALL")]
    [string]$Lang = "ALL",

    [Parameter(ParameterSetName = "All")]
    [switch]$All,

    [Parameter(ParameterSetName = "Interactive")]
    [switch]$Interactive,

    [Parameter(ParameterSetName = "Smart")]
    [switch]$Smart,

    [switch]$Force,
    [switch]$DistributeToPdfFolder = $true
)

$rootDir = $PSScriptRoot
$pdfOutDir = Join-Path $rootDir "pdf"

if ($DistributeToPdfFolder -and -not (Test-Path $pdfOutDir)) {
    New-Item -ItemType Directory -Path $pdfOutDir -Force | Out-Null
}

# Rileva tutte le cartelle materia
$availableSubjects = Get-ChildItem -Path $rootDir -Directory | Where-Object {
    (Test-Path (Join-Path $_.FullName "main.tex")) -or
    (Test-Path (Join-Path $_.FullName "main_it.tex")) -or
    (Test-Path (Join-Path $_.FullName "main_en.tex"))
}

if ($availableSubjects.Count -eq 0) {
    Write-Warning "Nessuna cartella materia trovata in $rootDir."
    exit 0
}

# Auto-discovery per latexmk
$latexmkPath = Get-Command latexmk -ErrorAction SilentlyContinue
if (-not $latexmkPath) {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\latexmk.exe",
        "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\latexmk.exe",
        "$env:ProgramFiles\MiKTeX\miktex\bin\x64\latexmk.exe",
        "${env:ProgramFiles(x86)}\MiKTeX\miktex\bin\latexmk.exe",
        "C:\MiKTeX\miktex\bin\x64\latexmk.exe"
    ) + (Get-Item "C:\texlive\*\bin\*\latexmk.exe" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)

    foreach ($cand in $candidates) {
        if ($cand -and (Test-Path $cand)) {
            $latexmkDir = Split-Path -Parent $cand
            $env:PATH = "$latexmkDir;$env:PATH"
            $latexmkPath = Get-Command latexmk -ErrorAction SilentlyContinue
            if ($latexmkPath) {
                Write-Host "[INFO] Individuata installazione LaTeX in: $latexmkDir" -ForegroundColor Cyan
                break
            }
        }
    }
}

# Auto-discovery per motore Perl (necessario per latexmk su Windows)
$perlPath = Get-Command perl -ErrorAction SilentlyContinue
if (-not $perlPath) {
    $perlCandidates = @(
        "C:\Program Files\Git\usr\bin\perl.exe",
        "C:\Program Files (x86)\Git\usr\bin\perl.exe",
        "C:\Strawberry\perl\bin\perl.exe",
        "C:\Perl64\bin\perl.exe",
        "C:\Perl\bin\perl.exe"
    )
    foreach ($p in $perlCandidates) {
        if (Test-Path $p) {
            $perlDir = Split-Path -Parent $p
            $env:PATH = "$perlDir;$env:PATH"
            $perlPath = Get-Command perl -ErrorAction SilentlyContinue
            if ($perlPath) {
                Write-Host "[INFO] Individuato motore Perl in: $perlDir" -ForegroundColor Cyan
                break
            }
        }
    }
}

# Assicura che MiKTeX installi i pacchetti mancanti in automatico senza blocchi GUI
$initexmf = Get-Command initexmf -ErrorAction SilentlyContinue
if ($initexmf) {
    try {
        & initexmf --set-config-value [MPM]AutoInstall=1 2>$null | Out-Null
    } catch { }
}

if (-not $latexmkPath) {
    Write-Host "`n[ERRORE] 'latexmk' non e' stato trovato nel PATH o nelle directory standard." -ForegroundColor Red
    Write-Host "Per compilare i documenti LaTeX e' necessaria una distribuzione TeX:" -ForegroundColor Yellow
    Write-Host "  -> Scarica e installa MiKTeX da: https://miktex.org/download" -ForegroundColor Yellow
    Write-Host "     (Durante l'installazione seleziona 'Install missing packages on the fly: Yes')" -ForegroundColor Gray
    Write-Host "  -> Oppure TeX Live da: https://tug.org/texlive/`n" -ForegroundColor Gray
    exit 1
}

# Funzione per testare se una specifica combinazione (Materia, Lingua) ha modifiche
function Test-TargetModified {
    param(
        [System.IO.DirectoryInfo]$Dir,
        [string]$Language # "IT" o "EN"
    )

    $langLower = $Language.ToLower()
    $texFile = "main_$langLower.tex"
    $fullTexPath = Join-Path $Dir.FullName $texFile
    
    # Se non esiste main_it o main_en, usa main.tex come fallback
    if (-not (Test-Path $fullTexPath)) {
        $texFile = "main.tex"
        $fullTexPath = Join-Path $Dir.FullName $texFile
    }

    if (-not (Test-Path $fullTexPath)) {
        return @{ Exists = $false; IsModified = $false; Reason = "File sorgente $texFile non presente" }
    }

    $pdfFile = [System.IO.Path]::ChangeExtension($texFile, ".pdf")
    $pdfPath = Join-Path $Dir.FullName $pdfFile

    if (-not (Test-Path $pdfPath)) {
        return @{ Exists = $true; IsModified = $true; Reason = "PDF ($pdfFile) non ancora generato"; TexFile = $texFile; PdfFile = $pdfFile }
    }

    $pdfTime = (Get-Item $pdfPath).LastWriteTimeUtc

    # Raccogli file sorgente specifici per questa lingua
    $sources = @()
    $sources += Get-Item $fullTexPath
    
    $preamble = Join-Path $Dir.FullName "config\preamble_$langLower.tex"
    if (Test-Path $preamble) { $sources += Get-Item $preamble }
    $bib = Join-Path $Dir.FullName "references.bib"
    if (Test-Path $bib) { $sources += Get-Item $bib }

    $chapDir = Join-Path $Dir.FullName "chapters\$langLower"
    if (Test-Path $chapDir) {
        $sources += Get-ChildItem -Path $chapDir -Filter *.tex -Recurse -File
    }

    $assetDir = Join-Path $Dir.FullName "assets"
    if (Test-Path $assetDir) {
        $sources += Get-ChildItem -Path $assetDir -Recurse -File
    }

    foreach ($file in $sources) {
        if ($file.LastWriteTimeUtc -gt $pdfTime) {
            return @{
                Exists = $true
                IsModified = $true
                Reason = "'$($file.Name)' modificato il $(($file.LastWriteTime).ToString('yyyy-MM-dd HH:mm:ss'))"
                TexFile = $texFile
                PdfFile = $pdfFile
            }
        }
    }

    return @{ Exists = $true; IsModified = $false; Reason = "PDF aggiornato"; TexFile = $texFile; PdfFile = $pdfFile }
}

# Costruzione lista target (Materia + Lingua)
$targetsToProcess = @()
$languagesToBuild = if ($Lang -eq "ALL") { @("IT", "EN") } else { @($Lang) }

# Selezione materie
$selectedDirs = $availableSubjects
if ($Subject -and $Subject.Count -gt 0) {
    $selectedDirs = $availableSubjects | Where-Object {
        $subjectName = $_.Name
        $Subject | Where-Object { $subjectName -like "*$_*" }
    }
    if ($selectedDirs.Count -eq 0) {
        Write-Warning "Nessuna materia corrisponde a '$($Subject -join ', ')'. Disponibili: $(($availableSubjects.Name) -join ', ')"
        exit 1
    }
}

# Gestione modalità interattiva
if ($Interactive) {
    Write-Host "`n==================================================" -ForegroundColor Cyan
    Write-Host "     SELEZIONE COMPILAZIONE APPUNTI (IT / EN)" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Materie rilevate:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $availableSubjects.Count; $i++) {
        Write-Host "  [$($i + 1)] $($availableSubjects[$i].Name)"
    }
    Write-Host "  [A] Tutte le materie"
    Write-Host "--------------------------------------------------" -ForegroundColor Cyan
    $subjChoice = Read-Host "Scegli materia (1, 2, A)"
    
    if ($subjChoice -match "^[Aa]$" -or [string]::IsNullOrWhiteSpace($subjChoice)) {
        $selectedDirs = $availableSubjects
    } else {
        $idx = [int]$subjChoice - 1
        if ($idx -ge 0 -and $idx -lt $availableSubjects.Count) {
            $selectedDirs = @($availableSubjects[$idx])
        }
    }

    Write-Host "`nLingua:" -ForegroundColor Yellow
    Write-Host "  [1] Italiano (IT)"
    Write-Host "  [2] Inglese (EN)"
    Write-Host "  [3] Entrambe (IT + EN)"
    $langChoice = Read-Host "Scegli lingua (1, 2, 3)"
    switch ($langChoice) {
        "1" { $languagesToBuild = @("IT") }
        "2" { $languagesToBuild = @("EN") }
        default { $languagesToBuild = @("IT", "EN") }
    }
}

$buildPlan = @()
$skippedPlan = @()

foreach ($dir in $selectedDirs) {
    foreach ($l in $languagesToBuild) {
        $check = Test-TargetModified -Dir $dir -Language $l
        if ($check.Exists) {
            $item = [PSCustomObject]@{
                Directory = $dir
                Subject = $dir.Name
                Language = $l
                TexFile = $check.TexFile
                PdfFile = $check.PdfFile
                Reason = if ($Force -or $All) { "Compilazione forzata" } else { $check.Reason }
                NeedsBuild = ($Force -or $All -or $check.IsModified)
            }
            if ($item.NeedsBuild) {
                $buildPlan += $item
            } else {
                $skippedPlan += $item
            }
        }
    }
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "   PIANO DI COMPILAZIONE MULTILINGUA" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if ($skippedPlan.Count -gt 0) {
    Write-Host "`nDispense già aggiornate (SKIP):" -ForegroundColor DarkGray
    foreach ($item in $skippedPlan) {
        Write-Host "  - [$($item.Language)] $($item.Subject): $($item.Reason)" -ForegroundColor DarkGray
    }
}

if ($buildPlan.Count -eq 0) {
    Write-Host "`n[OK] Tutte le dispense ($($languagesToBuild -join ', ')) sono gia' compilate e aggiornate!" -ForegroundColor Green
    Write-Host "     (Usa -Force per ricompilare comunque)`n" -ForegroundColor DarkGray
    exit 0
}

Write-Host "`nDispense da compilare ($($buildPlan.Count)): " -ForegroundColor Yellow
foreach ($item in $buildPlan) {
    Write-Host "  * [$($item.Language)] $($item.Subject) ($($item.TexFile)) -> $($item.Reason)" -ForegroundColor Yellow
}
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

$successCount = 0
$failCount = 0

foreach ($item in $buildPlan) {
    $dir = $item.Directory
    $subjectName = $item.Subject
    $lang = $item.Language
    $texFile = $item.TexFile
    $pdfFile = $item.PdfFile

    Write-Host "`n>>> [$lang] Compilazione: $subjectName ($texFile)..." -ForegroundColor Cyan

    Push-Location $dir.FullName
    try {
        & latexmk -pdf -interaction=nonstopmode $texFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Compilato con successo: $subjectName [$lang]" -ForegroundColor Green
            $successCount++

            if ($DistributeToPdfFolder -and (Test-Path $pdfFile)) {
                $targetPdf = Join-Path $pdfOutDir "$subjectName-$lang.pdf"
                Copy-Item -Path $pdfFile -Destination $targetPdf -Force
                Write-Host "     PDF salvato in: pdf/$subjectName-$lang.pdf" -ForegroundColor Gray
            }
        } else {
            Write-Host "[ERRORE] Fallimento compilazione per $subjectName [$lang] (exit code: $LASTEXITCODE)" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "[ECCEZIONE] Errore critico per $($subjectName) [$lang]: $_" -ForegroundColor Red
        $failCount++
    } finally {
        Pop-Location
    }
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "  Riepilogo finale: $successCount riuscite, $failCount fallite" -ForegroundColor Cyan
Write-Host "==================================================`n" -ForegroundColor Cyan
