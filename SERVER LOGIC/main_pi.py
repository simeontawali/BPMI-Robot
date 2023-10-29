"""
BPMI Robotic Annular Pipe Sanitization System
File Name: main.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: main script
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes:
    Initial structure and research

Dependencies: None

References:

Additional Notes:
    Ensure ports are the same on both the pi and the pc

"""
 
import camera_pi
import sensors
import ethernet_pi

HOST = '0.0.0.0' # all available networks
# TODO: setup PI IP automatically. Read IP and establish connection
PORT = 65432  # Port to listen on (non-privileged ports are > 1023) ensure port is the same for both PC/PI


# main_pi.py
from motor_control import control_motors
from ethernet_pi import init_server, init_conection, send_data, recieve_data, close_connection
import ctypes

class XINPUT_GAMEPAD(ctypes.Structure):
    # Define the structure of XINPUT_GAMEPAD here based on the definition in controller.py
    _fields_ = [
        # Define the fields of XINPUT_GAMEPAD here
    ]

# Function to convert the received string back to XINPUT_GAMEPAD
def convert_to_gamepad(data):
    packet_number, gamepad_data = data.split(b',', 1)
    gamepad = XINPUT_GAMEPAD.from_buffer_copy(gamepad_data)
    return int(packet_number), gamepad


# Initialize the server on the Raspberry Pi
server_socket = init_server(HOST, PORT)
connection = init_conection(server_socket)

try:
    while True:
        # Receive data from the PC
        data = recieve_data(connection)
        packet_number, gamepad = convert_to_gamepad(data)
        # Control the motors based on the received controller input
        control_motors(packet_number, gamepad)

except KeyboardInterrupt:
    pass
finally:
    # Close the connection
    close_connection(connection, server_socket)
