<!-- Created: 2026-09-28T18:45:14+09:00 -->
# Handwritten Digit Recognition

## Project Overview
Local handwritten digit recognition with desktop and web interfaces, following the supplied PDF practice sequence.

## Commands
- `Start Desktop.bat`: open the native desktop canvas.
- `Start Web.bat`: start or reuse the local web server and open a browser.
- `python web_version/server.py`: start the web server manually.
- `python desktop_version/digit_recognition.py`: start the desktop app manually.
- `python app.py --evaluate 1000`: evaluate held-out MNIST images.

## Tech Stack
Python, NumPy, Pillow, Tkinter, standard-library HTTP server, HTML, CSS, JavaScript.

## Architecture
- `app.py`: shared recognition engine, normalization, dataset loading, and HTTP implementation.
- `data/`: shared MNIST training and test data.
- `desktop_version/`: native desktop interface and version-specific guidance.
- `web_version/`: browser interface, server entry point, and version-specific guidance.
- `start.ps1`: Windows web launcher.

## Code Style
Write all source code and comments in English. Add creation date and time comments to new source files. Keep model behavior shared between versions.

## Development Notes
Recognize one digit from 0 through 9 at a time. Neighbor vote shares are not calibrated probabilities. Bind the HTTP server to localhost. Read README.md for launch instructions. PDF preview images, old interface copies, build tools, and test scripts were removed during cleanup. The portable web executable and distribution ZIP remain under release/.
