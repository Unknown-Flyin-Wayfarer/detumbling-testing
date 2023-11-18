from machine import Pin
from lib.bangbang.bangbang import BangBang 
import time
from lib.codes import *
from lib.command import OBC

led = Pin(25, Pin.OUT) 
detumble = BangBang() 

#Start detumbling
detumble.start()
time.sleep_ms(100)
del detumble 
#obc = OBC()

#Set the reference frame for finding orientaion

#Estimate the orientaion and adjust for correction

#Set mag field as ref vector 

#Begin transmission 
'''obc.ExecuteCommand(str(TRIAD_ORIENT))
while True:
    led.off()
    try:
        obc.receiveCommand()
    except Exception as e:
        print(e)
    time.sleep_ms(100)
'''


