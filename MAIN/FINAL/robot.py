"""
BPMI Robotic Annular Pipe Sanitization System
File Name: Robot.py
Date Created: 3/5/2024 SAT
Date Last Modified: 3/5/2024 SAT
Description: Robot class
Verion: 1.0.1
Authors: Tiwari

Build Notes: First Finished Implementation

Dependencies: None

References:

Additional Notes:

"""
import RPi.GPIO as GPIO

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
        pass

    def cleanup(self):
        GPIO.cleanup()
