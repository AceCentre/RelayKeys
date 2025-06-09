#!/usr/bin/env python3
"""
Entry point wrapper for device polling utility.
This script provides backward compatibility for the build system.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from relaykeys.utils.device_poller import *

if __name__ == "__main__":
    # The device_poller module runs its main logic when imported
    pass
