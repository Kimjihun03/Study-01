param([switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$portableExecutable = Join-Path $PSScriptRoot 'release\portable\DigitStudio\DigitStudio.exe'
if (Test-Path -LiteralPath $portableExecutable) {
    if ($NoBrowser) {
        & $portableExecutable --no-browser
    } else {
        & $portableExecutable
    }
    exit $LASTEXITCODE
}
$appUrl = 'http://localhost:8765'

function Test-AppReady {
    try {
        $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/health' -TimeoutSec 2
        return ($health.ready -eq $true -and $health.samples -eq 60000)
    } catch {
        return $false
    }
}

try {
    if (-not (Test-AppReady)) {
        $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
        if (Test-Path -LiteralPath $bundledPython) {
            $pythonPath = $bundledPython
        } else {
            $pythonPath = (Get-Command python -ErrorAction Stop).Source
        }
        $serverProcess = Start-Process -FilePath $pythonPath -ArgumentList 'web_version/server.py' `
            -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $PSScriptRoot 'server.log') `
            -RedirectStandardError (Join-Path $PSScriptRoot 'server-error.log')
        $deadline = (Get-Date).AddSeconds(30)
        while (-not (Test-AppReady)) {
            if ($serverProcess.HasExited) {
                throw 'The server could not start. See server-error.log for details.'
            }
            if ((Get-Date) -gt $deadline) {
                throw 'The server did not become ready within 30 seconds. See server-error.log.'
            }
            Start-Sleep -Milliseconds 300
        }
    }
    if (-not $NoBrowser) {
        Start-Process $appUrl
    }
    Write-Host "Digit Studio is running at $appUrl"
    exit 0
} catch {
    Write-Host "Unable to launch Digit Studio: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
