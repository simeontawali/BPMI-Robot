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
from module import Module
import time

class RobotControl:
    def __init__(self, led_wf_pin, led_wu_pin, led_uv_pin, pwm_left_pin, pwm_right_pin):
        self.led_wf_pin = led_wf_pin
        self.led_wu_pin = led_wu_pin
        self.led_uv_pin = led_uv_pin
        self.pwm_left_pin = pwm_left_pin
        self.pwm_right_pin = pwm_right_pin
        self.motor_stop_pin = 19
        self.freq = 50
        self.setup_gpio()
        self.mod = Module()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_wf_pin, GPIO.OUT)
        GPIO.setup(self.led_wu_pin,GPIO.OUT)
        GPIO.setup(self.led_uv_pin,GPIO.OUT)
        GPIO.setup(self.pwm_left_pin, GPIO.OUT)
        GPIO.setup(self.pwm_right_pin, GPIO.OUT)
        GPIO.setup(self.motor_stop_pin,GPIO.OUT)
        self.p_l = GPIO.PWM(self.pwm_left_pin, self.freq)
        self.p_r = GPIO.PWM(self.pwm_right_pin, self.freq)
        self.p_l.start(0)
        self.p_r.start(0)

    def update_motors(self, duty_cycle_l, duty_cycle_r, stop):
        # Adjust PWM based on duty cycle
        self.p_l.ChangeDutyCycle(duty_cycle_l)
        self.p_r.ChangeDutyCycle(duty_cycle_r)
        if (not self.motors_stopped()) and stop:
            self.stop_motors_toggle()
        elif self.motors_stopped() and (not stop):
            self.stop_motors_toggle()

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

    def stop_motors_toggle(self):
        if GPIO.input(self.motor_stop_pin) == GPIO.LOW:
            print("MOTORS STOPPED")
            GPIO.output(self.motor_stop_pin, GPIO.HIGH)
        else:
            print("MOTORS CONTINUING")
            GPIO.output(self.motor_stop_pin, GPIO.LOW) 

    def motors_stopped(self):
        return GPIO.input(self.motor_stop_pin) == GPIO.HIGH

    def update_control(self, controller: Controller):
        """Preform Actions based on controller input"""

        if (controller.state_change('LeftThumbX') or controller.state_change('LeftThumbY')):
            X,Y,stop = controller.get_duty_cycle()
            self.update_motors(X,Y,stop)

        if controller.get_button('A') and controller.state_change('A'):
            if GPIO.input(self.led_wu_pin) == GPIO.LOW:
                print("UNDERSIDE WHITE LED ON")
                GPIO.output(self.led_wu_pin, GPIO.HIGH)  # Turn the LED ON
            else:
                print("UNDERSIDE WHITE LED OFF")
                GPIO.output(self.led_wu_pin, GPIO.LOW)  # Turn the LED OFF
        if controller.get_button('B') and controller.state_change('B'):
            if GPIO.input(self.led_wf_pin) == GPIO.LOW:
                print("FORWARD WHITE LED ON")
                GPIO.output(self.led_wf_pin, GPIO.HIGH)  # Turn the LED ON
            else:
                print("FORWARD WHITE LED OFF")
                GPIO.output(self.led_wf_pin, GPIO.LOW)  # Turn the LED OFF
        if controller.get_button('X') and controller.state_change('X'):
            self.stop()
        if controller.get_button('Y') and controller.state_change('Y'):
            if GPIO.input(self.led_uv_pin) == GPIO.LOW:
                print("UV LED ON")
                GPIO.output(self.led_uv_pin, GPIO.HIGH)  # Turn the LED ON
            else:
                print("UV LED OFF")
                GPIO.output(self.led_uv_pin, GPIO.LOW)  # Turn the LED OFF
        if controller.get_button('LeftThumbX') > 0.1 and controller.state_change('LeftThumbX'):
            pass
        if controller.get_button('LeftThumbY') > 0.1 and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbX') and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbY') and controller.state_change('RightThumbY'):
            pass
        if controller.get_button('DPadUp') and controller.state_change('DPadUp'):
            # self.mod.incr_l()
            # self.mod.update()
            self.mod.actuator_forward()
            time.sleep(1)
            self.mod.actuator_off()
        if controller.get_button('DPadDown') and controller.state_change('DPadDown'):
            # self.mod.decr_l()
            # self.mod.update()
            self.mod.actuator_forward()
            time.sleep(1)
            self.mod.actuator_off()
        if controller.get_button('DPadLeft') and controller.state_change('DPadLeft'):
            # self.mod.decr_r()
            # self.mod.update()
            pass
        if controller.get_button('DPadRight') and controller.state_change('DPadRight'):
            # self.mod.incr_r()
            # self.mod.update()
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
