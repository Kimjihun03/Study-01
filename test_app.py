"""Exercise preprocessing and the running local prediction API."""

import json
import unittest
import urllib.error
import urllib.request

import numpy as np
from PIL import Image

from app import load_dataset, normalize


class RecognitionTests(unittest.TestCase):
    def request_prediction(self, pixels):
        request = urllib.request.Request(
            'http://127.0.0.1:8765/predict',
            data=json.dumps({'pixels': pixels}).encode(),
            headers={'Content-Type': 'application/json'},
        )
        return urllib.request.urlopen(request, timeout=20)

    def test_blank_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize(np.zeros((280, 280), dtype=np.uint8))
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request_prediction(np.zeros((280, 280), dtype=np.uint8).tolist())
        self.assertEqual(caught.exception.code, 400)

    def test_invalid_shape_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request_prediction([[255]])
        self.assertEqual(caught.exception.code, 400)

    def test_scaled_handwriting_round_trip(self):
        images, labels = load_dataset('t10k')
        correct = 0
        for digit in range(10):
            index = np.flatnonzero(labels == digit)[0]
            image = Image.fromarray(images[index]).resize((280, 280), Image.Resampling.BILINEAR)
            with self.request_prediction(np.asarray(image).tolist()) as response:
                result = json.load(response)
            correct += result['digit'] == digit
            self.assertAlmostEqual(sum(result['scores']), 1)
            self.assertEqual(np.asarray(result['preview']).shape, (28, 28))
        self.assertGreaterEqual(correct, 9)
        print(f'Scaled handwriting integration check: {correct}/10')


if __name__ == '__main__':
    unittest.main()
