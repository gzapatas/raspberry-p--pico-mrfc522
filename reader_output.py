import digitalio
import asynccp

class ReaderOutput:
    def __init__(self, pin) -> None:
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.pulseTimeout = 0.3
        self.pulse = False
        
    def turnOn(self):
        self.pin.value = True

    def turnOff(self):
        self.pin.value = False
    
    def startPulse(self,timeout = 0.3):
        self.pulse = True
        self.pulseTimeout = timeout

    async def run(self):
        if self.pulse:
            self.pin.value = True
            await asynccp.delay(self.pulseTimeout)
            self.pin.value = False
            self.pulse = False