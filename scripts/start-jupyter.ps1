<#
.SYNOPSIS
    Avvia rapidamente il server Jupyter Lab nel container Docker e apre il browser.
#>
$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   AVVIO JUPYTER LAB (DOCKER CONTAINER)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Verifica Docker
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    Write-Host "[ERRORE] Docker non e' installato o non e' presente nel PATH." -ForegroundColor Red
    exit 1
}

$null = & docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRORE] Docker Desktop non e' in esecuzione. Avvialo prima di continuare." -ForegroundColor Red
    exit 1
}

$rootDir = Split-Path $PSScriptRoot -Parent
Set-Location $rootDir

Write-Host "[1/3] Avvio del container Jupyter in background..." -ForegroundColor Yellow
& docker compose up -d jupyter

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRORE] Impossibile avviare il container Jupyter." -ForegroundColor Red
    exit 1
}

Write-Host "[2/3] Attesa inizializzazione server (3 secondi)..." -ForegroundColor DarkCyan
Start-Sleep -Seconds 3

$url = "http://localhost:8888/lab/tree/notebooks/1_basics_and_understanding.ipynb"
Write-Host "[3/3] Apertura del browser all'indirizzo:" -ForegroundColor Green
Write-Host "      $url" -ForegroundColor Green

Start-Process $url

Write-Host "`n[OK] Jupyter Lab e' attivo!" -ForegroundColor Green
Write-Host "Per arrestare il container quando hai finito, esegui:" -ForegroundColor Gray
Write-Host "    docker compose down" -ForegroundColor Cyan
