"""
BPMI Robotic Annular Pipe Sanitization System
File Name: main.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
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


class main():

    server_socket = ethernet_pi.init_server(HOST,PORT)
    client_socket = ethernet_pi.init_conection(server_socket)


    #while True:
    #control_input = controller.get_input()

    #camera_pi.close()
    #sensors.close()
    ethernet_pi.close_connection(client_socket,server_socket)
