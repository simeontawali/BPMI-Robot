#!/usr/bin/python3

"""
Control Program for Raspberry Pi Zero

This script listens for controller inputs over a network connection
and controls motors based on the received input values.

Requirements:
- RPi.GPIO library for Raspberry Pi GPIO control
- json library for handling JSON data
"""

# Import necessary modules and libraries
import socket
import pickle
import os
import RPi.GPIO as GPIO
import time
import math
import json

# IP and port of the Raspberry Pi Zero
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

# GPIO pin configuration
led = 6
pwm_left = 12
pwm_right = 13
freq = 50  # 100
dc_forward = 5
dc_backward = 10
dead: bool = True
GPIO.setmode(GPIO.BCM)  # for GPIO Numbering choose BCM, for pin numbering choose BOARD
GPIO.setup(led, GPIO.OUT)
GPIO.setup(pwm_left, GPIO.OUT)
p_l = GPIO.PWM(pwm_left, freq)
GPIO.setup(pwm_right, GPIO.OUT)
p_r = GPIO.PWM(pwm_right, freq)
p_l.start(0)
p_r.start(0)

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Accept a connection
conn, addr = s.accept()

# function to translate joystick x/y to differential drive
def joystickToDiff(x, y, minJoystick, maxJoystick, minSpeed, maxSpeed):
    # Header for the method
    """
    Translate joystick x/y values to differential drive outputs.

    Args:
    x (float): Joystick x-coordinate value.
    y (float): Joystick y-coordinate value.
    minJoystick (float): Minimum joystick value.
    maxJoystick (float): Maximum joystick value.
    minSpeed (int): Minimum motor speed.
    maxSpeed (int): Maximum motor speed.

    Returns:
    tuple: A tuple containing right and left motor speeds.
    """
    if x == 0 and y == 0:
        return (0, 0)

    # First Compute the angle in deg
    # First hypotenuse
    z = math.sqrt(x * x + y * y)

    # angle in radians
    rad = math.acos(math.fabs(x) / z)

    # and in degrees
    angle = rad * 180 / math.pi

    # Now angle indicates the measure of turn
    # Along a straight line, with an angle o, the turn co-efficient is same
    # this applies for angles between 0-90, with angle 0 the coeff is -1
    # with angle 45, the co-efficient is 0 and with angle 90, it is 1
    tcoeff = -1 + (angle / 90) * 2
    turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
    turn = round(turn * 100, 0) / 100

    # And max of y or x is the movement
    mov = max(math.fabs(y), math.fabs(x))

    # First and third quadrant
    if (x >= 0 and y >= 0) or (x < 0 and y < 0):
        rawLeft = mov
        rawRight = turn
    else:
        rawRight = mov
        rawLeft = turn

    # Reverse polarity
    if y < 0:
        rawLeft = 0 - rawLeft
        rawRight = 0 - rawRight

    # Map the values onto the defined range
    rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
    leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

    return (rightOut, leftOut)

# Helper function for joystickToDiff which maps a variable to a new range
def map(v, in_min, in_max, out_min, out_max):
    # Header for the method
    """
    Map a value from one range to another.

    Args:
    v (float): Input value to be mapped.
    in_min (float): Minimum input value.
    in_max (float): Maximum input value.
    out_min (float): Minimum output value.
    out_max (float): Maximum output value.

    Returns:
    float: Mapped value in the output range.
    """
    # Check that the value is at least in_min
    if v < in_min:
        v = in_min
    # Check that the value is at most in_max
    if v > in_max:
        v = in_max
    return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Logic for controlling the game or robot
