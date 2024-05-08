from network import NetworkCommunication
from robot import RobotControl
from controller import Controller
import json
# lights GPIO 21,20,18

def main():
    network = NetworkCommunication()
    robot = RobotControl()
    controller = Controller()

    try:
        conn = network.accept_connection()
        while True:

            try:
                controller_values = network.receive_control_data(conn)
                if controller_values is None:
                    pass
                for controller_val in controller_values:
                    controller.update_state(controller_val)
                    indicators = robot.update_control(controller)
                    #network.send_data(indicators) # not debugged
            except json.JSONDecodeError as e:
                print(e)
                print('Detected JSON decode error')

    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
