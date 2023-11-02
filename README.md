# BPMI Robotic Annular Pipe Sanitization System
## Overview
- File Name: README.md
- Date Created: 10/11/2023 SAT
- Date Last Modified: 10/11/2023 SAT
- Description: readme
- Verion: 0.0.1
- Authors: Tiwari, Gomez, Bennett
## Hardware
- Raspberry pi zero 2
- Arduino nano every
- Raspberry pi camera 3
- DC motors (2)
## Programs
- main.py
- controller.py
- motorControl.py
- README.md
## Installation

## Wiring the robot

## Notes:

### Ethernet

### client

### server

To run server you will need to use flask/gunicorn and nginx

#### Nginx

Nginx is a lightway fast reverse proxy - we store the camera image in RAM and serve it up directly
configuration file from nginx/nginx.conf to /etc/nginx/nginx.conf

```
sudo apt-get install nginx
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf
```

restart nginx

```
sudo nginx -s reload
```

#### flask

install flask


copy configuration file

```
sudo
```

start flask

#### Camera

# References

- https://github.com/lukas/robot/tree/master
- https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/
- https://www.oreilly.com/content/how-to-build-a-robot-that-sees-with-100-and-tensorflow/
- https://learn.microsoft.com/en-us/windows/win32/api/_xinput/
- https://pinout.xyz/pinout/spi

# Credits

BPMI Team:
Ben Elverson,
Ben Genberg,
Jon Weir,
Kaitlyn Ritchey,
Katherine Bennett,
Madeline Weatherill,
Mark Armour,
Michael Gomez,
Simeon Tiwari,
Trace Peace, and
Will Zeisler
