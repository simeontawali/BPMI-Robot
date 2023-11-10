"""
BPMI Robotic Annular Pipe Sanitization System
File Name: ethernet_pi.py
Date Created: 10/28 /2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: ethernet data
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies:

pip install picamera

References:
https://docs.python.org/3/library/socket.html
https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/
https://docs.python.org/3/library/pickle.html

Additional Notes: None

"""

import socket
import struct
import io
import picamera
import time

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

def send_data(client_socket, data, type="camera"):
    if type == "camera" or type == "third_data":
        client_socket.sendall(data)
    else:
        client_socket.send(data.encode())

def receive_data(client_socket, type="controller"):
    if type == "controller":
        buffer = 1024
        data = client_socket.recv(buffer)
        return data
    else:
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
    

def send_image(client_socket):
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)  # Set the resolution to 1080p
            camera.framerate = 60  # Set the framerate to 60 fps
            time.sleep(2)  # Give the camera some time to adjust to lighting
            start = time.time()
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # Write the length of the capture to the stream and flush to ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data
                stream.seek(0)
                connection.write(stream.read())
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
    finally:
        connection.close()


def close_connection(client_socket,server_socket):
    client_socket.close()
    server_socket.close()