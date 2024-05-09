#!/usr/bin/python3

"""
BPMI Robotic Annular Pipe Sanitization System
File Name: cam.py
Authors: Tiwari, Gomez, Bennett

This script sets up a streaming server using Picamera2 library to stream MJPEG frames.
Clients can view the stream by pointing a web browser to http://<this-ip-address>:8000.

Requirements:
- Requires simplejpeg to be installed (pip3 install simplejpeg).
- Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
"""

# Import necessary modules and libraries
import io
import logging
import socketserver
from http import server
from threading import Condition

# Import Picamera2 library components
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls

# HTML page to be served
PAGE = """\
<html>
<head>
<title>BPMI picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>BPMI Picamera2 MJPEG Streaming Demo yay</h1>
<img src="stream.mjpg" width="1920" height="1080" />
</body>
</html>
"""

# Class for handling streaming output
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    # Write method to update the frame
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# Class for handling HTTP requests
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handling various HTTP paths
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serve the main HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Start streaming MJPEG frames
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            # Return 404 for unrecognized paths
            self.send_error(404)
            self.end_headers()

# Class for streaming server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Initialize Picamera2
picam2 = Picamera2()
# Configure Picamera2 with video settings
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}))
# Set autofocus mode to Continuous
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
# Initialize streaming output
output = StreamingOutput()
# Start recording with Picamera2, encoding to JPEG and outputting to file
picam2.start_recording(JpegEncoder(), FileOutput(output))

# Start the streaming server
try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
# Stop recording and close the server when interrupted
finally:
    picam2.stop_recording()
