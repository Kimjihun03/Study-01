# PDF Practice Sequence

This project implements the programming exercise on pages 55-94 of the supplied PDF. Claude-specific setup screens and commands are represented by equivalent project files; no separate Claude installation or account is required.

1. **Pages 55-64: Build the desktop recognizer.** `desktop_version/digit_recognition.py` provides a native Tkinter window, white drawing canvas, Clear and Recognize buttons, and three ranked predictions. The shared engine uses 60,000 MNIST examples.
2. **Pages 65-71: Double-click execution.** `Start Desktop.bat` runs the native app from Windows Explorer. `Start Web.bat` runs the browser version. Both find the bundled Python runtime on this computer.
3. **Pages 73-79: Document the project.** Root `CLAUDE.md` records the overview, commands, stack, architecture, code style, and development notes.
4. **Pages 80-83: Record project rules.** The documentation specifies English source/comments and date/time comments for newly created source files. New version files contain actual creation timestamps.
5. **Pages 84-89: Separate versions.** `desktop_version` and `web_version` each contain their own entry point, interface, and `CLAUDE.md`. Shared recognition and data remain at the root to avoid duplicated model behavior and datasets.
6. **Pages 90-93: Run the web version.** Open http://localhost:8765, draw one digit, and click PREDICT. Its layout follows the PDF's final screenshot.

## Verification

The portable Windows x64 ZIP was extracted to a different directory and run with Python removed from PATH. Its bundled prediction, web page, and health checks passed both with a free port and with the requested port already occupied. This validates packaging and fallback behavior on the development PC; separate physical PCs have not been tested.

The previous engine evaluation recognized 964 of the first 1,000 held-out MNIST test images. API tests cover blank input, malformed dimensions, and ten enlarged digit examples passed through preprocessing. This accuracy is not a measurement of arbitrary user handwriting. Vote shares are not calibrated confidence probabilities.

## Files retained for compatibility

`app.py` remains a supported manual web entry point and the shared engine. `Start Digit Studio.cmd` remains a supported web launcher. `index.previous.html` preserves the original dark design. The root `index.html` is a compatibility copy; the active web interface is `web_version/index.html`.
