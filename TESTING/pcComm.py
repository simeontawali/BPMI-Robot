import socket

HOST = '169.254.232.79'  # Update this with the Raspberry Pi's IP
PORT = 12345  # Make sure this port matches the one used in the Raspberry Pi script

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter message to send to Raspberry Pi: ")
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received from Raspberry Pi: {data.decode()}")
