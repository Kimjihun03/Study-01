# Created: 2026-09-28T19:06:23+09:00
"""Build the Windows x64 portable web distribution with PyInstaller."""
import sys
import shutil
import importlib.metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.build-tools'))
import PyInstaller.__main__

PyInstaller.__main__.run([
    str(ROOT / 'web_version' / 'portable.py'),
    '--name', 'DigitStudio', '--onedir', '--console', '--noconfirm',
    '--distpath', str(ROOT / 'release' / 'portable'),
    '--workpath', str(ROOT / 'build' / 'portable'),
    '--specpath', str(ROOT / 'build'),
    '--paths', str(ROOT),
    '--add-data', str(ROOT / 'web_version' / 'index.html') + ';web_version',
    '--add-data', str(ROOT / 'data' / 'train-images-idx3-ubyte.gz') + ';data',
    '--add-data', str(ROOT / 'data' / 'train-labels-idx1-ubyte.gz') + ';data',
    '--exclude-module', 'tkinter', '--exclude-module', 'matplotlib',
    '--exclude-module', 'pandas', '--exclude-module', 'scipy',
    '--exclude-module', 'IPython', '--exclude-module', 'pytest',
])

output = ROOT / 'release' / 'portable' / 'DigitStudio'
shutil.copyfile(ROOT / 'PORTABLE_README.txt', output / 'START HERE.txt')
licenses = output / 'LICENSES'
licenses.mkdir(exist_ok=True)
for name in ('numpy', 'pillow'):
    distribution = importlib.metadata.distribution(name)
    for item in distribution.files:
        source = distribution.locate_file(item)
        if 'license' in str(item).lower() and source.is_file():
            shutil.copyfile(source, licenses / (name + '-' + Path(str(item)).name))
for name in ('LICENSE.txt', 'LICENSE'):
    source = Path(sys.base_prefix) / name
    if source.is_file():
        shutil.copyfile(source, licenses / 'Python-LICENSE.txt')
shutil.make_archive(str(ROOT / 'release' / 'DigitStudio-Windows-x64'), 'zip', ROOT / 'release' / 'portable', 'DigitStudio')
