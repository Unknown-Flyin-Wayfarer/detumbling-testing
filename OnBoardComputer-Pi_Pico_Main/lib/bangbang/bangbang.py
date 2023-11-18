from imu import CalibrateIMU
import math
from machine import Pin
import npy as np
import time
from torquer.torquer import torquer
from torquer.logger import LogBoard
from codes import *
led = Pin(25, Pin.OUT)


class BangBang:
    '''
    Detumbling Algorithm (Bang Bang Max Torque). This class calls imu sensor on itsown pls avoid calling the IMU befor or after this calls.

    detect_motion() checks whether the satellite is moving or drifting.

    getMagFieldSign() retruns the sign of mag field on the required axis.
    '''

    # Motion detection threshold
    gyro_threshold = 0.009  # value should be greater than 0.008
    mag_threshold = (0.52)
    accel_threshold = (0.005) 
    inmotion = True
    data2 = [1,1,1]
    f = 1
    mag = [0.0,0,0]
    prev_mag_sign = [0.0,0,0]
    prev_mag= [0.0,0,0]
    p_t = 0
    dB = [0,0,0.0]

    def __init__(self):
        self.last_tick = time.ticks_us()
        self.imu = CalibrateIMU()
        #self.torq = torquer()
        #self.logger = LogBoard() 
        self.p_t = time.ticks_us()

    def getMagFieldSign(self,ticks:int):
        '''
        Returns the sign of the Derivative of magnetic field of each axis as tuple of (x,y,x). If mag field is -ve it returns -1.
        '''
        noisebias = 0.0
        self.mag = tuple(round(m, 3) for m in self.mag)
        dt = (ticks-self.p_t)/1000
        if dt==0:
            raise ValueError("Div by zero in getMagFieldSign")

        self.dB = list((self.mag[i]-self.prev_mag[i])/dt for i in range(3))  
        print(str(self.dB)+" "+str(self.mag))
        return list((math.copysign(1, self.mag[i]) if abs(self.dB[i]) > noisebias else self.prev_mag_sign[i]) for i in range(3))

    def CalculateMomentAndSend(self):
        '''
        Sends torquer moment to adcs and waits for 98ms.
        '''

        #self.torq.torquersDemag()
        #self.torq.torquersOff()
        time.sleep_ms(2)
        (self.mag, gyro, accel,t) = self.imu.getCalibDataWithoutLowPass()
        # if (math.sqrt(self.mag[0]**2+self.mag[1]**2+self.mag[2]**2) > 65):
        #     self.torq.torquersOff()
        #     time.sleep_ms(20)
        #     (self.mag, gyro, accel) = self.imu.getCalibDataWithoutLowPass()

        x, y, z = self.getMagFieldSign(t)
#         print("{:.2f},{:.2f},{:.2f}".format(
#             self.mag[0], self.mag[1], self.mag[2]))

        #LogData = "{:.2f} {:.2f} {:.2f}".format(gyro[0], gyro[1], gyro[2])

        #self.logger.send(LogData)
        gval = np.norm(gyro) 
        data = (-int(x), -int(y),-int(z))
        
        if (gval < self.gyro_threshold):
            self.inmotion = False
            return
        elif (gval < 0.1):
            if self.f:
                self.data2 = self.prev_mag_sign
                self.f = 0
            data = self.data2

        self.prev_mag_sign = (x,y,z)
        self.prev_mag = self.mag
        self.p_t = t
        #self.torq.sendTorquerMoment(data[0], data[1],data[2])
        #print(str(data[0])+" "+str(data[1])+" "+str(data[2]))
        time.sleep_ms(98)
        # print(str(self.moment_x)+","+str(self.moment_y)+","+str(self.moment_z))

    def start(self):
        measureTime = time.ticks_us()
        print("Starting Detumbling...")
        flag = True
        while self.inmotion:
            if flag:
                print("Detected motion")
                flag = False
            led.toggle()
            self.CalculateMomentAndSend()
            time.sleep_ms(50)
        led.off()
        t = abs(time.ticks_diff(measureTime, time.ticks_us()))/1000000
        print("Detumble ended, took "+str(t)+"s")

