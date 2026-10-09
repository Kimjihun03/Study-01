@echo off
rem Created: 2026-09-28T18:45:14+09:00
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0desktop_version\start.ps1"
if errorlevel 1 pause
endlocal
