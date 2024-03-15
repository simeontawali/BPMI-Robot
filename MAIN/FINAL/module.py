import RPi.GPIO as GPIO
import smbus
import time

class Module():
    def __init__(self):
        # Setup I2C
        bus = smbus.SMBus(1) # 1 should be /dev/i2c-1
        DS1050_ADDRESS = 0x00 # Replace 0x00 with the DS1050's actual address, I dont know this yet
        PWM_REG = 0x00 # PWM register address; not sure what this is yet

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        IN1_MOTOR1 = 2 # Motor 1 direction pin
        IN1_MOTOR2 = 4 # Motor 2 direction pin
        GPIO.setup(IN1_MOTOR1, GPIO.OUT)
        GPIO.setup(IN1_MOTOR2, GPIO.OUT)
        pwm = GPIO.PWM(2, 1000) # Set PWM frequency to 1000 Hz for now

    def set_pwm_duty_cycle(self,duty_cycle):
        """
        Set the PWM duty cycle on the DS1050.
        :param duty_cycle: A value from 0 to 31 (5-bit resolution), where 31 is 100% duty cycle.
        """
        self.bus.write_byte_data(self.DS1050_ADDRESS, self.PWM_REG, duty_cycle) # TODO: implement func

# Function to control motor direction and speed
def control_motor(self,motor, direction, speed):
    if motor == 1:
        GPIO.output(self.IN1_MOTOR1, direction)
    elif motor == 2:
        GPIO.output(self.IN1_MOTOR2, direction)
    self.set_pwm_duty_cycle(speed) # Adjust this



    def tape_module():
        pass