prev_buttons_state = dict()
prev_right_trigger_state = 0
prev_left_trigger_state = 0
prev_left_thumb_state = (0, 0)
prev_right_thumb_state = (0, 0)
def control(controller_values):
    # Header for the method
    """
    Control motors based on received controller values.

    Args:
    controller_values (dict): Dictionary containing controller values.
    """
    global prev_buttons_state, prev_right_trigger_state, prev_left_trigger_state, prev_left_thumb_state, prev_right_thumb_state
    left_thumb = controller_values.get('LeftThumb', (0, 0))
    left_thumb_x, left_thumb_y = left_thumb
    right_thumb = controller_values.get('RightThumb', (0, 0))
    right_thumb_x, right_thumb_y = right_thumb
    left_trigger, right_trigger = controller_values.get('Triggers', (0, 0))
    A, B, X, Y = controller_values.get('Buttons', (False, False, False, False))
    LeftShoulder, RightShoulder = controller_values.get('Shoulders', (False, False))
    DPadUp, DPadDown, DpadLeft, DpadRight = controller_values.get('DPad', (False, False, False, False))
    Start, Back = controller_values.get('Other', (False, False))

    global dead
    threshold = 0.1  # deadzone threshold
    if (dead):
        left_thumb_x = deadzone(left_thumb_x, threshold)
        left_thumb_y = deadzone(left_thumb_y, threshold)
        right_thumb_x = deadzone(left_thumb_x, threshold)
        right_thumb_y = deadzone(left_thumb_y, threshold)

    # Convert to differential drive
    (L, R) = joystickToDiff(left_thumb_x, left_thumb_y, -1, 1, -100, 100)
    L = L + 100
    R = R + 100

    # Deadzone on/off

    duty_cycle_l = 5 + float(L) / 200 * 5
    duty_cycle_r = 5 + float(200 - R) / 200 * 5

    if (dead):
        if (duty_cycle_l >= 7.4 and duty_cycle_l <= 7.6):
            duty_cycle_l = 0
        if (duty_cycle_r >= 7.4 and duty_cycle_r <= 7.6):
            duty_cycle_r = 0

    # Triggers
    if right_trigger > 0 and prev_right_trigger_state == 0:
        p_l.ChangeDutyCycle(10)
        p_r.ChangeDutyCycle(5)
        print("right trigger")
    elif right_trigger == 0 and prev_right_trigger_state > 0:
        p_r.ChangeDutyCycle(0)
        p_l.ChangeDutyCycle(0)

    if left_trigger > 0 and prev_left_trigger_state == 0:
        p_l.ChangeDutyCycle(5)
        p_r.ChangeDutyCycle(10)
        print("left trigger")
    elif left_trigger == 0 and prev_right_trigger_state > 0:
        p_l.ChangeDutyCycle(0)
        p_r.ChangeDutyCycle(0)

    # Handling thumbs
    if (left_thumb_x, left_thumb_y) != prev_left_thumb_state:
        # Handle left thumbstick movement
        p_l.ChangeDutyCycle(duty_cycle_l)
        p_r.ChangeDutyCycle(duty_cycle_r)

    if (right_thumb_x, right_thumb_y) != prev_right_thumb_state:
        # Handle right thumbstick movement
        pass

    # Update the previous state
    prev_right_trigger_state = right_trigger
    prev_left_trigger_state = left_trigger
    prev_left_thumb_state = (left_thumb_x, left_thumb_y)
    prev_right_thumb_state = (right_thumb_x, right_thumb_y)

def deadzone(value, threshold):
    # Header for the method
    """
    Apply deadzone to joystick values.

    Args:
    value (float): Joystick value to be deadzoned.
    threshold (float): Deadzone threshold.

    Returns:
    float: Deadzoned joystick value.
    """
    if abs(value) < threshold:
        return 0
    elif value > 0:
        return (value - threshold) / (1 - threshold)
    else:
        return (value + threshold) / (1 - threshold)

# Main loop for receiving controller inputs and controlling the motors
while True:
    # Receive the data from the sender
    data = conn.recv(4096)

    if not data:
        break

    # Decode the bytes to a string then load string as JSON
    controller_values_str = data.decode('utf-8')
    controller_values = json.loads(controller_values_str)

    # Process the received data
    control(controller_values)

# Close the connection and clean up GPIO
conn.close()
GPIO.cleanup()
