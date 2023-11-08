import socket

HOST = '0.0.0.0'  # Use 0.0.0.0 to accept connections from any IP
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received message from PC: {data.decode()}")
            response_message = input("Enter message to send back to PC: ")
            conn.sendall(response_message.encode())
