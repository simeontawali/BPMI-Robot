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

from ctypes import WinDLL, WinError, Structure, POINTER, byref, c_ubyte
from ctypes.util import find_library
from ctypes.wintypes import DWORD, WORD, SHORT

# for some reason wintypes.BYTE is defined as signed c_byte and as c_ubyte
BYTE = c_ubyte


# Max number of controllers supported
XUSER_MAX_COUNT = 4

class XINPUT_BUTTONS(Structure):
	"""Bit-fields of XINPUT_GAMEPAD wButtons"""

	_fields_ = [
		("DPAD_UP", WORD, 1),
		("DPAD_DOWN", WORD, 1),
		("DPAD_LEFT", WORD, 1),
		("DPAD_RIGHT", WORD, 1),
		("START", WORD, 1),
		("BACK", WORD, 1),
		("LEFT_THUMB", WORD, 1),
		("RIGHT_THUMB", WORD, 1),
		("LEFT_SHOULDER", WORD, 1),
		("RIGHT_SHOULDER", WORD, 1),
		("_reserved_1_", WORD, 1),
		("_reserved_1_", WORD, 1),
		("A", WORD, 1),
		("B", WORD, 1),
		("X", WORD, 1),
		("Y", WORD, 1)
	]
	
	def __repr__(self):
		r = []
		for name, type, size in self._fields_:
			if "reserved" in name:
				continue
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"
	

class XINPUT_GAMEPAD(Structure):
	"""Describes the current state of the Xbox 360 Controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_gamepad
	
	wButtons is a bitfield describing currently pressed buttons
	"""
	_fields_ = [
		("wButtons", XINPUT_BUTTONS),
		("bLeftTrigger", BYTE),
		("bRightTrigger", BYTE),
		("sThumbLX", SHORT),
		("sThumbLY", SHORT),
		("sThumbRX", SHORT),
		("sThumbRY", SHORT),
	]
	
	def __repr__(self):
		r = []
		for name, type in self._fields_:
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"


class XINPUT_STATE(Structure):
	"""Represents the state of a controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_state
	
	dwPacketNumber: State packet number. The packet number indicates whether
		there have been any changes in the state of the controller. If the
		dwPacketNumber member is the same in sequentially returned XINPUT_STATE
		structures, the controller state has not changed.
	"""
	_fields_ = [
		("dwPacketNumber", DWORD),
		("Gamepad", XINPUT_GAMEPAD)
	]
	
	def __repr__(self):
		return f"XINPUT_STATE(dwPacketNumber={self.dwPacketNumber}, Gamepad={self.Gamepad})"

class XInput:
	"""Minimal XInput API wrapper"""

	def __init__(self):
		# https://docs.microsoft.com/en-us/windows/win32/xinput/xinput-versions
		# XInput 1.4 is available only on Windows 8+.
		# Older Windows versions are End Of Life anyway.
		lib_name = "XInput1_4.dll"  
		lib_path = find_library(lib_name)
		if not lib_path:
			raise Exception(f"Couldn't find {lib_name}")
		self._XInput_ = WinDLL(lib_path)
		self._XInput_.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
		self._XInput_.XInputGetState.restype = DWORD

	def GetState(self, dwUserIndex):
		state = XINPUT_STATE()
		ret = self._XInput_.XInputGetState(dwUserIndex, byref(state))
		if ret:
			raise WinError(ret)
		return state.dwPacketNumber, state.Gamepad


if __name__ == "__main__":
	xi = XInput()
	from time import sleep
	for x in range(XUSER_MAX_COUNT):
		try:
			print(f"Reading input from controller {x}")
			print(xi.GetState(x))
		except Exception as e:
			print(f"Controller {x} not available: {e}")

	print("Reading all inputs from gamepad 0")
	while True:
		print(xi.GetState(0), end="     \r")
		sleep(0.016)
