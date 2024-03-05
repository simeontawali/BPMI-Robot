import socket
import pickle
import os
import RPi.GPIO as GPIO
import time
import math

# IP and port of the Raspberry Pi Zero
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

led = 6
pwm_left = 12
pwm_right = 13
freq = 50 # 100
dc_forward = 5
dc_backward = 10
dead: bool = True
GPIO.setmode(GPIO.BCM) # for GPIO Numbering choose BCM, for pin numbering choose BOARD
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

	# minJoystick, maxJoystick, minSpeed, maxSpeed
	# Map the values onto the defined rang
	rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
	leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

	return (rightOut, leftOut)

# helper function for joystickToDiff which maps a variable to a new range
def map(v, in_min, in_max, out_min, out_max):
	# Check that the value is at least in_min
	if v < in_min:
		v = in_min
	# Check that the value is at most in_max
	if v > in_max:
		v = in_max
	return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# logic for controlling the game or robot
prev_buttons_state = set()
prev_right_trigger_state = 0
prev_left_trigger_state = 0
prev_left_thumb_state = (0, 0)
prev_right_thumb_state = (0, 0)
def control(controller_values):
    global prev_buttons_state, prev_right_trigger_state, prev_left_trigger_state, prev_left_thumb_state, prev_right_thumb_state
    left_thumb_x, left_thumb_y = controller_values['left_thumb']
    right_thumb_x, right_thumb_y = controller_values['right_thumb']
    left_trigger, right_trigger = controller_values['triggers']
    buttons_pressed = controller_values['buttons']
    global dead
    threshold = 0.1 # deadzone threshold
    if (dead):
         left_thumb_x = deadzone(left_thumb_x,threshold)
         left_thumb_y = deadzone(left_thumb_y,threshold)
         right_thumb_x = deadzone(left_thumb_x,threshold)
         right_thumb_y = deadzone(left_thumb_y,threshold)

    # convert to differential drive
    print('x,y is ' + str(left_thumb_x) + ' ' + str(left_thumb_y)) 
    (L,R) = joystickToDiff(left_thumb_x,left_thumb_y,-1,1,-100,100)
    L = L + 100
    R = R + 100
    # deadzone on/off
    
    # print(f"Left Thumb: ({left_thumb_x}, {left_thumb_y})")
    duty_cycle_l = 5 + float(L)/200*5
    duty_cycle_r = 5 + float(200-R)/200*5

    if (dead):
        if (duty_cycle_l >= 7.4 and duty_cycle_l <= 7.6):
            duty_cycle_l = 0
        if (duty_cycle_r >= 7.4 and duty_cycle_r <= 7.6):
            duty_cycle_r = 0

    print('L: ' + str(duty_cycle_l) + ' ' + str(L))
    print('R: ' + str(duty_cycle_r) + ' ' + str(R))

    # triggers
    if right_trigger > 0 and prev_right_trigger_state == 0:
        p_l.ChangeDutyCycle(10)
        p_r.ChangeDutyCycle(5)
        #print("right trigger")
    elif right_trigger == 0 and prev_right_trigger_state > 0:
        p_r.ChangeDutyCycle(0)
        p_l.ChangeDutyCycle(0)
    
    if left_trigger > 0 and prev_left_trigger_state == 0:
        p_l.ChangeDutyCycle(5)
        p_r.ChangeDutyCycle(10)
        #print("left trigger")
    elif left_trigger == 0 and prev_right_trigger_state > 0:
        p_l.ChangeDutyCycle(0)
        p_r.ChangeDutyCycle(0)

    # Handling buttons
    for button in buttons_pressed:
        if button not in prev_buttons_state:
            if 'A' in buttons_pressed:
                if GPIO.input(led) == GPIO.LOW:
                    print("LED ON")
                    GPIO.output(led, GPIO.HIGH)  # Turn the LED ON
                else:
                    print("LED OFF")
                    GPIO.output(led, GPIO.LOW)  # Turn the LED OFF
            if 'B' in buttons_pressed:
                dead = not dead
                print("Deadzone mode: ", dead)

    # Handling thumbs
    if (left_thumb_x, left_thumb_y) != prev_left_thumb_state:
        # Handle left thumbstick movement
        p_l.ChangeDutyCycle(duty_cycle_l)
        p_r.ChangeDutyCycle(duty_cycle_r)
        #print(f"Left thumbstick: ({left_thumb_x}, {left_thumb_y})")

    if (right_thumb_x, right_thumb_y) != prev_right_thumb_state:
        # Handle right thumbstick movement
        #print(f"Right thumbstick: ({right_thumb_x}, {right_thumb_y})")
        pass

    # Update the prev state
    prev_buttons_state = set(buttons_pressed)
    prev_right_trigger_state = right_trigger
    prev_left_trigger_state = left_trigger
    prev_left_thumb_state = (left_thumb_x, left_thumb_y)
    prev_right_thumb_state = (right_thumb_x, right_thumb_y)

def deadzone(value, threshold):
    if abs(value) < threshold:
        return 0
    elif value > 0:
        return (value - threshold) / (1 - threshold)
    else:
        return (value + threshold) / (1 - threshold)
     

def movement(left_thumb_x, left_thumb_y):
    (L,R) = joystickToDiff(left_thumb_x,left_thumb_y,-1,1,-100,100)
    L = L + 100
    R = R + 100
    # deadzone on/off
    if (dead):
        if (L >= 95 and L <= 105):
            duty_cycle_l = 0
        if (R >= 95 and R <= 105):
            duty_cycle_r = 0

    # print(f"Left Thumb: ({left_thumb_x}, {left_thumb_y})")
    duty_cycle_l = 5 + float(200-R)/200*5
    duty_cycle_r = 5 + float(L)/200*5
    TL = 5 + float(200-R)/200*5
    TR = 5 + float(L)/200*5
    p_l.ChangeDutyCycle(duty_cycle_l)
    p_r.ChangeDutyCycle(duty_cycle_r)
     

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

