# Script di pulizia artefatti temporanei per tutte le materie
$rootDir = $PSScriptRoot

$subjectDirs = Get-ChildItem -Path $rootDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "main.tex")
}

$hasLatexmk = [bool](Get-Command latexmk -ErrorAction SilentlyContinue)
$auxExtensions = @("*.aux", "*.bbl", "*.bcf", "*.blg", "*.fdb_latexmk", "*.fls", "*.idx", "*.ilg", "*.ind", "*.lof", "*.log", "*.out", "*.run.xml", "*.synctex*", "*.toc", "*.nav", "*.snm", "*.vrb", "*.xdv")

Write-Host "Pulizia artefatti ausiliari LaTeX in corso..." -ForegroundColor Cyan

foreach ($dir in $subjectDirs) {
    Write-Host "--> Pulizia cartella: $($dir.Name)..." -ForegroundColor Gray
    if ($hasLatexmk) {
        Push-Location $dir.FullName
        try {
            & latexmk -c
        } finally {
            Pop-Location
        }
    }
    
    # Pulizia diretta via PowerShell per garantire la rimozione completa
    foreach ($ext in $auxExtensions) {
        Get-ChildItem -Path $dir.FullName -Filter $ext -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Pulizia completata con successo." -ForegroundColor Green
