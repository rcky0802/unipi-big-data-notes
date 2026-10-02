<#
.SYNOPSIS
    Converte una videolezione MP4 in MP3 mono a 64 kbps eseguendo Python e FFmpeg nel container Docker.
    Se la durata dell'audio supera 1 ora, viene automaticamente diviso in due meta'.
.PARAMETER FilePath
    Percorso del file MP4 da convertire (relativo o assoluto).
.PARAMETER OutputPath
    Percorso del file MP3 di output (opzionale, default: stesso nome e cartella con estensione .mp3).
.PARAMETER Bitrate
    Bitrate audio (default: "64k").
.PARAMETER Channels
    Numero di canali audio (default: 1 per mono).
.EXAMPLE
    .\scripts\mp4-to-mp3.ps1 "D:\Archivio\Download\Lecture5.mp4"
    .\scripts\mp4-to-mp3.ps1 "lezione.mp4" -OutputPath "audio_lezione.mp3"
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$FilePath,

    [Parameter(Position = 1)]
    [string]$OutputPath,

    [string]$Bitrate = "64k",
    [int]$Channels = 1
)

if ([string]::IsNullOrWhiteSpace($FilePath)) {
    Write-Host "`nUso: .\scripts\mp4-to-mp3.cmd <percorso_file.mp4> [percorso_output.mp3]" -ForegroundColor Yellow
    Write-Host "Esempio: .\scripts\mp4-to-mp3.cmd `"D:\Archivio\Download\Lecture5.mp4`"`n" -ForegroundColor Gray
    exit 1
}

$rootDir = Split-Path $PSScriptRoot -Parent

# Verifica presenza Docker
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    Write-Host "`n[ERRORE] 'docker' non trovato nel PATH. Avvia Docker Desktop per eseguire la conversione.`n" -ForegroundColor Red
    exit 1
}

# Risolvi percorso assoluto del file di input
if (-not (Test-Path $FilePath)) {
    Write-Host "`n[ERRORE] File di input non trovato: '$FilePath'`n" -ForegroundColor Red
    exit 1
}

$resolvedInput = (Resolve-Path $FilePath).Path
$inputDir = Split-Path $resolvedInput -Parent
$inputFileName = Split-Path $resolvedInput -Leaf

$rootDirDocker = $rootDir -replace '\\', '/'
$inputDirDocker = $inputDir -replace '\\', '/'

# Gestione output
$outputArgs = @()
if ($OutputPath) {
    $resolvedOutput = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
    $outputDir = Split-Path $resolvedOutput -Parent
    if (-not $outputDir) { $outputDir = (Get-Location).Path }
    $outputDirDocker = $outputDir -replace '\\', '/'
    $outputFileName = Split-Path $resolvedOutput -Leaf
    
    # Se la directory di output e' diversa da quella di input, la montiamo
    if ($outputDir -ne $inputDir) {
        $dockerArgs = @(
            "run", "--rm",
            "-v", "${rootDirDocker}:/workspace",
            "-v", "${inputDirDocker}:/input_media",
            "-v", "${outputDirDocker}:/output_media",
            "-w", "/workspace",
            "university-notes-compiler:latest",
            "python3", "scripts/mp4_to_mp3.py",
            "/input_media/$inputFileName",
            "-o", "/output_media/$outputFileName",
            "-b", $Bitrate,
            "-c", "$Channels"
        )
        & docker @dockerArgs
        exit $LASTEXITCODE
    } else {
        $outputArgs = @("-o", "/media/$outputFileName")
    }
}

# Monta la cartella del video in /media nel container
$dockerArgs = @(
    "run", "--rm",
    "-v", "${rootDirDocker}:/workspace",
    "-v", "${inputDirDocker}:/media",
    "-w", "/workspace",
    "university-notes-compiler:latest",
    "python3", "scripts/mp4_to_mp3.py",
    "/media/$inputFileName"
)

if ($outputArgs.Count -gt 0) {
    $dockerArgs += $outputArgs
}
$dockerArgs += @("-b", $Bitrate, "-c", "$Channels")

& docker @dockerArgs
exit $LASTEXITCODE
