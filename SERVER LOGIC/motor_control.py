"""
BPMI Robotic Annular Pipe Sanitization System
File Name: motorControl.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: motor control
Verion: 1.0.0
Authors: Bennett, Gomez, Tiwari

Build Notes: first implementation?

Dependencies: None

References:

Additional Notes:

"""

speedleft = 0
speedright = 0

# FIXME: Not sure how to use pi gpio
import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the motor control
# Modify these values
AIN1 = 17
AIN2 = 18
BIN1 = 22
BIN2 = 23

# Initialize the GPIO pins
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# Function to control the left motor
def left_motor_control(speed, direction):
    if direction == "forward":
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)

# Function to control the right motor
def right_motor_control(speed, direction):
    if direction == "forward":
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)

# Function to stop both motors
def stop_motors():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    
# Function to control the motors based on the Xbox controller input
def control_motors(packet_number, gamepad):
    # Extract the necessary values from the gamepad input
    left_thumb_x = gamepad.sThumbLX
    right_trigger = gamepad.bRightTrigger

    # Convert the range of thumbstick and trigger values to the appropriate speed and turning values
    speed = int(right_trigger * 2.55)  # Scale the trigger value to a speed percentage (0-255)
    turn = int(left_thumb_x * 2.55)  # Scale the thumbstick value to a turning percentage (0-255)

    # Adjust the motor control based on the speed and turning values
    if speed > 0:
        left_motor_control(speed, "forward")
        right_motor_control(speed, "forward")
        if turn > 0:
            # Sharp left turn
            left_motor_control(turn, "backward")
            right_motor_control(turn, "forward")
        elif turn < 0:
            # Sharp right turn
            left_motor_control(-turn, "forward")
            right_motor_control(-turn, "backward")
    else:
        stop_motors()

# Main code to control the motors based on the Xbox controller input received over Ethernet
if __name__ == '__main__':
    try:
        while True:
            # TODO: Receive the controller input over Ethernet
            # TODO: Convert the data to packet_number and gamepad objects
            # TODO: Call the control_motors function with the received data
            pass
    except KeyboardInterrupt:
        stop_motors()
        GPIO.cleanup()
