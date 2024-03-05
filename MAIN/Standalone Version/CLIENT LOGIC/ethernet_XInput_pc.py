"""
BPMI Robotic Annular Pipe Sanitization System
File Name: ethernet_XInput_pc.py
Date Created: 10/11/2023 SAT
Date Last Modified: 11/09/2023 SAT
Description: Controller to ethernet logic
Verion: 1.0.1
Authors: Gomez, Tiwari, Bennett

Build Notes: First Finished Implementation

Dependencies: XInput

References:

Additional Notes:

"""
import socket
import pickle
from XInput import *
import time

# logic for controlling the game or robot
def control(controller_values):
    # Example logic
    left_thumb_x, left_thumb_y = controller_values['left_thumb']
    right_thumb_x, right_thumb_y = controller_values['right_thumb']
    left_trigger, right_trigger = controller_values['triggers']
    buttons_pressed = controller_values['buttons']

# IP and port of the Raspberry Pi Zero
HOST = '169.254.80.45'  # Change this to the IP of your Pi Zero
PORT = 12345


# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Your main loop
while True:
    events = get_events()
    for event in events:
        controller_values = {
            'left_thumb': (0, 0),
            'right_thumb': (0, 0),
            'triggers': (0, 0),
            'buttons': set()
        }

        if event.type == EVENT_STICK_MOVED:
            if event.stick == LEFT:
                controller_values['left_thumb'] = (event.x, event.y)
            elif event.stick == RIGHT:
                controller_values['right_thumb'] = (event.x, event.y)

        elif event.type == EVENT_TRIGGER_MOVED:
            if event.trigger == LEFT:
                controller_values['triggers'] = (event.value, controller_values['triggers'][1])
            elif event.trigger == RIGHT:
                controller_values['triggers'] = (controller_values['triggers'][0], event.value)

        elif event.type == EVENT_BUTTON_PRESSED:
            controller_values['buttons'].add(event.button)

        elif event.type == EVENT_BUTTON_RELEASED:
            if event.button in controller_values['buttons']:
                controller_values['buttons'].remove(event.button)

        # Send the controller_values dictionary to the Raspberry Pi Zero
        data = pickle.dumps(controller_values)
        s.sendall(data)

    time.sleep(0.1)  # Adjust the sleep duration as needed
