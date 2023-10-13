"""
BPMI Pipe Cleaning and Inspection Robot
File Name: ethernet_pc.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: ethernet data
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:
https://realpython.com/python-sockets/

Additional Notes: None

"""

import socket

def init_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def send_data(client_socket, data):
    client_socket.send(data.encode())

def recieve_data(client_socket):
    buffer = 1024
    data = client_socket.recv(buffer)
    return data

def close_connection(client_socket):
    client_socket.close()