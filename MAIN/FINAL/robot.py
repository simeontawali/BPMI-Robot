"""
BPMI Robotic Annular Pipe Sanitization System
File Name: Robot.py
Date Created: 3/5/2024 TSA
Date Last Modified: 3/5/2024 TSA
Description: Robot class
Version: 1.0.1
Authors: TSA

Build Notes: First Finished Implementation

Dependencies: None

References:

Additional Notes:

"""
import RPi.GPIO as GPIO
import os
from controller import Controller
from module import Module
import time

class RobotControl:
    def __init__(self):
        self.led_wf_pin = 20
        self.led_wu_pin = 21
        self.led_uv_pin = 18

        self.motor_stop_pin = 15
        self.pwm_left_pin_path = '/sys/class/pwm/pwmchip0/pwm0'
        self.pwm_right_pin_path = '/sys/class/pwm/pwmchip0/pwm1'
        self.pwm_export_path = '/sys/class/pwm/pwmchip0/export'
        self.freq = 50 # frequency in Hz
        self.period = 1/self.freq * 1e9 # period in nano seconds
        self.speed = 0
        self.driving = 'S'

        self.mod = Module()
        self.scrubber_pin = 23

        self.setup_gpio()

        self.data = {
            'Switches': {
                'FW': False,  # Front white
                'FUV': False,  # Front UV
                'BW': False,  # Bottom White
                'SR': False,  # Scrubber
                },
            'Temp': {
                'CPUTemp': 0.0,
                'GPUTemp': 0.0,
                },
            'DriveSpeed': {
                'Value': 0.0, 
                'Direction': 'S',
                },
            'Connections': {
                'Controller': False,  # Controller task
                'Camera': False,  # Camera task
                }
            }

    def setup_gpio(self):
        print('Initializing GPIO and PWMs')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_wf_pin, GPIO.OUT)
        GPIO.setup(self.led_wu_pin,GPIO.OUT)
        GPIO.setup(self.led_uv_pin,GPIO.OUT)
        GPIO.setup(self.motor_stop_pin,GPIO.OUT)
        GPIO.setup(self.scrubber_pin,GPIO.OUT)

        duty_cycle = 7.5 # initial duty cycle of 7.5% (arbitrary since relay will be stopping the motors)
        duty_cycle_period = duty_cycle/100*self.period
        GPIO.output(self.motor_stop_pin, GPIO.LOW) # start relay in stopped position

        os.system(f'echo 1 > {self.pwm_export_path}')
        os.system(f'echo 0 > {self.pwm_export_path}')
        os.system(f'echo {round(self.period)} > {self.pwm_left_pin_path}/period')
        os.system(f'echo {round(self.period)} > {self.pwm_right_pin_path}/period')
        os.system(f'echo {round(duty_cycle_period)}> {self.pwm_left_pin_path}/duty_cycle')
        os.system(f'echo {round(duty_cycle_period)} > {self.pwm_right_pin_path}/duty_cycle')
        os.system(f'echo 1 > {self.pwm_left_pin_path}/enable')
        os.system(f'echo 1 > {self.pwm_right_pin_path}/enable')

        print('Finished initializing GPIO and PWM')

    def update_motors(self, duty_cycle_l, duty_cycle_r, stop):
        duty_cycle_period_l = duty_cycle_l/100*self.period
        duty_cycle_period_r = duty_cycle_r/100*self.period

        os.system(f'echo {round(duty_cycle_period_l)} > {self.pwm_left_pin_path}/duty_cycle')
        os.system(f'echo {round(duty_cycle_period_r)} > {self.pwm_right_pin_path}/duty_cycle')

        if (not self.motors_stopped()) and stop:
            self.stop_motors_toggle()
        elif self.motors_stopped() and (not stop):
            self.stop_motors_toggle()

    def stop_motors_toggle(self):
        if GPIO.input(self.motor_stop_pin) == GPIO.LOW:
            GPIO.output(self.motor_stop_pin, GPIO.HIGH)
        else:
            GPIO.output(self.motor_stop_pin, GPIO.LOW) 

    def motors_stopped(self):
        return GPIO.input(self.motor_stop_pin) == GPIO.LOW

    def update_control(self, controller: Controller):
        """Preform Actions based on controller input"""
        scrub = False
        if (controller.state_change('LeftThumbX') or controller.state_change('LeftThumbY')):
            X,Y,stop = controller.get_duty_cycle()
            self.update_motors(X,Y,stop)

        if (controller.state_change('LeftThumbX') or controller.state_change('LeftThumbY')):
            pass
        if controller.get_button('A') and controller.state_change('A'): # underside white LED control
            if GPIO.input(self.led_wu_pin) == GPIO.LOW:
                print("UNDERSIDE WHITE LED ON")
                GPIO.output(self.led_wu_pin, GPIO.HIGH)  # Turn the LED ON
                self.data['Switches']['UW'] = True
            else:
                print("UNDERSIDE WHITE LED OFF")
                GPIO.output(self.led_wu_pin, GPIO.LOW)  # Turn the LED OFF
                self.data['Switches']['UW'] = False
        if controller.get_button('B') and controller.state_change('B'): # forward white LED control
            if GPIO.input(self.led_wf_pin) == GPIO.LOW:
                print("FORWARD WHITE LED ON")
                GPIO.output(self.led_wf_pin, GPIO.HIGH)  # Turn the LED ON
                self.data['Switches']['FW'] = True
            else:
                print("FORWARD WHITE LED OFF")
                GPIO.output(self.led_wf_pin, GPIO.LOW)  # Turn the LED OFF
                self.data['Switches']['FW'] = False
        if controller.get_button('X') and controller.state_change('X'): # tape module scrubber control
            if GPIO.input(self.scrubber_pin) == GPIO.LOW:
                print("module scrubber ON")
                GPIO.output(self.scrubber_pin, GPIO.HIGH)  # Turn the scrubber ON
                self.data['Switches']['SR'] = True
                self.mod.actuator_off()
            else:
                print("module scrubber OFF")
                self.data['Switches']['SR'] = False
                GPIO.output(self.scrubber_pin, GPIO.LOW)  # Turn the scrubber OFF
        if controller.get_button('Y') and controller.state_change('Y'): # UV LED control
            if GPIO.input(self.led_uv_pin) == GPIO.LOW:
                print("UV LED ON")
                GPIO.output(self.led_uv_pin, GPIO.HIGH)  # Turn the LED ON
                self.data['Switches']['UV'] = True
            else:
                print("UV LED OFF")
                GPIO.output(self.led_uv_pin, GPIO.LOW)  # Turn the LED OFF
                self.data['Switches']['UV'] = False
        if controller.get_button('LeftThumbX') > 0.1 and controller.state_change('LeftThumbX'):
            pass
        if controller.get_button('LeftThumbY') > 0.1 and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbX') > 0.5 and controller.state_change('RightThumbX'):
            pass
        if controller.get_button('RightThumbY') > 0.5 and controller.state_change('RightThumbY'):
            pass
        if controller.get_button('DPadUp') and controller.state_change('DPadUp'): # drive motor forward
            L,R,stop = controller.get_duty_cycle(self.speed,'F')
            self.driving = 'F'
            self.data['DriveSpeed']['Direction'] = 'F'
            print('Moving forward')
            self.update_motors(L,R,stop)
        elif controller.state_change('DPadUp'):
            L,R,stop = controller.get_duty_cycle(self.speed,'S')
            self.driving = 'S'
            self.data['DriveSpeed']['Direction'] = 'S'
            print('Stopping')
            self.update_motors(L,R,stop)
        if controller.get_button('DPadDown') and controller.state_change('DPadDown'): # drive motor backward
            L,R,stop = controller.get_duty_cycle(self.speed,'B')
            self.driving = 'B'
            self.data['DriveSpeed']['Direction'] = 'B'
            print('Moving backward')
            self.update_motors(L,R,stop)
        elif controller.state_change('DPadDown'):
            L,R,stop = controller.get_duty_cycle(self.speed,'S')
            self.data['DriveSpeed']['Direction'] = 'S'
            self.driving = 'S'
            print('Stopping')
            self.update_motors(L,R,stop)
        if controller.get_button('DPadLeft') and controller.state_change('DPadLeft'): # drive motor left
            L,R,stop = controller.get_duty_cycle(self.speed,'L')
            self.driving = 'L'
            self.data['DriveSpeed']['Direction'] = 'L'
            print('Turing left')
            self.update_motors(L,R,stop)
        elif controller.state_change('DPadLeft'):
            L,R,stop = controller.get_duty_cycle(self.speed,'S')
            self.driving = 'S'
            self.data['DriveSpeed']['Direction'] = 'S'
            print('Stopping')
            self.update_motors(L,R,stop)
        if controller.get_button('DPadRight') and controller.state_change('DPadRight'): # drive motor right
            L,R,stop = controller.get_duty_cycle(self.speed,'R')
            self.driving = 'R'
            self.data['DriveSpeed']['Direction'] = 'R'
            print('Turing right')
            self.update_motors(L,R,stop)
        elif controller.state_change('DPadRight'):
            L,R,stop = controller.get_duty_cycle(self.speed,'S')
            self.driving = 'S'
            self.data['DriveSpeed']['Direction'] = 'S'
            print('Stopping')
            self.update_motors(L,R,stop)
        if controller.get_button('LeftTrigger') > 0.1 and controller.state_change('LeftTrigger'): # tape module actuator control
            print('actuator forward')
            self.mod.actuator_forward()
            GPIO.output(self.scrubber_pin, GPIO.LOW)  # Turn the scrubber OFF, they should not be on at the same time            
        elif controller.state_change('LeftTrigger'):
            self.mod.actuator_off()
        if controller.get_button('RightTrigger') > 0.1 and controller.state_change('RightTrigger'): # motor speed control
            if self.speed < 100:
                self.speed = self.speed + 5
                if self.driving != 'S':
                    L,R,stop = controller.get_duty_cycle(self.speed,self.driving)
                    self.update_motors(L,R,stop)
            self.data['DriveSpeed']['Value'] = self.speed
            print(f"drive speed: {self.speed}")
        if controller.get_button('LeftShoulder') and controller.state_change('LeftShoulder'): # tape module actuator control
            print('actuator backward')
            self.mod.actuator_backward()
            GPIO.output(self.scrubber_pin, GPIO.LOW)  # Turn the scrubber OFF, they should not be on at the same time 
        elif controller.state_change('LeftShoulder'):
            self.mod.actuator_off()
        if controller.get_button('RightShoulder') and controller.state_change('RightShoulder'): # motor speed control
            if self.speed > 0:
                self.speed = self.speed - 5
                if self.driving != 'S':
                    L,R,stop = controller.get_duty_cycle(self.speed,self.driving)
                    self.update_motors(L,R,stop)
            print(f"drive speed: {self.speed}")
            self.data['DriveSpeed']['Value'] = self.speed

    def cleanup(self):
        GPIO.cleanup()
