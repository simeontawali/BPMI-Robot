"""
BPMI Robotic Annular Pipe Sanitization System
File Name: cam_stream.py
Date Created: 11/09/2023 SAT
Date Last Modified: 11/09/2023 SAT
Description: MJPEG Web Streaming
Verion: 1.0.1
Authors: Gomez, Tiwari, Bennett

Build Notes: First Finished Implementation

Dependencies: picamera

References: https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming

Additional Notes:

"""
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<head>
<title>BPMI MJPEG Server</title>
</head>
<body>
<h1>BPMI CAM</h1>
<img src="stream.mjpg" width="1280" height="1024" />
</body>
</html>
"""

# Class to handle the streaming output from the camera
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        # Check if the buffer starts with the JPEG start marker
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

# Class to handle HTTP requests
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to /index.html
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
            # Set up headers for MJPEG streaming
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        # Wait for a new frame to be available
                        output.condition.wait()
                        frame = output.frame
                    # Send the frame as part of the MJPEG stream
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
            # Return a 404 error for unknown paths
            self.send_error(404)
            self.end_headers()

# Class for the streaming server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Set up the camera with resolution and framerate
with picamera.PiCamera(resolution='1280x1024', framerate=30) as camera:
    # Create a StreamingOutput instance to handle the camera output
    output = StreamingOutput()
    # Start recording with MJPEG format
    camera.start_recording(output, format='mjpeg')
    try:
        # Set up the address and create the streaming server
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        # Start serving indefinitely
        server.serve_forever()
    finally:
        # Stop recording when the program exits
        camera.stop_recording()