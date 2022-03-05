import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

class ReaderUsb:
    def __init__(self) -> None:
        self.keyboard = Keyboard(usb_hid.devices)
        self.keyboard_layout = KeyboardLayoutUS(self.keyboard)
    
    def writeMessage(self, message: str):
        self.keyboard_layout.write(message)