from network import NetworkCommunication
from robot import RobotControl
from controller import Controller
# lights GPIO 21,20,18

def main():
    network = NetworkCommunication()
    robot = RobotControl(led_wf_pin=20, led_wu_pin=21, led_uv_pin=18, pwm_left_pin=12, pwm_right_pin=13)
    controller = Controller()

    try:
        conn = network.accept_connection()
        while True:
            controller_values = network.receive_data(conn)
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
