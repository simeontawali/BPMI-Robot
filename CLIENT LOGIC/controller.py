"""
BPMI Robotic Annular Pipe Sanitization System
File Name: controller.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: XInput Game Controller APIs
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:
https://learn.microsoft.com/en-us/windows/win32/api/_xinput/
https://gist.github.com/artizirk/b407ba86feb7f0227654f8f5f1541413

Additional Notes:
For non standard controller support use DirectInput over Xinput. Note: triggers may not work

"""

from ctypes import Structure

class XINPUT_BUTTONS(Structure):
    pass

class XINPUT_GAMEPAD(Structure):
    pass

class XINPUT_STATE(Structure):
    pass

class Xinput:
    pass


if __name__ == "__main__":
    pass