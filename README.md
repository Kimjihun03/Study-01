# Handwritten Digit Recognition

## Run

- Double-click `Start Web.bat` to open the web version on localhost. Keep its console window open while using the app.
- Double-click `Start Desktop.bat` to open the desktop version. The desktop source requires Python with NumPy, Pillow, and Tkinter; the bundled runtime is used on this computer.
- Draw one digit from 0 to 9, then select PREDICT or Recognize. Use CLEAR to draw another digit.

## Use another Windows PC

Copy `release/DigitStudio-Windows-x64.zip`, extract it completely, and run `DigitStudio/DigitStudio.exe`. Keep its `_internal` folder beside the executable. This Windows 10/11 x64 package includes Python, dependencies, and model data. No installation or Internet connection is needed. If port 8765 is occupied, it uses an available localhost port. Organization security policies may restrict unsigned applications.

## Project files

- `app.py`: shared recognition engine and local HTTP implementation.
- `data/`: MNIST training and evaluation data.
- `desktop_version/`: native desktop source and launcher.
- `web_version/`: browser page and server source.
- `release/portable/DigitStudio/`: runnable portable web application.
- `release/DigitStudio-Windows-x64.zip`: distribution for another PC.
- `requirements.txt`: source dependencies.
- `CLAUDE.md`: project guidance, with version-specific guidance in each source folder.
- `start.ps1`, `Start Digit Studio.cmd`: helpers used by `Start Web.bat`.

The application recognizes one digit at a time using 60,000 MNIST examples. Displayed percentages are neighbor vote shares, not calibrated confidence. All code and comments are in English.

PDF preview images, earlier interface copies, build tools, build intermediates, and test scripts have been removed. Runtime log files may be recreated by the source launcher.
