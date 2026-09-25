@echo off
title Avvio Jupyter Lab (UniPi Notes Container)
echo ==================================================
echo    AVVIO RAPIDO JUPYTER LAB NEL CONTAINER DOCKER
echo ==================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-jupyter.ps1"
pause
