import serial
from smbus2 import SMBus

class Module():
    def __init__(self) -> None:
        # Define I2C address for the DS1050Z
        self.PWM_L_ADDRESS = 2     # 010
        self.PWM_R_ADDRESS = 0     # 000
        self.CONTROL_CODE = 40     # 7'b0101000 too add to the address
        self.left_pwm = 0
        self.right_pwm = 0

        # Setup serial port
        #ser = serial.Serial('/dev/serial0', 9600, timeout=1)
        #ser.flush()
    # Function to send commands to DS1050Z via I2C
    def send_pwm_command(self, address, command):
        with SMBus(1) as bus:
            bus.write_byte(address + self.CONTROL_CODE, command)

    def change(self, duty_cycle, address):
        if duty_cycle == 100:
            command = 32  # 100% duty cycle
        else:
            duty_cycle_mapped = int((duty_cycle / 100) * 31)
            command = duty_cycle_mapped
        self.send_pwm_command(address, command)

    # TODO: 128 and 192 may work for both in certian situatuons. figure out that case
    def stop(self,address):
        if address == self.PWM_R_ADDRESS:
            command = 192  # R 8'b11000000 command for PWM shutdown
            self.send_pwm_command(address, command)
        elif address == self.PWM_L_ADDRESS:
            command = 128 # L 8'b10000000 command for PWM shutdown
            self.send_pwm_command(address, command)
        else:
            print("Bad address")

    def update(self):
        if self.left_pwm == 0:
            self.change(0,self.PWM_L_ADDRESS)
            self.stop(self.PWM_L_ADDRESS)
        else:
            self.change(self.left_pwm,self.PWM_L_ADDRESS)
        if self.right_pwm == 0:
            self.change(0,self.PWM_R_ADDRESS)
            self.stop(self.PWM_R_ADDRESS)
        else:
            self.change(self.left_pwm,self.PWM_R_ADDRESS)

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