from network import NetworkCommunication
from robot import RobotControl
from controller import Controller
# lights GPIO 21,20,18

def main():
    network = NetworkCommunication()
    robot = RobotControl()
    controller = Controller()

    try:
        conn = network.accept_connection()
        while True:
            # controller_values = network.receive_data(conn)
            # delimiter update
            controller_values = network.receive_control_data(conn)
            if controller_values is None:
                # controller.update_state(controller_values)
                pass
            # Process controller values
            controller.update_state(controller_values)
            #controller.print_values()
            robot.update_control(controller)

    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
