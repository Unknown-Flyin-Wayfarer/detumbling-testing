import time
from bmx160 import BMX160 
import npy as np

class CalibrateIMU:
    init = False

    bmx = BMX160(1)

    # Raw data
    raw_mag = [0, 0, 0]
    raw_gyro = [0, 0, 0]
    raw_accel = [0, 0, 0]

    # Calibrated Data
    mag = [0.0, 0, 0]
    gyro = [0.0, 0, 0]
    accel = [0.0, 0, 0]

    # Calibrate GYROSCOPE
    gyro_bias = [-0.04005197, 0.004573256, 0.03303826]
    alpha = 0.2  # Smoothing factor, 0 < alpha < 1

    # Calib ACCELEROMETER
    A = [[0.998244, 0.002527, -0.002566],
         [0.002527, 0.999236, -0.000588],
         [-0.002566, -0.000588, 0.995214]]
    b = [-0.045349, -0.018113, 0.027794]

    alpha_accel = 0.7

    # Calib MAGNETOMETER
    Amag = [[0.178208, -0.000699, 0.002791],
              [-0.000699, 0.175333, -0.002224],
              [0.002791, -0.002224, 0.297395]]
    bmag = [12.377759, -13.149879, -12.212561]

    alpha_mag = 0.66

    def __init__(self):
        self.init = True
        self.begin()

    def begin(self):
        self.bmx.begin()
        self.bmx.set_gyro_range(self.bmx.GyroRange_125DPS)
        self.bmx.set_accel_range(self.bmx.AccelRange_2G)

    def getAllUncalibratedData(self):
        '''
        Updates raw sensor values
        '''
        t = time.ticks_us()
        data = self.bmx.get_all_data()

        self.raw_mag = [data[0]*0.913461, data[1]
                        * 0.913461, (data[2]-1)*2.321809]
        # added constants to make all the mag values in the same range
        self.raw_gyro = [data[3], data[4], data[5]]
        self.raw_accel = [data[6], data[7], data[8]]
        #print(self.raw_accel)
        
        return self.raw_mag,self.raw_gyro,self.accel,t

    def getAllDataCalibrated(self) -> tuple:
        '''
        Returns calibrated values as tuple of ([mag],[gyro],[accel])
        '''
        # Returns tuples Mag,Gyro,Accel
        t = time.ticks_us()
        if (self.init):
            print("Wait for 500ms while initializing the calibration values \n")
            n = 10
            while (n >= 0):
                self.getAllUncalibratedData()
                self.calibrate_accelerometer_readings(self.raw_accel)
                self.calibrate_gyroscope_readings(self.raw_gyro)
                self.calibrate_magnetometer_readings(self.raw_mag)
                time.sleep_ms(50)
                n = n-1
            self.init = False
        else:
            self.getAllUncalibratedData()
            self.calibrate_accelerometer_readings(self.raw_accel)
            self.calibrate_gyroscope_readings(self.raw_gyro)
            self.calibrate_magnetometer_readings(self.raw_mag)

        return (np.normalise(self.mag), self.gyro, self.accel,t)

    def UpdateGyroCalibration(self, duration):
        '''
        Updates the gyro_bias constants. Call this function only when the satellite is at still.
        '''

        # Do not call this function every time this is only for updating the gyro_bias, once it is complete keep calm!
        print("Gyro calib started.. donot nove the sensor")
        gyros_bias = [0, 0, 0]  # Initialize bias values for each axis
        sample_count = 0
        time.sleep(2)
        start_time = time.time()

        while (time.time() - start_time) < duration:
            # Read gyroscope data from the sensor
            data = self.bmx.get_all_data()
            gyro_data = (data[3], data[4], data[5])

            # Accumulate the data for bias calculation
            gyros_bias[0] += gyro_data[0]
            gyros_bias[1] += gyro_data[1]
            gyros_bias[2] += gyro_data[2]

            sample_count += 1
            time.sleep(0.01)  # Add a delay to control the sample rate

        # Calculate the average bias values
        self.gyro_bias[0] = gyros_bias[0] / sample_count
        self.gyro_bias[1] = gyros_bias[1] / sample_count
        self.gyro_bias[2] = gyros_bias[2] / sample_count
        print("Calib ended")
        print("Paste this value in imu.py as gyro_bias = " +
              "["+str(self.gyro_bias)+"]")

    def calibrate_gyroscope_readings(self, raw):
        '''
        Calibrates the gyroscope readings.
        '''
        calibrated_gx = raw[0] - self.gyro_bias[0]
        calibrated_gy = raw[1] - self.gyro_bias[1]
        calibrated_gz = raw[2] - self.gyro_bias[2]
        self.calib_gyro = [calibrated_gx, calibrated_gy, calibrated_gz]
        filtered_gyro_X = self.alpha * calibrated_gx + \
            (1 - self.alpha) * self.gyro[0]
        filtered_gyro_Y = self.alpha * calibrated_gy + \
            (1 - self.alpha) * self.gyro[1]
        filtered_gyro_Z = self.alpha * calibrated_gz + \
            (1 - self.alpha) * self.gyro[2]

        self.gyro = [filtered_gyro_X, filtered_gyro_Y, filtered_gyro_Z]

    def calibrate_accelerometer_readings(self, raw):
        '''
        Calibrates the accelerometer readings.
        '''
        # Define calibration parameters

        # Read raw accelerometer values from the sensor

        # Apply calibration
        cax = 0.0
        cay = 0.0
        caz = 0.0

        for i in range(3):
            calib_value = 0.0
            calib_value += self.A[i][0] * (raw[0] - self.b[0])
            calib_value += self.A[i][1] * (raw[1] - self.b[1])
            calib_value += self.A[i][2] * (raw[2] - self.b[2])

            if i == 0:
                cax = calib_value
            elif i == 1:
                cay = calib_value
            elif i == 2:
                caz = calib_value
        self.calib_accel = [cax, cay, caz]
        # Apply low-pass filter
        self.filtered_cax = self.alpha_accel * cax + \
            (1 - self.alpha_accel) * self.accel[0]
        self.filtered_cay = self.alpha_accel * cay + \
            (1 - self.alpha_accel) * self.accel[1]
        self.filtered_caz = self.alpha_accel * caz + \
            (1 - self.alpha_accel) * self.accel[2]

        # Update previous values
        self.accel = [self.filtered_cax, self.filtered_cay, self.filtered_caz]

    def calibrate_magnetometer_readings(self, raw):
        '''
        Calibrates the magnetometer readings.
        '''
        # Define calibration parameters

        # Read raw accelerometer values from the sensor

        # Apply calibration
        cmx = 0.0
        cmy = 0.0
        cmz = 0.0

        for i in range(3):
            calib_value = 0.0
            calib_value += self.Amag[i][0] * (raw[0] - self.bmag[0])
            calib_value += self.Amag[i][1] * (raw[1] - self.bmag[1])
            calib_value += self.Amag[i][2] * (raw[2] - self.bmag[2])

            if i == 0:
                cmx = calib_value
            elif i == 1:
                cmy = calib_value
            elif i == 2:
                cmz = calib_value
        self.calib_mag = [cmx, cmy, cmz]
        filtered_cmx = self.alpha_mag * cmx + \
            (1 - self.alpha_mag) * self.mag[0]
        filtered_cmy = self.alpha_mag * cmy + \
            (1 - self.alpha_mag) * self.mag[1]
        filtered_cmz = self.alpha_mag * cmz + \
            (1 - self.alpha_mag) * self.mag[2]
        self.mag = [filtered_cmx, filtered_cmy, filtered_cmz]

    def getCalibDataWithoutLowPass(self):
        t = time.ticks_us()
        self.getAllUncalibratedData()
        self.calibrate_accelerometer_readings(self.raw_accel)
        self.calibrate_gyroscope_readings(self.raw_gyro)
        self.calibrate_magnetometer_readings(self.raw_mag)
        return (np.normalise(self.calib_mag), self.calib_gyro, self.calib_accel,t)

