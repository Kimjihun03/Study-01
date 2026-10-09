# Created: 2026-09-28T18:45:14+09:00
"""Start the web version with the shared MNIST recognition engine."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import main

if __name__ == '__main__':
    main()
