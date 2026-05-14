#!/usr/bin/env python3
"""
Mouse repeat utility for RelayKeys.
Continuously sends mouse movement commands until stopped.
"""

import argparse
import os
import sys
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from relaykeys.core.client import RelayKeysClient


def main():
    parser = argparse.ArgumentParser(description="Repeat mouse movements")
    parser.add_argument("-x", "--x", type=int, default=0, help="X movement per iteration")
    parser.add_argument("-y", "--y", type=int, default=0, help="Y movement per iteration")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between movements in seconds")
    parser.add_argument("--url", default="http://127.0.0.1:5383/", help="RelayKeys daemon URL")
    
    args = parser.parse_args()
    
    if args.x == 0 and args.y == 0:
        print("Error: At least one of -x or -y must be non-zero")
        return 1
    
    client = RelayKeysClient(url=args.url)
    
    print(f"Starting mouse repeat: x={args.x}, y={args.y}, delay={args.delay}s")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            client.mousemove(args.x, args.y)
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\nStopped mouse repeat")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
