#!/usr/bin/env python3
"""
Entry point wrapper for relaykeys Qt GUI.
This script provides backward compatibility for the build system.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from relaykeys.gui.qt_app import main

if __name__ == "__main__":
    sys.exit(main())
