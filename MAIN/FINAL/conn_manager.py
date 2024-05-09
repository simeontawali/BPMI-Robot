"""
BPMI Robotic Annular Pipe Sanitization System
File Name: conn_manager.py
Authors: Tiwari, Gomez, Bennett

This script initiates the two threads required for robot operation, the camera streaming thread (cam.py)
and the controller data streaming thread (conn_manager.py).

"""

This script initializes the socket connection to the user application through the network class,
interprets the controller data through the controller class, and updates the robot hardware through
the robot class.

"""

from network import NetworkCommunication
from robot import RobotControl
from controller import Controller
import json

def main():
    network = NetworkCommunication() # receives/sends communications from user application
    robot = RobotControl() # interfaces with robot hardware
    controller = Controller() # interpret and store controller data

    try:
        conn = network.accept_connection() # establish connection
        while True:

            try:
                controller_values = network.receive_control_data(conn) # receive controller data
                if controller_values is None:
                    pass
                for controller_val in controller_values:
                    controller.update_state(controller_val) # update controller data
                    indicators = robot.update_control(controller) # update robot hardware control
                    #network.send_data(indicators) # not debugged, send robot status data back to user application
            except json.JSONDecodeError as e:
                print(e)
                print('Detected JSON decode error')

    finally:
        network.close_connection()
        robot.cleanup()

if __name__ == "__main__":
    main()
