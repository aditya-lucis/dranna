# tools/doctor.py — wrapper CLI untuk verifikasi lingkungan
import sys
import os

# Tambahkan root workspace ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anna.src.reset.doctor import doctor

if __name__ == "__main__":
    sys.exit(0 if doctor() == 0 else 1)
