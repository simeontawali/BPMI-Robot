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

"""
script_dir = os.path.dirname(os.path.realpath(__file__))
server_path = os.path.join(script_dir, 'cam_stream.py')
ethernet_path = os.path.join(script_dir, 'ethernet_controller_pi.py')
with io.open(server_path, 'r') as f:
    server_command = ['python',f]
with io.open(ethernet_path, 'r') as f:
    ethernet_command = ['python',f]
    """

# Define the command to run the streaming server script
server_command = ['python','/mnt/usb_share/cam_stream.py']
# Define the command to run the other Python script
ethernet_command = ['python','/mnt/usb_share/ethernet_controller_pi.py']

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

