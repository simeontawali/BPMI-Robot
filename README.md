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

### Pi setup
Install the following:
- RaspberryPi Imager Software: https://www.raspberrypi.org/software/
- Bonjour Drivers: https://support.apple.com/kb/dl999?locale=en_GB
- Putty: https://www.putty.org/
- USB Ethernet Drivers: https://www.catalog.update.microsoft.com/Search.aspx?q=USB+RNDIS+Gadget
Setup the raspberry pi lite software
Make the following edits in boot:
Config.txt: "dtoverlay=dwc2" 
Cmdline.txt:  "modules-load=dwc2,g_ether" (add a space and insert after "rootwait")
SSH Host: "raspberrypi.local"
create a file named ssh (no type)
see the following tutorial for additional help: https://www.youtube.com/watch?v=XaTmG708Mss&ab_channel=CineSpirit

Establish connection in putty
yourhostname.host
open
Install the following in the terminal:
- sudo apt-get update && sudo apt-get upgrade -y
- sudo apt-get install python-pip
- sudo apt-get install python3-pip

Install a text editor like VIM:
- sudo apt install vim

## Camera setup
Enable legacy camera support
'''
sudo raspi-config
'''
- Interface options
- Legacy camera

Test camera is enabled and connected to the pi:
'''
vcgencmd get_camera
'''
Test picture:
'''
raspistill -o Desktop/image.jpg
'''


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
- https://www.instructables.com/How-to-Use-Ethernet-on-Raspberry-Pi-Zero-W/
- https://www.hackster.io/sameerk/getting-started-with-raspberry-pi-zero-w-and-python-3-16c274
- https://medium.com/practical-coding/headless-setup-of-raspberry-pi-once-and-for-all-de5a2c4f715b
- https://www.reddit.com/r/RASPBERRY_PI_PROJECTS/comments/emt7ek/raspberry_pi_zero_w_headless_procedure_for/
- https://nrsyed.com/2021/06/02/raspberry-pi-headless-setup-via-ethernet-and-how-to-share-the-host-pcs-internet-connection/
- https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system
- https://github.com/pyqt/examples
- https://roboticsbackend.com/raspberry-pi-create-a-flask-server/#Install_%E2%80%93_Setup_Raspberry_Pi_OS_and_Flask
- https://gist.github.com/artizirk/b407ba86feb7f0227654f8f5f1541413
- https://www.youtube.com/watch?v=XaTmG708Mss&ab_channel=CineSpirit

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
