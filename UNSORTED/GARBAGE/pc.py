import socket
import struct
from controller import XInput

HOST = '192.168.137.57'
PORT = 65432

xi = XInput()

class ControllerData:
    def __init__(self):
        self.wButtons = 0
        self.bLeftTrigger = 0
        self.bRightTrigger = 0
        self.sThumbLX = 0
        self.sThumbLY = 0
        self.sThumbRX = 0
        self.sThumbRY = 0

    def to_binary(self):
        return struct.pack('iiiiiii', self.wButtons, self.bLeftTrigger, self.bRightTrigger, self.sThumbLX, self.sThumbLY, self.sThumbRX, self.sThumbRY)


def convert(controller_data):
    controller = ControllerData()
    controller.wButtons = controller_data['wButtons']
    controller.bLeftTrigger = controller_data['bLeftTrigger']
    controller.bRightTrigger = controller_data['bRightTrigger']
    controller.sThumbLX = controller_data['sThumbLX']
    controller.sThumbLY = controller_data['sThumbLY']
    controller.sThumbRX = controller_data['sThumbRX']
    controller.sThumbRY = controller_data['sThumbRY']
    return controller


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    controller = ControllerData()
    for x in range(4):
        try:
            print(f"Reading input from controller {x}")
            state = xi.GetState(x)
            controller = convert(state)
            serialized_data = controller.to_binary()
            s.sendall(serialized_data)
        except Exception as e:
            print(f"Controller {x} not available: {e}")

    print("Reading all inputs from gamepad 0")
    while True:
        state = xi.GetState(0)
        custom_data = convert(state)
        serialized_data = custom_data.to_binary()  # Serialize the data
        s.sendall(serialized_data)
