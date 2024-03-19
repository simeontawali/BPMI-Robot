import serial
from smbus2 import SMBus

class Module():
    def __init__(self) -> None:
        # Define I2C address for the DS1050Z
        PWM_L_ADDRESS = 2     # 010
        PWM_R_ADDRESS = 0     # 000
        CONTROL_CODE = 40     # 7'b0101000 too add to the address

        # Setup serial port
        ser = serial.Serial('/dev/serial0', 9600, timeout=1)
        ser.flush()
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

    def stop(self,address):
        command = 192  # Shutdown command
        self.send_pwm_command(address, command)


    def operate(self, command):
        if self.ser.in_waiting > 0:
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