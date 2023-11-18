from Lora.sx1262 import SX1262  

class Lora:
    isBusy = False
    def __init__(self) -> None:
        self.sx = SX1262(clk=10, mosi=11, miso=12, cs=13, irq=20, rst=15, gpio=2)
        self.sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
                 power=-5, currentLimit=60.0, preambleLength=8,
                 implicit=False, implicitLen=0xFF,
                 crcOn=True, txIq=False, rxIq=False,
                 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
    #     self.sx.setBlockingCallback(False, self.cb)

    # def cb(self, events):
    #     if events & SX1262.RX_DONE:
    #         print('RX done.')
    #         self.isBusy = False
    #     elif events & SX1262.TX_DONE: 
    #         print('TX done.')
    #         self.isBusy = False

    def receive(self): 
        msg, err = self.sx.recv()
        if len(msg) > 0:
            error = SX1262.STATUS[err]
            string = msg.decode('utf-8') 
            return str(string)
        return 0

    def transmit(self, string: str): 
        self.sx.send(bytes(string, 'UTF-8'))

