"""
BPMI Robotic Annular Pipe Sanitization System
File Name: ethernet_pc.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: ethernet data
Verion: 0.1.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:
https://realpython.com/python-sockets/

Additional Notes: None

"""

import socket
import struct

def init_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def send_data(client_socket, data, type="controller"):
    if type == "controller":
        client_socket.send(data.encode())
    else:
        # Assuming type is camera
        client_socket.sendall(data)

def receive_data(client_socket, type="camera"):
    if type == "camera" or type == "status_data":
        data = b""
        payload_size = struct.calcsize("<L")
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("<L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        return frame_data
    elif type == "controller":
        buffer = 1024
        data = client_socket.recv(buffer)
        return data
    else:
        raise ValueError("Invalid data type")

def close_connection(client_socket):
    client_socket.close()