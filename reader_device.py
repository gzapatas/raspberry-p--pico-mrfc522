import reader.mfrc522 as mfrc522
import board

class ReaderDevice:
    def __init__(self) -> None:
        self.reader = mfrc522.MFRC522(sck=board.GP2,miso=board.GP4,mosi=board.GP3,cs=board.GP5,rst=board.GP22)
        self.reader.set_antenna_gain(0x07 << 4)
        self.cardId = ""
        self.counterCardOut = 0

    async def run(self):
        (stat, _) = self.reader.request(self.reader.REQIDL)
        if stat == self.reader.OK:
            (stat, raw_uid) = self.reader.anticoll()
            if stat == self.reader.OK:
                self.counterCardOut = 0
                #Card in
                if self.cardId == "":
                    (stat, raw_uid) = self.reader.anticoll()
                    if len(raw_uid) >= 4:
                        self.cardId = "%02x%02x%02x%02x"%(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
        else:
            self.counterCardOut += 1
            #Card out
            if self.cardId and self.counterCardOut >= 2:
                self.cardId = ""
