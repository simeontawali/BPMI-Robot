"""
BPMI Robotic Annular Pipe Sanitization System
File Name: main.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: main script
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:

Additional Notes:
Ensure ports are the same on both the pi and the pc
Ensure Host is configured to the IP of the pi

"""
import ethernet_pc

HOST = '0.0.0.0' # use the same host as IP address of Pi
# TODO: setup PI IP automatically. Read IP and establish connection
PORT = 65432  # Port to listen on (non-privileged ports are > 1023) ensure port is same for PC/PI


class startup():
    client_socket = ethernet_pc.init_client(HOST,PORT)
    ethernet_pc.close_connection(client_socket)