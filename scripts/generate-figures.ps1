# Genera su richiesta le figure vettoriali statiche per Data Mining
# Questo script va eseguito manualmente solo quando si modificano gli script di generazione figure,
# e NON viene eseguito in fase di compilazione LaTeX (le figure sono asset statici tracciati in git).

$rootDir = Split-Path -Parent $PSScriptRoot

Write-Host "`n[Docker] Generazione figure vettoriali Data-Mining..." -ForegroundColor DarkCyan
& docker compose -f "$rootDir\docker-compose.yml" run --rm figures

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Figure generate con successo in Data-Mining/assets/figures/`n" -ForegroundColor Green
} else {
    Write-Host "[ERRORE] Generazione figure fallita (exit code: $LASTEXITCODE)`n" -ForegroundColor Red
}
