import digitalio

class ReaderInput:
    def __init__(self, pin) -> None:
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        
    def setPullUp(self):
        self.pin.pull = digitalio.Pull.UP

    def setPullDown(self):
        self.pin.pull = digitalio.Pull.DOWN
        
    def read(self) -> bool:
        return self.pin.value