from codes import *
from Lora.lora import Lora
from imu import CalibrateIMU
import npy as np
from triad.triad import TRIAD
from torquer.torquer import torquer
import time 
from machine import Pin

led = Pin(25, Pin.OUT) 
class OBC:
    radio = Lora()
    imu = CalibrateIMU()
    attitudeController = torquer()
    orient = TRIAD()
    gyro_threshold = 0.02

    def __init__(self):
        MAG = {'X': 900000, 'Y': 0, 'Z': 0, 'H': 40457.71374183856, 
                   'F': 40555.973113595035, 'I': 3.989191930692085, 'D': -1.9202506878626793, 'GV': -1.9202506878626793} 
        magField = [MAG['X'], MAG['Y'], MAG['Z']]
        self.orient = TRIAD(v2=magField)
        

    def ExecuteCommand(self, code:str|int|None):
        led.on() 
        check,info = self.extract_values(code) 
        
        led.off()
        if (check == MAG_DATA):
            mag, gyro, accel = self.imu.getAllUncalibratedData() 
            self.radio.transmit(
                "MAG : "+str(mag[0])+" "+str(mag[1])+" "+str(mag[2]))
            while self.radio.isBusy:
                pass
            return str(code)+": DONE"

        if (check == TRIAD_ORIENT): 
            print("Triad Algorithm initializing")
            (mag, gyro, accel) = self.imu.getCalibDataWithoutLowPass() 
            DCM = self.orient.estimate(w1=accel, w2=mag)
            print(DCM)
            
            m = np.matmul(DCM, [[1], [0], [0]])
            values =(m[0][0],m[1][0],m[2][0])
            moment = tuple(round(value, 3) for value in values) 

            #print(str(moment))
            self.attitudeController.sendTorquerMoment(moment[0],moment[1],moment[2])
            while True:
                (mag, gyro, accel) = self.imu.getCalibDataWithoutLowPass() 
                if np.norm(gyro) < self.gyro_threshold:
                    self.attitudeController.torquersOff()
                    break
                time.sleep(1)
            print("Orientation Done")
            return str(code)+": DONE"
        
        if check == ORIENT_ADJUST:
            #print(str(info))
            mo = self.orient.orientTo(info) 
            
            pri =  (mo[0][0],mo[1][0],mo[2][0])
            
            moment = tuple(round(value, 3) for value in pri)
            self.attitudeController.sendTorquerMoment(moment[0],moment[1],moment[2])
            
            print(str(moment))
            return str(code)+": DONE"
            
         
            
    def extract_values(self,string):
            a = string.split(',')
            b = [int(value) for value in a]
            
            c = b[0]
            
            if len(b) == 4:
                d =  [b[1],b[2],b[3]]
            else:
                d = [0,0,0]
            #print(str([c,d]))
            return c,d
    
    def receiveCommand(self):
        s = self.radio.receive()
#         while self.radio.isBusy:
#             pass
        print(s)
        if len(s) > 0: 
            time.sleep_ms(150)
            self.radio.transmit("OK")
            self.ExecuteCommand(s)
            return
        else:
            raise ValueError("Received null")


