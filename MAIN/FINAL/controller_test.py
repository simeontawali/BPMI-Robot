import socket
import pickle
import os
import time
import math
import json

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Accept a connection
conn, addr = s.accept()

def control(controller_values):
    try:
        left_thumb = controller_values.get('LeftThumb', (0, 0))
        left_thumb_x, left_thumb_y = left_thumb
        right_thumb = controller_values.get('RightThumb', (0, 0))
        right_thumb_x, right_thumb_y = right_thumb
        left_trigger, right_trigger = controller_values.get('Triggers', (0, 0))
        A, B, X, Y = controller_values.get('Buttons', (False, False, False, False))
        LeftShoulder, RightShoulder = controller_values.get('Shoulders', (False, False))
        DPadUp, DPadDown, DpadLeft, DpadRight = controller_values.get('DPad', (False, False, False, False))
        Start, Back = controller_values.get('Other', (False, False))

        # Print the values
        print(f"Left Thumb: {left_thumb_x}, {left_thumb_y}")
        print(f"Right Thumb: {right_thumb_x}, {right_thumb_y}")
        print(f"Triggers: L:{left_trigger}, R:{right_trigger}")
        print(f"Buttons: A:{A}, B:{B}, X:{X}, Y:{Y}")
        print(f"Shoulders: L:{LeftShoulder}, R:{RightShoulder}")
        print(f"DPad: Up:{DPadUp}, Down:{DPadDown}, Left:{DpadLeft}, Right:{DpadRight}")
        print(f"Other: Start:{Start}, Back:{Back}")
    except Exception as e:
        print("Error processing controller values:")
        print(e)
        print(controller_values)

i=0
while True:
    i+=1
    # Receive the data from the sender
    data = conn.recv(4096)

    if not data:
        break

    # Unpickle the received data
    #controller_values = pickle.loads(data)
    # Decode the bytes to a string then load string as JSON
    controller_values_str = data.decode('utf-8')
    controller_values = json.loads(controller_values_str)

    # Process the received data
    # Add your processing logic here
    if i % 6:
        os.system('cls' if os.name == 'nt' else 'clear')
        control(controller_values)

conn.close()
