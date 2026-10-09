# Created: 2026-09-28T18:45:14+09:00
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) {
    & $bundledPython digit_recognition.py
} else {
    python digit_recognition.py
}
exit $LASTEXITCODE
