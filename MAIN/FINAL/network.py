"""
BPMI Robotic Annular Pipe Sanitization System
File Name: Network.py
Date Created: 3/5/2024 TSA
Date Last Modified: 3/5/2024 TSA
Description: Network class
Verion: 1.0.1
Authors: TSA

Build Notes: First Finished Implementation

Dependencies: None

References:

Additional Notes:

"""
import socket
import json

class NetworkCommunication:
    def __init__(self, receive_host='0.0.0.0', receive_port=12345, send_host='localhost', send_port=54321):
        self.receive_host = receive_host
        self.receive_port = receive_port
        self.send_host = send_host
        self.send_port = send_port
        self.receive_socket = None
        self.send_socket = None
        self.client_address = None
        self.setup_receive_connection()

    def setup_receive_connection(self):
        """Sets up the socket for receiving data."""
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_socket.bind((self.receive_host, self.receive_port))
        self.receive_socket.listen()
        print(f"Listening for incoming connections on {self.receive_host}:{self.receive_port}")

    def accept_connection(self):
        """Accepts an incoming connection."""
        connection, self.client_address = self.receive_socket.accept()
        print(f"Connection from {self.client_address}")
        return connection

    def receive_control_data(self,conn):
        buffer = ""
        try:
            while True:
                data = conn.recv(1024) # update to 4096 if needed
                if not data:
                    break
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    if message:
                        yield json.loads(message)
        except Exception as e:
            print(f"Error processing data: {e}")
            yield None


    def setup_send_connection(self):
        """Establishes a connection for sending data."""
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket.connect((self.send_host, self.send_port))
        print(f"Connected to {self.send_host}:{self.send_port} for sending data.")

    def send_data(self, data):
        """Sends data over the send socket."""
        if self.send_socket:
            self.send_socket.sendall(json.dumps(data).encode('utf-8') + '\n')

    def close_connection(self):
        """Closes both sending and receiving sockets."""
        if self.receive_socket:
            self.receive_socket.close()
        if self.send_socket:
            self.send_socket.close()
