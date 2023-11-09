import cv2
import numpy as np
import socket
import struct
import io

HOST = '192.168.137.57'  # IP address of the Raspberry Pi
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((HOST, PORT))
client_socket.listen(0)
connection = client_socket.accept()[0].makefile('rb')

try:
    cv2.namedWindow('Live Video', cv2.WINDOW_NORMAL)
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        cv2.imshow('Live Video', frame)
        if cv2.waitKey(1) == 27:
            break
finally:
    connection.close()
    client_socket.close()
    cv2.destroyAllWindows()
