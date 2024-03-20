from network import NetworkCommunication
from robot import RobotControl
from controller import Controller
# lights GPIO 21,20,18

def main():
    network = NetworkCommunication()
    robot = RobotControl(led_pin=6, pwm_left_pin=12, pwm_right_pin=13, freq=50)
    controller = Controller()

    try:
        network.accept_connection()
        while True:
            controller_values = network.receive_data()
            if controller_values is None:
                # controller.update_state(controller_values)
                break
            # Process controller values
            controller.update_state(controller_values)
            robot.update_control(controller)

    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
