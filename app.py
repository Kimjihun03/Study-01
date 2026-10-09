"""Local handwritten digit recognition using MNIST and weighted nearest neighbors."""

import argparse
import gzip
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent


def load_dataset(prefix):
    with gzip.open(ROOT / 'data' / f'{prefix}-images-idx3-ubyte.gz', 'rb') as stream:
        images = np.frombuffer(stream.read(), dtype=np.uint8, offset=16).reshape(-1, 28, 28)
    with gzip.open(ROOT / 'data' / f'{prefix}-labels-idx1-ubyte.gz', 'rb') as stream:
        labels = np.frombuffer(stream.read(), dtype=np.uint8, offset=8)
    return images, labels


def normalize(pixels):
    """Fit the ink into a 20-pixel box and center its mass in a 28-pixel image."""
    image = Image.fromarray(np.asarray(pixels, dtype=np.uint8))
    box = image.point(lambda value: 255 if value > 20 else 0).getbbox()
    if box is None:
        raise ValueError('Draw a digit before recognizing it.')
    image = image.crop(box)
    scale = 20 / max(image.size)
    image = image.resize(tuple(max(1, round(size * scale)) for size in image.size), Image.Resampling.LANCZOS)
    result = np.zeros((28, 28), dtype=np.float32)
    ink = np.asarray(image, dtype=np.float32)
    y, x = np.indices(ink.shape)
    mass = ink.sum()
    left = int(round(13.5 - (x * ink).sum() / mass))
    top = int(round(13.5 - (y * ink).sum() / mass))
    left = min(max(left, 0), 28 - image.width)
    top = min(max(top, 0), 28 - image.height)
    result[top:top + image.height, left:left + image.width] = ink
    return result / 255


class Recognizer:
    def __init__(self):
        images, self.labels = load_dataset('train')
        self.samples = images.reshape(-1, 784).astype(np.float32) / 255
        self.squared_norms = np.einsum('ij,ij->i', self.samples, self.samples)

    def predict(self, image):
        flat = np.asarray(image, dtype=np.float32).reshape(784)
        distances = np.maximum(self.squared_norms + flat @ flat - 2 * (self.samples @ flat), 0)
        indices = np.argpartition(distances, 7)[:7]
        votes = np.bincount(self.labels[indices], weights=1 / (distances[indices] + 0.001), minlength=10)
        scores = votes / votes.sum()
        return {'digit': int(scores.argmax()), 'scores': scores.tolist()}


class Handler(BaseHTTPRequestHandler):
    model = None

    def respond(self, status, content, content_type='application/json'):
        body = content.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.respond(200, (ROOT / 'web_version' / 'index.html').read_text(encoding='utf-8'), 'text/html')
        elif self.path == '/health':
            self.respond(200, json.dumps({'ready': True, 'samples': len(self.model.labels)}))
        else:
            self.respond(404, json.dumps({'error': 'Not found'}))

    def do_POST(self):
        if self.path != '/predict':
            self.respond(404, json.dumps({'error': 'Not found'}))
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 500000:
                raise ValueError('Invalid request size.')
            payload = json.loads(self.rfile.read(length))
            pixels = np.asarray(payload['pixels'], dtype=np.float32)
            if pixels.shape != (280, 280) or not np.isfinite(pixels).all() or pixels.min() < 0 or pixels.max() > 255:
                raise ValueError('Expected a 280 by 280 grayscale image with values from 0 to 255.')
            normalized = normalize(pixels)
            result = self.model.predict(normalized)
            result['preview'] = (normalized * 255).astype(np.uint8).tolist()
            self.respond(200, json.dumps(result))
        except (ValueError, KeyError, TypeError) as error:
            self.respond(400, json.dumps({'error': str(error)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--evaluate', type=int, default=0, metavar='COUNT')
    args = parser.parse_args()
    model = Recognizer()
    if args.evaluate:
        images, labels = load_dataset('t10k')
        count = min(args.evaluate, len(labels))
        correct = sum(model.predict(image.astype(np.float32) / 255)['digit'] == int(label)
                      for image, label in zip(images[:count], labels[:count]))
        print(f'MNIST held-out accuracy: {correct}/{count} ({correct / count:.1%})', flush=True)
        return
    Handler.model = model
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Open http://localhost:{args.port} in your browser. Press Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
