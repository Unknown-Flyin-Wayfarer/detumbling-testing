from machine import Pin, I2C,UART
from codes import*
import time

class torquer:
    moment= [0,0,0] 
    CALIB_OK = 1
    I2C_SDA_PIN = 6
    I2C_SCL_PIN = 7
    pin =Pin(9)
    def __init__(self):
        #self.Adcs_uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
        #self.Adcs_uart.init(bits=8, parity=0, stop=2)
        #Uart is asynchronus the data transmitted may not get fully picked up
        # Use i2c for fast data transfer. the data is not lost and also synchronised
        self.i2c=I2C(1,sda=Pin(self.I2C_SDA_PIN), scl=Pin(self.I2C_SCL_PIN), freq=100000)
      
        print("Init magnetorquers")

    def sendTorquerMoment(self, moment_x, moment_y, moment_z):
        # moment_x = self.moment_max[0]/moment_x
        # moment_y = self.moment_max[1]/moment_y
        # moment_z = self.moment_max[2]/moment_z
        self.moment = (moment_x,moment_y,moment_z)
        self.ADCS_Send(str(moment_x)+","+str(moment_y)+","+str(moment_z)+"\n")

    def ADCS_Send(self, string):
        #self.Adcs_uart.write(bytes(string, 'UTF-8')) 
        try:
        # Code that may raise an error
            self.pin.on()
            self.i2c.writeto(0x26, bytes(string,'UTF-8'))
            self.pin.off()
            return 1
        except Exception as e:
        # Handle the error
            print("An error occurred:", e)
            return 0

    
    def torquersOff(self)-> bool:
        '''
        Sets torquer moments to zero. Returns true.
        '''
        self.sendTorquerMoment(DEINIT,DEINIT,DEINIT) 
        #Write a confirmation from stm32 that the torquers are off.
        # TODO: Or send the hbridge off command to eps module.

        return True
    # def torquersDead(self)-> bool:
    #     '''
    #     Sets torquer moments to zero. Returns true.
    #     '''
    #     self.sendTorquerMoment(TORQUER_OFF,TORQUER_OFF,TORQUER_OFF) 
    #     #Write a confirmation from stm32 that the torquers are off.
    #     # TODO: Or send the hbridge off command to eps module.

    #     return True
    def torquersDemag(self)-> bool:
        '''
        Demagnetise the torquer using Reproducible cyclic state of magnetisation demagnetisation. Returns true when complete.
        '''
        self.sendTorquerMoment(DEMAG,DEMAG,DEMAG)
        time.sleep_ms(41)
        #Write a confirmation from stm32 that the torquers are off.
        # TODO: Or send the hbridge off command to eps module.

        return True
    
    def torquersRepeat(self)-> bool: 
        self.sendTorquerMoment(REPEAT,REPEAT,REPEAT)
        time.sleep_ms(41)
        #Write a confirmation from stm32 that the torquers are off.
        # TODO: Or send the hbridge off command to eps module.

        return True

    


