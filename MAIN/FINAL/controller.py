"""
BPMI Robotic Annular Pipe Sanitization System
File Name: controller.py
Date Created: 3/5/2024 TSA
Date Last Modified: 3/5/2024 TSA
Description: Controller class
Verion: 1.0.1
Authors: TSA

Build Notes: First Finished Implementation

Dependencies: None

References:
JoystickToDiff
https://www.instructables.com/Joystick-to-Differential-Drive-Python/

Additional Notes:

"""
import math
import copy

class Controller:
    
    def __init__(self):
        self.state = {
            'Buttons': {
                'A': False,  # Button A
                'B': False,  # Button B
                'X': False,  # Button X
                'Y': False,  # Button Y
            },
            'Triggers': {
                'Left': 0.0,  # Left Trigger pressure (0-100)
                'Right': 0.0  # Right Trigger pressure (0-100)
            },
            'Shoulders': {
                'LeftShoulder': False, # Left Shoulder Button
                'RightShoulder': False # Right Shoulder Button
            },
            'Thumbsticks': {
                'LeftThumb': (0.0, 0.0),  # Left Thumbstick position (X, Y)
                'RightThumb': (0.0, 0.0)  # Right Thumbstick position (X, Y)
            },
            'DPad': {
                'Up': False,  # D-Pad Up
                'Down': False,  # D-Pad Down
                'Left': False,  # D-Pad Left
                'Right': False  # D-Pad Right
            },
            'Other': {
                'Start': False,  # Start
                'Back': False  # Back Button
            }
        }
        self.prev_state = copy.deepcopy(self.state)
        self.prev_controller_values = None
        self.deadzone_value = True
        self.thumbstick_deadzone = 0.15
        self.motor_deadzone = 0.04

    def update(self, state, new_values):
        try:
            # Update Thumbsticks
            state['Thumbsticks']['LeftThumb'] = tuple(new_values['LeftThumb'])
            state['Thumbsticks']['RightThumb'] = tuple(new_values['RightThumb'])

            # Update Triggers
            state['Triggers']['Left'] = new_values['Triggers'][0]
            state['Triggers']['Right'] = new_values['Triggers'][1]

            # Update Buttons, Shoulders, DPad, and Other using a mapping to convert 1/0 to True/False
            button_names = ['A', 'B', 'X', 'Y']
            shoulder_names = ['LeftShoulder', 'RightShoulder']
            dpad_names = ['Up', 'Down', 'Left', 'Right']
            other_names = ['Start', 'Back']

            for i, name in enumerate(button_names):
                state['Buttons'][name] = bool(new_values['Buttons'][i])

            for i, name in enumerate(shoulder_names):
                state['Shoulders'][name] = bool(new_values['Shoulders'][i])

            for i, name in enumerate(dpad_names):
                state['DPad'][name] = bool(new_values['DPad'][i])

            for i, name in enumerate(other_names):
                state['Other'][name] = bool(new_values['Other'][i])
        except Exception as e:
            print("Error processing controller values:")
            print(e)
            print(new_values)

    def print_values(self):
        """Prints the current state of the controller."""
        print("Controller State:")
        for category, details in self.state.items():
            print(f"  {category}:")
            for key, value in details.items():
                print(f"    {key}: {value}")

    def update_state(self, new_values):
        self.prev_state = copy.deepcopy(self.state)
        #self.update_prev_state(self.state)
        self.update(self.state,new_values)

    def update_prev_state(self,prev_controller_values):
        self.update(self.prev_state,prev_controller_values)

    def state_change(self, input_name):
        """Returns true if current state has changed from prev state, else returns false"""
        return self.get_input_value(self.state,input_name) != self.get_input_value(self.prev_state,input_name)
        #return True

    def get_state(self):
        return self.state
    
    def get_button(self,input_name):
        return self.get_input_value(self.state,input_name)

    def get_input_value(self, state, input_name):
        """Returns the value of a given input (button, trigger, thumbstick, DPad, or shoulder)."""
        # For Triggers
        if input_name in ['LeftTrigger', 'RightTrigger']:
            trigger_key = input_name[:-7]  # Remove "Trigger" from the end to match 'Left' or 'Right'
            return state['Triggers'][trigger_key]

        # For Shoulders
        elif input_name in state['Shoulders']:
            return state['Shoulders'][input_name]

        # For DPad
        elif input_name.startswith('DPad'):
            dpad_direction = input_name[4:]  # Get direction part like 'Left', 'Right', etc.
            if dpad_direction in state['DPad']:
                return state['DPad'][dpad_direction]

        # For Buttons and Other inputs (direct match)
        elif input_name in state['Buttons']:
            return state['Buttons'][input_name]
        elif input_name in state['Other']:
            return state['Other'][input_name]

        # For Thumbsticks (expecting something like "LeftThumbX" or "RightThumbY")
        elif 'Thumb' in input_name:
            thumbstick, axis = input_name[:-1], input_name[-1].upper()  # Split into thumbstick and axis
            if thumbstick in state['Thumbsticks'] and axis in ['X', 'Y']:
                axis_index = 0 if axis == 'X' else 1  # Convert axis into index (0 for X, 1 for Y)
                if (self.deadzone_value):
                    return self.deadzone(state['Thumbsticks'][thumbstick][axis_index],self.thumbstick_deadzone)
                return state['Thumbsticks'][thumbstick][axis_index]

        # If input_name does not match any known inputs or patterns
        return "Unknown input"
    @staticmethod
    def deadzone(value, threshold):
        if abs(value) < threshold:
            return 0
        elif value > 0:
            return (value - threshold) / (1 - threshold)
        else:
            return (value + threshold) / (1 - threshold)
        
    def set_deadzone(self,deadzone_value: bool):
        print(f"Deadzone is {'active' if deadzone_value else 'not active'}\n")
        self.deadzone_value = deadzone_value

    def get_duty_cycle(self):
        offsetL = -0.4
        offsetR = -0.4
        min_joystick, max_joystick = -1, 1  # joystick ranges
        min_speed, max_speed = -100, 100   # speed ranges to be mapped to PWM
        (X,Y) = self.state['Thumbsticks']['LeftThumb']
        print("\r")
        print(f"controller: {X},{Y}")
        (left_speed,right_speed) = self.joystick_to_diff(X,Y,min_joystick,max_joystick,min_speed,max_speed)
        print(f"joystick_to_diff: {left_speed},{right_speed}")
        left_duty_cycle = self.map_val(left_speed, min_speed, max_speed, 4.5+offsetL,10.5+offsetL)  # range, adjust as needed
        right_duty_cycle = self.map_val(right_speed, min_speed, max_speed, 4.5+offsetR, 10.5+offsetR)  # range, adjust as needed
        stop_motors = False
        if (self.deadzone_value):
             if (left_duty_cycle >= (7.5+offsetL - 3*self.motor_deadzone) and left_duty_cycle <= (7.5+offsetL + 3*self.motor_deadzone)):
                 left_duty_cycle = 7.5+offsetL
                 stop_motors = True
             if (right_duty_cycle >= (7.5+offsetR - 3*self.motor_deadzone) and right_duty_cycle <= (7.5+offsetR + 3*self.motor_deadzone)):
                 right_duty_cycle = 7.5+offsetR
                 stop_motors = True
        print(f"duty cycles: {left_duty_cycle},{right_duty_cycle}")
        return left_duty_cycle,right_duty_cycle,stop_motors

    @staticmethod
    def map_val(v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
    def joystick_to_diff(self,x, y, min_joystick, max_joystick, min_speed, max_speed):
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
        rightOut = self.map_val(rawRight, min_joystick, max_joystick, min_speed, max_speed)
        leftOut = self.map_val(rawLeft, min_joystick, max_joystick, min_speed, max_speed)
        return (leftOut, rightOut)
