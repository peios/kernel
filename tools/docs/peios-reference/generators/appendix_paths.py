"""Canonical kernel source for the native-reference generators."""
import os
from pathlib import Path
PKM = Path(os.environ.get('PEIOS_KERNEL_ROOT', Path(__file__).resolve().parents[4]))
LEARN = Path(os.environ['PEIOS_REFERENCE_RAW_OUTPUT'])
def learn_is_absent():
    return False
