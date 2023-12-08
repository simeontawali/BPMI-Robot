import socket
import picamera

HOST = '0.0.0.0'  # Use 0.0.0.0 to accept connections from any IP
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()
    print('Connection established:', addr)
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == 'start':
                # Initialize Pi camera
                with picamera.PiCamera() as camera:
                    camera.resolution = (640, 480)
                    camera.start_preview()
                    input("Press Enter to stop the camera feed...")
                    camera.stop_preview()
            elif data == 'stop':
                print("Stop message received.")
            else:
                print("Invalid message.")
