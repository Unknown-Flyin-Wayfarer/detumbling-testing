from machine import UART ,Pin

import time

class LogBoard:
    uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

    def __init__(self) -> None:
        self.uart.init()

    def send(self,string:str):
        data = "OBC,"+str(time.ticks_ms())+"-"+string+"$"
        self.uart.write(bytes(data,'UTF-8'))

    
