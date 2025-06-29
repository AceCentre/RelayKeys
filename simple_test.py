#!/usr/bin/env python3
"""
Simple RelayKeys test - just mouse movement and simple typing
"""

import json
import requests
import time

DAEMON_URL = "http://127.0.0.1:5383/"

def send_rpc_request(method, params):
    """Send a JSON-RPC request to the RelayKeys daemon"""
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1,
    }
    headers = {"content-type": "application/json"}
    
    try:
        response = requests.post(DAEMON_URL, data=json.dumps(payload), headers=headers, timeout=10)
        result = response.json()
        if "result" in result:
            return result["result"]
        elif "error" in result:
            print(f"Error: {result['error']}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    print("Simple RelayKeys Test")
    print("====================")
    
    print("1. Testing mouse movement in a circle...")
    
    # Move in a circle
    moves = [
        [50, 0, 0, 0],   # Right
        [0, 50, 0, 0],   # Down  
        [-50, 0, 0, 0],  # Left
        [0, -50, 0, 0],  # Up
    ]
    
    for i, move in enumerate(moves):
        print(f"   Move {i+1}: {move}")
        result = send_rpc_request("mousemove", [move])
        print(f"   Result: {result}")
        time.sleep(0.5)
    
    print("\n2. Testing mouse click...")
    result = send_rpc_request("mousebutton", [["l", "click"]])
    print(f"   Click result: {result}")
    
    print("\n3. Testing simple key press (Space)...")
    # Try a simple space key press - parameters need to be in an array
    result = send_rpc_request("keyevent", [["SPACE", [], True]])  # Key down
    print(f"   Space down result: {result}")
    time.sleep(0.1)
    result = send_rpc_request("keyevent", [["SPACE", [], False]])  # Key up
    print(f"   Space up result: {result}")
    
    print("\nTest completed! Check your iPhone to see if the mouse moved and if a space was typed.")

if __name__ == "__main__":
    main()
