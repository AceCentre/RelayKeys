#!/usr/bin/env python3
"""
Entry point wrapper for relaykeys CLI.
This script provides backward compatibility for the build system.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from relaykeys.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
