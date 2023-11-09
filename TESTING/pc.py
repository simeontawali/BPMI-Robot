from controller import XInput
import socket
import os

HOST = '192.168.137.57'  # The IP address of your Raspberry Pi
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

xi = XInput()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for x in range(4):
        try:
            print(f"Reading input from controller {x}")
            data = str(xi.GetState(x)).encode('utf-8')
            s.sendall(data)
        except Exception as e:
            print(f"Controller {x} not available: {e}")

    print("Reading all inputs from gamepad 0")
    while True:
        data = str(xi.GetState(0)).encode('utf-8')
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print(data)
        s.sendall(data)
