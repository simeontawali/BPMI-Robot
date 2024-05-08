"""
BPMI Robotic Annular Pipe Sanitization System
File Name: main.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: main script
Verion: 0.1.1
Authors: Tiwari, Gomez, Bennett

Build Notes:
    Initial structure and research

Dependencies: None

References:

Additional Notes:
    Ensure ports are the same on both the pi and the pc

"""

import subprocess
import time
import os, io
import sys
import threading

# command to run the camera streaming server script
# server_command = ['python','/mnt/usb_share/cam_stream.py']
# server_command = ['python','/mnt/usb_share/32-bit_cam_stream.py']
server_command = ['python','/mnt/usb_share/cam.py']
# command to run the ethernet controller script
ethernet_command = ['python','/mnt/usb_share/conn_manager.py']

def run_ethernet_script():
    while True:
        try:
            # Start the other Python script in a separate process
            ethernet_process = subprocess.Popen(ethernet_command)
            ethernet_process.wait()
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C) to gracefully terminate the process
            ethernet_process.terminate()
        time.sleep(5)  # Sleep for 5 seconds before retrying

try:
    # Start the streaming server script in a separate process
    server_process = subprocess.Popen(server_command)
    # Add a short delay to ensure that the streaming server has started
    time.sleep(0.1)
    
    # Start the Ethernet script in a separate thread
    ethernet_thread = threading.Thread(target=run_ethernet_script)
    ethernet_thread.start()

    # Wait for the streaming server process to complete
    server_process.wait()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully terminate both processes
    server_process.terminate()
    ethernet_thread.join()  # Wait for the Ethernet thread to finish



try:
    # Start the streaming server script in a separate process
    server_process = subprocess.Popen(server_command)
    # Add a short delay to ensure that the streaming server has started
    time.sleep(0.1)
    # Start the other Python script in a separate process
    ethernet_process = subprocess.Popen(ethernet_command)
    # Wait for both processes to complete
    server_process.wait()
    ethernet_process.wait()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully terminate both processes
    server_process.terminate()
    ethernet_process.terminate()

