from network import NetworkCommunication
from robot import RobotControl
from controller import Controller

def main():
    network = NetworkCommunication()
    robot = RobotControl(led=6, pwm_left=12, pwm_right=13, freq=50)
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

    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
