Digit Studio - Portable Web Version

Supported target: Windows 10/11, x64 (Intel/AMD 64-bit).

1. Extract the entire ZIP to a local folder.
2. Open the DigitStudio folder.
3. Double-click DigitStudio.exe.
4. Wait for the browser to open at http://localhost:<port>.
5. Draw one digit and click PREDICT. Use CLEAR to start again.

Keep the console window open while using the application.
Close the console window or press Ctrl+C to stop the server.

No separate Python installation, package installation, API key, or Internet
connection is needed. Python, NumPy, Pillow, the web page, and the MNIST
training data are included. Keep the _internal folder beside DigitStudio.exe.
Do not run the executable from inside the ZIP viewer.

The default port is 8765. If it is occupied, an available port is selected
automatically and the browser opens the actual address. If your browser
does not open automatically, copy the address printed in the console.
The server accepts connections only from this computer.

This is a locally built, unsigned application. Organization security policies
may prevent it from running; follow your organization's software policy.
The package has been tested on the development computer, not every PC.

MNIST dataset: Yann LeCun, Corinna Cortes, and Christopher J. C. Burges.
Data source: https://storage.googleapis.com/cvdf-datasets/mnist/
Third-party license notices are included in the LICENSES folder.
