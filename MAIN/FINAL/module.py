import serial
from smbus2 import SMBus, i2c_msg

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

        # Setup serial port
        #ser = serial.Serial('/dev/serial0', 9600, timeout=1)
        #ser.flush()
        #self.bus = SMBus(1)
    # Function to send commands to DS1050Z via I2C
    def send_pwm_command(self, address, command):
        with SMBus(1) as bus:
            #bus.write_byte(address + self.CONTROL_CODE, command)
            msg = i2c_msg.write(address + self.CONTROL_CODE, [command])
            bus.i2c_rdwr(msg)

    def change_duty_cycle(self, duty_cycle, address):
        if duty_cycle == 100:
            command = 32  # 100% duty cycle
        else:
            duty_cycle_mapped = int((duty_cycle / 100) * 31)
            command = duty_cycle_mapped
        self.send_pwm_command(address, command)

    # TODO: 128 and 192 may work for both in certian situatuons. figure out that case
    def stop(self,address):
        self.send_pwm_command(address, 192) # 8'b11000000 command for PWM shutdown

        if address == self.PWM_R_ADDRESS:
            self.right_pwm_stopped = True
        #     command = 128 # 192  # R 8'b11000000 command for PWM shutdown
        #     self.send_pwm_command(address, command)
        elif address == self.PWM_L_ADDRESS:
            self.left_pwm_stopped = True
        #     command = 128 # L 8'b10000000 command for PWM shutdown
        #     self.send_pwm_command(address, command)
        # else:
        #     print("Bad address")

    def restart(self,address):
        self.send_pwm_command(address, 128) # 8'b10000000 command for PWM shutdown

    def update(self):
        if self.left_pwm == 0:
            #self.change_duty_cycle(0,self.PWM_L_ADDRESS)
            self.stop(self.PWM_L_ADDRESS)
            print("stopping left PWM")
        elif self.left_pwm_stopped:
            self.restart(self.PWM_L_ADDRESS)
            self.change_duty_cycle(self.left_pwm,self.PWM_L_ADDRESS)
            print("restarting left PWM")
        else:
            self.change_duty_cycle(self.left_pwm,self.PWM_L_ADDRESS)
            print("adjusting left PWM")
        if self.right_pwm == 0:
            #self.change_duty_cycle(0,self.PWM_R_ADDRESS)
            self.stop(self.PWM_R_ADDRESS)
            print("stopping right PWM")
        elif self.right_pwm_stopped:
            self.restart(self.PWM_R_ADDRESS)
            self.change_duty_cycle(self.right_pwm,self.PWM_R_ADDRESS)
            print("restarting right PWM")
        else:
            self.change_duty_cycle(self.right_pwm,self.PWM_R_ADDRESS)
            print("adjusting right PWM")

# increment and decrement pwm counter for l/r respectively
    def incr_l(self):
        if self.left_pwm < 32:
            self.left_pwm += 1
            self.update()
    def decr_l(self):
            if self.left_pwm > 0:
                self.left_pwm -= 1
                self.update()
    def incr_r(self):
            if self.right_pwm < 32:
                self.right_pwm += 1
                self.update()
    def decr_r(self):
            if self.right_pwm > 0:
                self.right_pwm -= 1
                self.update()

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

    def operate(self, command):
        #if self.ser.in_waiting > 0:
            if command:
                drive_change = False
                stop_PWM = False
                
                if command.startswith('R'):
                    address = self.PWM_R_ADDRESS
                    if command[1] == 'S':
                        stop_PWM = True
                    else:
                        duty_cycle = int(command[1:])
                        drive_change = True
                        
                elif command.startswith('L'):
                    address = self.PWM_L_ADDRESS
                    if command[1] == 'S':
                        stop_PWM = True
                    else:
                        duty_cycle = int(command[1:])
                        drive_change = True
                        
                if drive_change:
                    if duty_cycle == 100:
                        command = 32  # 100% duty cycle
                    else:
                        duty_cycle_mapped = int((duty_cycle / 100) * 31)
                        command = duty_cycle_mapped
                    self.send_pwm_command(address, command)
                    
                elif stop_PWM:
                    command = 192  # Shutdown command
                    self.send_pwm_command(address, command)

    def tape_module():
        pass