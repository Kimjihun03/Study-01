# Created: 2026-09-28T19:06:23+09:00
"""Self-contained Windows launcher for the local web application."""
import argparse
import json
import sys
import threading
import urllib.request
import webbrowser
from pathlib import Path

if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import Handler, Recognizer, ROOT, ThreadingHTTPServer, load_dataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('Port must be between 0 and 65535.')

    # Binding first eliminates the race between probing and claiming a port.
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as error:
        if error.errno not in (13, 98, 10013, 10048) and getattr(error, 'winerror', None) not in (10013, 10048):
            raise
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    try:
        print('Loading the handwriting model. Please wait...', flush=True)
        Handler.model = Recognizer()
        if args.self_test:
            images, labels = load_dataset('train')
            result = Handler.model.predict(images[0].astype('float32') / 255)
            assert result['digit'] == int(labels[0]), result
            assert (ROOT / 'web_version' / 'index.html').is_file()
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(f'http://127.0.0.1:{server.server_port}/health', timeout=10) as response:
                assert json.load(response)['samples'] == 60000
            with opener.open(f'http://127.0.0.1:{server.server_port}/', timeout=10) as response:
                assert b'Handwritten Digit' in response.read()
            server.shutdown()
            worker.join()
            print('PASS: bundled model, prediction, web page, and HTTP health.', flush=True)
            return
        url = f'http://localhost:{server.server_port}'
        print(f'Open {url}', flush=True)
        print('Keep this window open. Close it or press Ctrl+C to stop.', flush=True)
        if not args.no_browser:
            webbrowser.open(url)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Unable to start Digit Studio: {error}', file=sys.stderr, flush=True)
        if sys.stdin.isatty():
            try:
                input('Press Enter to close...')
            except EOFError:
                pass
        sys.exit(1)
