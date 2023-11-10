import socket
import cv2
import numpy as np
import struct

HOST = '192.168.1.2'  # Replace with the IP address of your Raspberry Pi
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter message (start/stop): ")
        s.sendall(message.encode())
        if message == 'start':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as img_socket:
                img_socket.connect((HOST, PORT))
                data = b""
                payload_size = struct.calcsize("<L")
                while True:
                    while len(data) < payload_size:
                        data += img_socket.recv(4096)
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("<L", packed_msg_size)[0]
                    while len(data) < msg_size:
                        data += img_socket.recv(4096)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame_bytes = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
                    cv2.imshow("Pi Camera Feed", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
