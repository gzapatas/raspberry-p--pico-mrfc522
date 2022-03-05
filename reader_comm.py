
import busio
import board

class ReaderComm:
    def __init__(self) -> None:
        self.uart = busio.UART(board.GP0, board.GP1, baudrate=115200,timeout=0.01)
        self.bufferTx = ""
        self.bufferRx = ""
        self.rxComplete = False
    
    def getTxBuffer(self) -> str:
        return self.bufferTx

    def setTxBuffer(self, tx: str):
        self.bufferTx = tx

    def getRxBuffer(self) -> str:
        if self.rxComplete:
            buffer = self.bufferRx
            self.bufferRx = ""
            self.rxComplete = False
            return buffer
        return ""

    async def run(self):
        rx = self.uart.read()
        if rx != None and not self.rxComplete:
            for byte in rx:
                character = chr(byte)

                if character == '\n':
                    self.rxComplete = True
                    break

                self.bufferRx += chr(byte)

        if self.getTxBuffer() != "":
            self.uart.write(bytearray(self.bufferTx.encode()))
            self.setTxBuffer("")
