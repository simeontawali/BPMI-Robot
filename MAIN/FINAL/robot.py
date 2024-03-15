"""
BPMI Robotic Annular Pipe Sanitization System
File Name: Robot.py
Date Created: 3/5/2024 TSA
Date Last Modified: 3/5/2024 TSA
Description: Robot class
Verion: 1.0.1
Authors: TSA

Build Notes: First Finished Implementation

Dependencies: None

References:

Additional Notes:

"""
import RPi.GPIO as GPIO
from controller import Controller

class RobotControl:
    def __init__(self, led_pin, pwm_left_pin, pwm_right_pin, freq):
        self.led_pin = led_pin
        self.pwm_left_pin = pwm_left_pin
        self.pwm_right_pin = pwm_right_pin
        self.freq = freq
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.pwm_left_pin, GPIO.OUT)
        GPIO.setup(self.pwm_right_pin, GPIO.OUT)
        self.p_l = GPIO.PWM(self.pwm_left_pin, self.freq)
        self.p_r = GPIO.PWM(self.pwm_right_pin, self.freq)
        self.p_l.start(0)
        self.p_r.start(0)

    def update_motors(self, duty_cycle_l, duty_cycle_r):
        # Adjust PWM based on duty cycle
        self.p_l.ChangeDutyCycle(duty_cycle_l)
        self.p_r.ChangeDutyCycle(duty_cycle_r)

    def start(self):
        self.p_l.start(0)
        self.p_l.start(0)
        
    def stop(self):
        self.p_l.stop()
        self.p_r.stop()

    def forward(self, distance):
        pass
    def backward(self, distance):
        pass
    def turn_left(self):
        pass
    def turn_right(self):
        pass
    def turn_around(self):
        pass

    def update_control(self, controller: Controller):
        """Preform Actions based on controller input"""
        if controller.get_button('A') and controller.state_change('A'):
            pass
        if controller.get_button('B') and controller.state_change('B'):
            pass
        if controller.get_button('X') and controller.state_change('X'):
            pass
        if controller.get_button('Y') and controller.state_change('Y'):
            pass
        if controller.get_button('LeftThumbX') > 0.1 and controller.state_change('LeftThumbX'):
            pass
        if controller.get_button('LeftThumbY') > 0.1 and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbX') and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbY') and controller.state_change('RightThumbY'):
            pass
        if controller.get_button('DPadUp') and controller.state_change('DPadUp'):
            pass
        if controller.get_button('DPadDown') and controller.state_change('DPadDown'):
            pass
        if controller.get_button('DPadLeft') and controller.state_change('DPadLeft'):
            pass
        if controller.get_button('DPadRight') and controller.state_change('DPadRight'):
            pass
        if controller.get_button('LeftTrigger') > 0.1 and controller.state_change('LeftTrigger'):
            pass
        if controller.get_button('RightTrigger') > 0.1 and controller.state_change('RightTrigger'):
            pass
        if controller.get_button('LeftShoulder') and controller.state_change('LeftShoulder'):
            pass
        if controller.get_button('RightShoulder') and controller.state_change('RightShoulder'):
            pass


    def cleanup(self):
        GPIO.cleanup()
