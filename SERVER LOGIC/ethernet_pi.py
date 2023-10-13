"""
BPMI Pipe Cleaning and Inspection Robot
File Name: ethernet_pi.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: ethernet data
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:
https://docs.python.org/3/library/socket.html
https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/
https://docs.python.org/3/library/pickle.html

Additional Notes: None

"""

import socket, pickle

# host = '0.0.0.0' # all available network interfaces
# port = 12345 # pick a suitable port number

def init_server(host,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # one connection at a time
    print(f"Server is listening on {host}:{port}")
    return server_socket

def init_conection(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    return client_socket

def send_data(client_socket, data):
    data_serialized = pickle.dumps(data)
    client_socket.send(data_serialized)

def recieve_data(client_socket):
    data = client_socket.recv(1024)
    return pickle.loads(data)

def close_connection(client_socket,server_socket):
    client_socket.close()
    server_socket.close()