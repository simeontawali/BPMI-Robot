"""
BPMI Robotic Annular Pipe Sanitization System
File Name: camera.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: Camera logic
Verion: 0.0.1
Authors: Gomez, Tiwari, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:

Additional Notes:

"""
import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl



class Camera(object):


    def init(self):
        pass

    server_socket = socket.socket()
    server_socket.bind(('192.168.1.159',8000))
    server_socket.listen(0)

    connection = server_socket.accept()[0].makefile('rb')

    try:
            img = None
            while True:
                image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))

                image_stream.seek(0)
                image = Image.open(image_stream)

                if img is None:
                      img = pl.imshow(image)
                else:
                    img.set_data

                pl.pause(0.01)
                pl.draw()

                print('Image is %dx%d' % image.size)
                image.verify()
                print('Image is verified')
    finally:
