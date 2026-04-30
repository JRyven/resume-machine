#!/usr/bin/env python3
"""Compatibility shim — forwards to utilities/config_manager.py."""

import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
NEW = os.path.join(HERE, 'utilities', 'config_manager.py')
if not os.path.exists(NEW):
    # best-effort fallback: attempt to import yaml and implement minimal loader
    try:
        import yaml  # type: ignore
    except Exception:
        pass

os.execv(sys.executable, [sys.executable, NEW] + sys.argv[1:])
