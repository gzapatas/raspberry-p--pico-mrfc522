import board
import asynccp
import time
from asynccp.time import Duration
from reader_usb import ReaderUsb
from reader_device import ReaderDevice
from reader_output import ReaderOutput

class ReaderMainUsb:
    def __init__(self) -> None:
        self.device = ReaderDevice()
        self.comm = ReaderUsb()
        self.testLed = ReaderOutput(board.LED)
        self.ledRed = ReaderOutput(board.GP19)
        self.ledGreen = ReaderOutput(board.GP20)
        self.buzzer = ReaderOutput(board.GP21)
        self.cardReported = False

        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.device.run)
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.buzzer.run)
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.ledRed.run)
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.ledGreen.run)
    
    def startUp(self):
        self.ledRed.turnOff()
        self.ledGreen.turnOn()
        self.testLed.turnOn()
        self.buzzer.turnOn()
        time.sleep(0.3)
        self.ledRed.turnOn()
        self.ledGreen.turnOff()
        self.testLed.turnOff()
        self.buzzer.turnOff()
    
    async def run(self):
        if self.device.cardId != "" and not self.cardReported:
            self.comm.writeMessage(self.device.cardId + "\n")
            self.cardReported = True
            self.testLed.turnOn()
            self.buzzer.startPulse()
            self.ledRed.startPulse()
            self.ledGreen.startPulse()
        elif self.device.cardId == "":
            self.cardReported = False
            self.testLed.turnOff()
