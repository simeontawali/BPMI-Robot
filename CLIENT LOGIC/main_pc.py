"""
BPMI Robotic Annular Pipe Sanitization System
File Name: main.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/28/2023 SAT
Description: main script
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:

Additional Notes:
Ensure ports are the same on both the pi and the pc
Ensure Host is configured to the IP of the pi

"""
from controller import XInput, XUSER_MAX_COUNT
from time import sleep
from ethernet_pc import init_client, send_data, recieve_data, close_connection

HOST = '0.0.0.0' # use the same host as IP address of Pi
# TODO: setup PI IP automatically. Read IP and establish connection
PORT = 65432  # Port to listen on (non-privileged ports are > 1023) ensure port is same for PC/PI
xi = XInput()


class startup():
    client_socket = init_client(HOST,PORT)

    try:
        for x in range(XUSER_MAX_COUNT):
            try:
                packet_number, gamepad = xi.GetState(x)
                # Convert the gamepad data to a string for transmission
                data = f"{packet_number},{gamepad}".encode()
                # Send data to the Raspberry Pi
                send_data(client_socket, data)
            except Exception as e:
                print(f"Controller {x} not available: {e}")

        while True:
            # Receive data from the Raspberry Pi
            received_data = recieve_data(client_socket)
            # Decode and unpack the data
            packet_number, gamepad = received_data.decode().split(',')
            gamepad = XINPUT_GAMEPAD.from_buffer_copy(gamepad)
            # Control the motors based on the received controller input
            control_motors(int(packet_number), gamepad)

    except KeyboardInterrupt:
        pass
    finally:
        # Close the connection
        close_connection(client_socket)    


