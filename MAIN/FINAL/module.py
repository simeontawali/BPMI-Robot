"""
BPMI Robotic Annular Pipe Sanitization System
File Name: module.py
Authors: Tiwari, Gomez, Bennett

This script is dedicated to controlling the tape module linear actuator. It is initialized in the robot hardware code,
and its functions are called from within that code based on controller data. It sends I2C commands to the PWM generator
chips on the tape module.

"""

import serial
from smbus2 import SMBus, i2c_msg
import os

class Module():
    def __init__(self) -> None:
        # Define I2C address for the DS1050Z
        self.PWM_L_ADDRESS = 2     # 010
        self.PWM_R_ADDRESS = 0     # 000
        self.CONTROL_CODE = 40     # 7'b0101000 too add to the address
        self.left_pwm = 0
        self.right_pwm = 0
        self.left_pwm_stopped = False
        self.right_pwm_stopped = False

    # Function to send commands to DS1050Z via I2C
    def send_pwm_command(self, address, command):
        with SMBus(1) as bus:
            try:
                msg = i2c_msg.write(address + self.CONTROL_CODE, [command])
                bus.i2c_rdwr(msg)
            except OSError as e:
                print(e)
                if e.errno == 121:
                    print("Tape module not connected, do not attempt to use tape module controls")
                    
    # send command to change duty cycle
    def change_duty_cycle(self, duty_cycle, address):
        if duty_cycle == 100:
            command = 32  # 100% duty cycle
        else:
            duty_cycle_mapped = int((duty_cycle / 100) * 31)
            command = duty_cycle_mapped
        self.send_pwm_command(address, command)

    # send command to shutdown PWM chip (stop it from generating a signal)
    def stop(self,address):
        self.send_pwm_command(address, 192) # 8'b11000000 command for PWM shutdown
        if address == self.PWM_R_ADDRESS:
            self.right_pwm_stopped = True
        elif address == self.PWM_L_ADDRESS:
            self.left_pwm_stopped = True

    # send command to restart PWM chip (chip must be restarted after shutdown)
    def restart(self,address):
        self.send_pwm_command(address, 128) # 8'b10000000 command for PWM shutdown

    # given that the PWM frequencies have changed, send I2C commands to update chip states
    def update(self):
        if self.left_pwm == 0:
            self.stop(self.PWM_L_ADDRESS)
            #print("stopping left PWM")
        elif self.left_pwm_stopped:
            self.restart(self.PWM_L_ADDRESS)
            self.change_duty_cycle(self.left_pwm,self.PWM_L_ADDRESS)
            #print("restarting left PWM")
        else:
            self.change_duty_cycle(self.left_pwm,self.PWM_L_ADDRESS)
            #print("adjusting left PWM")
        if self.right_pwm == 0:
            self.stop(self.PWM_R_ADDRESS)
            #print("stopping right PWM")
        elif self.right_pwm_stopped:
            self.restart(self.PWM_R_ADDRESS)
            self.change_duty_cycle(self.right_pwm,self.PWM_R_ADDRESS)
            #print("restarting right PWM")
        else:
            self.change_duty_cycle(self.right_pwm,self.PWM_R_ADDRESS)
            #print("adjusting right PWM")

    # functions to be called by robot class
    def actuator_forward(self):
        self.left_pwm = 50
        self.right_pwm = 0
        self.update()
    def actuator_backward(self):
        self.right_pwm = 50
        self.left_pwm = 0
        self.update()
    def actuator_off(self):
        self.left_pwm = 0
        self.right_pwm = 0
        self.update()
