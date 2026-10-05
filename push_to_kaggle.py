import sys
sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
"""
Push Audio-Automation Runner to Kaggle GPU (vinodkumartekam)
"""

import subprocess
import sys
from pathlib import Path

KAGGLE_DIR = Path(__file__).resolve().parent / "kaggle"

print("=" * 65)
print("\uf880 PUSHING AUDIO-AUTOMATION (CHATTERBOX V3) TO KAGGLE GPU")
print("=" * 65)

cmd = ["kaggle", "kernels", "push", "-p", str(KAGGLE_DIR)]
try:
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(res.stdout)
    print("\u2705 Successfully pushed kernel to Kaggle!")
    print("View and run at: https://www.kaggle.com/code/vinodkumartekam/audio-automation-chatterbox-v3")
except subprocess.CalledProcessError as e:
    print(f"\u2674 Error pushing to Kaggle: e{e.stderr or e.stdout}")
    sys.exit(1)
