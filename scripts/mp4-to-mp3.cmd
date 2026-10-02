@echo off
rem Launcher Windows CMD per convertire videolezioni MP4 in MP3 mono 64k tramite Docker
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0mp4-to-mp3.ps1" %*
