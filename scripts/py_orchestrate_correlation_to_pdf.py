#!/usr/bin/env python3
"""Compatibility shim — forwards to the reorganized orchestration script."""

import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
NEW = os.path.join(HERE, 'orchestration', 'py_orchestrate_correlation_to_pdf.py')
if not os.path.exists(NEW):
    print(f"Error: relocated orchestrator not found at {NEW}")
    sys.exit(1)

os.execv(sys.executable, [sys.executable, NEW] + sys.argv[1:])
