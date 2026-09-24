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

# Verifica presenza di Docker (unico prerequisito)
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    Write-Host "`n[ERRORE] 'docker' non e' stato trovato nel PATH." -ForegroundColor Red
    Write-Host "Questo progetto utilizza Docker per garantire la completa riproducibilità di LaTeX e Python." -ForegroundColor Yellow
    Write-Host "  -> Scarica e installa Docker Desktop: https://www.docker.com/products/docker-desktop`n" -ForegroundColor Gray
    exit 1
}

# Verifica che il daemon di Docker sia effettivamente in esecuzione
$null = & docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERRORE] Il daemon di Docker non e' in esecuzione." -ForegroundColor Red
    Write-Host "Avvia Docker Desktop per procedere con la compilazione delle dispense.`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Motore di compilazione: Container Docker (ambiente unificato LaTeX + Python)" -ForegroundColor Green

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
        # Se la materia è Data Mining e non esistono le figure o è invocato -Force, genera prima le figure nel container
        if ($subjectName -eq "Data-Mining" -and ($Force -or -not (Test-Path "$($dir.FullName)\assets\figures\it\iris_scatterplot_real.pdf"))) {
            Write-Host "     [Docker] Aggiornamento figure vettoriali Data-Mining..." -ForegroundColor DarkCyan
            & docker compose -f "$rootDir\docker-compose.yml" run --rm figures
        }

        # Esegui latexmk montando il workspace corrente nel container
        & docker compose -f "$rootDir\docker-compose.yml" run --rm -w "/workspace/$subjectName" app latexmk -pdf -interaction=nonstopmode $texFile

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
