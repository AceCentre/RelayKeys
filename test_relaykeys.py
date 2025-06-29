#!/usr/bin/env python3
"""
Test script for RelayKeys - tests mouse movement and macro execution
"""

import json
import requests
import time

# RelayKeys daemon endpoint
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

def test_mouse_movement():
    """Test mouse movement"""
    print("Testing mouse movement...")
    
    # Move mouse right
    print("Moving mouse right...")
    result = send_rpc_request("mousemove", [[50, 0, 0, 0]])
    print(f"Result: {result}")
    time.sleep(1)
    
    # Move mouse down
    print("Moving mouse down...")
    result = send_rpc_request("mousemove", [[0, 50, 0, 0]])
    print(f"Result: {result}")
    time.sleep(1)
    
    # Move mouse left
    print("Moving mouse left...")
    result = send_rpc_request("mousemove", [[-50, 0, 0, 0]])
    print(f"Result: {result}")
    time.sleep(1)
    
    # Move mouse up
    print("Moving mouse up...")
    result = send_rpc_request("mousemove", [[0, -50, 0, 0]])
    print(f"Result: {result}")

def test_mouse_click():
    """Test mouse clicking"""
    print("\nTesting mouse click...")
    
    # Left click
    print("Left click...")
    result = send_rpc_request("mousebutton", [["l", "click"]])
    print(f"Result: {result}")

def test_macro():
    """Test the iOS Notes macro"""
    print("\nTesting iOS Notes macro...")
    
    # Read the macro file
    try:
        with open("macros/open_ios_notes.txt", "r") as f:
            macro_lines = f.readlines()
        
        actions = []
        for line in macro_lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("keypress:"):
                # Parse keypress: KEY,MODIFIER
                parts = line[9:].split(",")
                key = parts[0]
                modifiers = parts[1:] if len(parts) > 1 else []
                actions.append(["keyevent", key, modifiers, True])  # Key down
                actions.append(["keyevent", key, modifiers, False]) # Key up
                
            elif line.startswith("type:"):
                # Parse type: text
                text = line[5:]
                for char in text:
                    actions.append(["keyevent", char.upper(), [], True])
                    actions.append(["keyevent", char.upper(), [], False])
                    
            elif line.startswith("delay:"):
                # For now, we'll just add the actions without delay
                # The daemon doesn't handle delays in the actions array
                pass
        
        # Send the actions
        if actions:
            print(f"Sending {len(actions)} actions...")
            result = send_rpc_request("actions", [actions])
            print(f"Result: {result}")
        
    except FileNotFoundError:
        print("Macro file not found!")
    except Exception as e:
        print(f"Error reading macro: {e}")

def check_daemon_status():
    """Check if daemon is running and connected"""
    print("Checking daemon status...")
    result = send_rpc_request("daemon", [["dongle_status"]])
    print(f"Dongle status: {result}")
    
    result = send_rpc_request("daemon", [["get_mode"]])
    print(f"Mode: {result}")

def main():
    print("RelayKeys Test Script")
    print("====================")
    
    # Check status first
    check_daemon_status()
    
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    # Test mouse movement
    test_mouse_movement()
    
    time.sleep(2)
    
    # Test mouse click
    test_mouse_click()
    
    time.sleep(2)
    
    # Test macro
    test_macro()
    
    print("\nTests completed!")

if __name__ == "__main__":
    main()
