#!/usr/bin/env python3
"""
Entry point wrapper for relaykeysd daemon.
This script provides backward compatibility for the build system.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from relaykeys.core.daemon import main

if __name__ == "__main__":
    sys.exit(main())
