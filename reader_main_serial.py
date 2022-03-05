import asynccp
from asynccp.time import Duration
import board
import time
from reader_device import ReaderDevice
from reader_comm import ReaderComm
from reader_output import ReaderOutput


class ReaderMainSerial:
    def __init__(self) -> None:
        self.device = ReaderDevice()
        self.comm = ReaderComm()
        self.testLed = ReaderOutput(board.LED)
        self.ledRed = ReaderOutput(board.GP19)
        self.ledGreen = ReaderOutput(board.GP20)
        self.buzzer = ReaderOutput(board.GP21)
        self.cardPresent = False
        self.realtime = False
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.comm.run)
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.device.run)
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=self.buzzer.run)
    
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
    
    def sendStatus(self, state: bool, message: str = ""):
        if state:
            if self.device.cardId == "":
                self.comm.setTxBuffer("ok,notcard,00000000")
            else: 
                self.comm.setTxBuffer("ok,card," + self.device.cardId)
        else:
            self.comm.setTxBuffer("error,notcard," + message)

    async def run(self):
        changeStatus = False

        if self.device.cardId != "" and not self.cardPresent:
            self.cardPresent = True
            changeStatus = True
            self.testLed.turnOn()
        elif self.device.cardId == "" and self.cardPresent:
            self.cardPresent = False
            changeStatus = True
            self.testLed.turnOff()

        if self.realtime and changeStatus:
            self.sendStatus(True)
        
        message = self.comm.getRxBuffer()
        if message == "":
            return

        if message == "REALTIME":
            self.realtime = True
            self.sendStatus(True)
        elif message == "POLL":
            self.realtime = False
            self.sendStatus(True)
        elif message == "STATUS":
            self.sendStatus(True)
        elif message == "BUZZER":
            self.buzzer.startPulse()
            self.sendStatus(True)
        elif message == "CARDOUT":
            self.ledRed.turnOn()
            self.ledGreen.turnOff()
            self.sendStatus(True)
        elif message == "CARDIN":
            self.ledRed.turnOff()
            self.ledGreen.turnOn()
            self.buzzer.startPulse()
            self.sendStatus(True)
        else:
            self.sendStatus(False, "1-"+message)