def main():
    network = NetworkCommunication()
    robot = RobotControl(led=6, pwm_left=12, pwm_right=13, freq=50)

    try:
        network.accept_connection()
        while True:
            controller_values = network.receive_data()
            if controller_values is None:
                break
            # Process controller values
            # Use ControllerProcessing methods if needed
            # Update robot control based on processed input
    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
