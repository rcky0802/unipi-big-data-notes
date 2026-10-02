# Script di pulizia artefatti temporanei per tutte le materie (Docker-based & PowerShell)
$rootDir = Split-Path $PSScriptRoot -Parent

$subjectDirs = Get-ChildItem -Path $rootDir -Directory | Where-Object {
    (Test-Path (Join-Path $_.FullName "main.tex")) -or
    (Test-Path (Join-Path $_.FullName "main_it.tex")) -or
    (Test-Path (Join-Path $_.FullName "main_en.tex"))
}

$auxExtensions = @("*.aux", "*.bbl", "*.bcf", "*.blg", "*.fdb_latexmk", "*.fls", "*.idx", "*.ilg", "*.ind", "*.lof", "*.log", "*.out", "*.run.xml", "*.synctex*", "*.toc", "*.nav", "*.snm", "*.vrb", "*.xdv")

Write-Host "Pulizia artefatti ausiliari LaTeX in corso..." -ForegroundColor Cyan

# Se Docker è attivo, invoca prima il clean interno
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerCmd) {
    $null = & docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        & docker compose -f "$rootDir\docker-compose.yml" run --rm clean
    }
}

# Pulizia diretta file ausiliari e cartelle build sul filesystem host
foreach ($dir in $subjectDirs) {
    Write-Host "--> Pulizia cartella: $($dir.Name)..." -ForegroundColor Gray
    $buildDir = Join-Path $dir.FullName "build"
    if (Test-Path $buildDir) {
        Remove-Item -Path $buildDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    foreach ($ext in $auxExtensions) {
        Get-ChildItem -Path $dir.FullName -Filter $ext -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Pulizia completata con successo." -ForegroundColor Green
