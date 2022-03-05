import board
import asynccp
from asynccp.time import Duration
from reader_main_serial import ReaderMainSerial
from reader_main_usb import ReaderMainUsb
from reader_input import ReaderInput

dpsw0 = ReaderInput(board.GP17)
dpsw0.setPullUp()

def run():
    pinValue = dpsw0.read()
    print("Starting rfid reader")
    if pinValue:
        print("Serial mode selected")
        main = ReaderMainSerial()
        main.startUp()
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=main.run)
    else:
        print("Usb mode selected")
        main = ReaderMainUsb()
        main.startUp()
        asynccp.schedule(Duration.of_milliseconds(10), coroutine_function=main.run)

    asynccp.run()

if __name__ == '__main__':
    run()
