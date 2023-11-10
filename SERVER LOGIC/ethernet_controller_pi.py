import socket
import pickle
import os
import RPi.GPIO as GPIO
import time

# IP and port of the Raspberry Pi Zero
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

led = 18
servo1 = 16
servo2 = 22
GPIO.setmode(GPIO.BOARD) # for GPIO Numberng choose BCM, for pin numbering choose BOARD
GPIO.setup(led, GPIO.OUT)

GPIO.setup(servo1, GPIO.OUT)
p = GPIO.PWM(servo1, 100)

GPIO.setup(servo2, GPIO.OUT)
p2 = GPIO.PWM(servo2, 100)

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Accept a connection
conn, addr = s.accept()


# logic for controlling the game or robot
def control(controller_values):
    left_thumb_x, left_thumb_y = controller_values['left_thumb']
    right_thumb_x, right_thumb_y = controller_values['right_thumb']
    left_trigger, right_trigger = controller_values['triggers']
    buttons_pressed = controller_values['buttons']

    #print(f"Left Thumb: ({left_thumb_x}, {left_thumb_y})")

    if right_trigger > 0:
        p.start(50)
        print("right trigger")
    else:
        p.stop()
    
    if left_trigger > 0:
        p2.start(50)
        print("left trigger")
    else:
        p2.stop()

    # Performing an action based on button press
    if 'A' in buttons_pressed:
        if GPIO.input(led) == GPIO.LOW:
            print("LED ON")
            GPIO.output(led, GPIO.HIGH)  # Turn the LED ON
        else:
            print("LED OFF")
            GPIO.output(led, GPIO.LOW)   # Turn the LED OFF

        if 'B' in buttons_pressed:
            print("LED OFF")
            GPIO.output(led, GPIO.LOW)


while True:
    # Receive the data from the sender
    data = conn.recv(4096)

    if not data:
        break

    # Unpickle the received data
    controller_values = pickle.loads(data)

    # Process the received data
    # Add your processing logic here
    control(controller_values)

conn.close()
GPIO.cleanup()

