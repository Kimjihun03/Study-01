# Created: 2026-09-28T18:45:14+09:00
"""Native desktop handwriting canvas using the shared MNIST recognizer."""
import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import Recognizer, normalize


class DigitWindow:
    def __init__(self, root):
        self.root = root
        self.model = None
        self.events = queue.Queue()
        self.revision = 0
        self.last = None
        self.has_ink = False
        self.busy = False
        root.title('Handwritten Digit Recognition - Desktop')
        root.resizable(False, False)
        root.configure(bg='#f3f3f8')
        frame = ttk.Frame(root, padding=24)
        frame.pack()
        ttk.Label(frame, text='Handwritten Digit Recognition', font=('Segoe UI', 17, 'bold')).pack()
        ttk.Label(frame, text='Draw one digit (0-9) in the box below.').pack(pady=(8, 18))
        self.canvas = tk.Canvas(frame, width=280, height=280, bg='white', highlightthickness=1, highlightbackground='#c9cad5')
        self.canvas.pack()
        self.canvas.bind('<ButtonPress-1>', self.begin)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', lambda event: setattr(self, 'last', None))
        buttons = ttk.Frame(frame)
        buttons.pack(pady=16)
        ttk.Button(buttons, text='Clear', command=self.clear).pack(side='left', padx=6)
        self.predict_button = ttk.Button(buttons, text='Recognize', command=self.predict, state='disabled')
        self.predict_button.pack(side='left', padx=6)
        self.status = tk.StringVar(value='Loading 60,000 MNIST examples...')
        ttk.Label(frame, textvariable=self.status, wraplength=320, justify='center').pack()
        self.result = tk.StringVar()
        ttk.Label(frame, textvariable=self.result, font=('Segoe UI', 13), justify='left').pack(pady=12)
        ttk.Label(frame, text='Percentages are neighbor votes, not confidence.', font=('Segoe UI', 9)).pack()
        self.clear()
        threading.Thread(target=self.load, daemon=True).start()
        root.after(80, self.poll)

    def load(self):
        try:
            self.events.put(('ready', Recognizer()))
        except Exception as error:
            self.events.put(('error', str(error)))

    def clear(self):
        self.revision += 1
        self.canvas.delete('all')
        self.image = Image.new('L', (280, 280), 0)
        self.ink = ImageDraw.Draw(self.image)
        self.has_ink = False
        self.last = None
        self.result.set('')
        if self.model is not None:
            self.status.set('Draw a digit, then click Recognize.')

    def begin(self, event):
        self.revision += 1
        self.has_ink = True
        self.result.set('')
        self.last = (event.x, event.y)
        self.mark(event.x, event.y)

    def mark(self, x, y):
        box = (x-9, y-9, x+9, y+9)
        self.canvas.create_oval(*box, fill='black', outline='black')
        self.ink.ellipse(box, fill=255)

    def draw(self, event):
        if self.last is None:
            return
        x, y = event.x, event.y
        self.canvas.create_line(*self.last, x, y, width=18, fill='black', capstyle=tk.ROUND)
        self.ink.line([self.last, (x, y)], fill=255, width=18)
        self.mark(x, y)
        self.last = (x, y)

    def predict(self):
        if not self.has_ink:
            self.status.set('Please draw a digit first.')
            return
        if self.model is None or self.busy:
            return
        self.busy = True
        self.predict_button.configure(state='disabled')
        self.status.set('Recognizing...')
        pixels, revision = np.asarray(self.image).copy(), self.revision

        def work():
            try:
                self.events.put(('prediction', (revision, self.model.predict(normalize(pixels)))))
            except Exception as error:
                self.events.put(('error', str(error)))
        threading.Thread(target=work, daemon=True).start()

    def poll(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == 'ready':
                    self.model = payload
                    self.status.set('Ready. Draw a digit, then click Recognize.')
                elif kind == 'prediction':
                    self.busy = False
                    revision, result = payload
                    if revision == self.revision:
                        self.status.set(f"Recognized digit: {result['digit']}")
                        ranked = sorted(enumerate(result['scores']), key=lambda item: -item[1])[:3]
                        self.result.set('\n'.join(f'Digit {digit}: {score:.1%}' for digit, score in ranked))
                else:
                    self.busy = False
                    self.status.set(f'Error: {payload}')
                if self.model is not None and not self.busy:
                    self.predict_button.configure(state='normal')
        except queue.Empty:
            pass
        self.root.after(80, self.poll)


if __name__ == '__main__':
    window = tk.Tk()
    DigitWindow(window)
    window.mainloop()
