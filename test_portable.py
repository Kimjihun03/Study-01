# Created: 2026-09-28T19:06:23+09:00
"""Validate the packaged application after relocation without Python on PATH."""
import os
import socket
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='digit-portable-') as temporary:
    relocated = Path(temporary) / 'Portable app copy'
    with zipfile.ZipFile(ROOT / 'release' / 'DigitStudio-Windows-x64.zip') as archive:
        archive.extractall(relocated)
    environment = os.environ.copy()
    environment['PATH'] = str(Path(os.environ['SystemRoot']) / 'System32')
    environment.pop('PYTHONPATH', None)
    environment.pop('PYTHONHOME', None)
    executable = relocated / 'DigitStudio' / 'DigitStudio.exe'
    for collision in (False, True):
        with socket.socket() as occupied:
            occupied.bind(('127.0.0.1', 0))
            port = occupied.getsockname()[1]
            if collision:
                occupied.listen()
            else:
                occupied.close()
            result = subprocess.run(
                [str(executable), '--self-test', '--port', str(port)],
                cwd=temporary, env=environment, capture_output=True, text=True, timeout=60,
            )
            assert result.returncode == 0, result.stdout + result.stderr
            assert 'PASS:' in result.stdout, result.stdout
            print(f"PASS: relocated package, no Python on PATH, port collision={collision}")
