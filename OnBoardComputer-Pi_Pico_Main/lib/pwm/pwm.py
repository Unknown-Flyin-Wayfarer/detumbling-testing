import machine 
import time

# Define the PWM pin numbers for each pair
x_positive_pin = 2
x_negative_pin = 3
y_positive_pin = 4
y_negative_pin = 5
z_positive_pin = 6
z_negative_pin = 7

# Create PWM objects for each pin
x_positive_pwm = machine.PWM(machine.Pin(x_positive_pin))
x_negative_pwm = machine.PWM(machine.Pin(x_negative_pin))
y_positive_pwm = machine.PWM(machine.Pin(y_positive_pin))
y_negative_pwm = machine.PWM(machine.Pin(y_negative_pin))
z_positive_pwm = machine.PWM(machine.Pin(z_positive_pin))
z_negative_pwm = machine.PWM(machine.Pin(z_negative_pin))

# Set the PWM frequency
pwm_freq = 128
x_positive_pwm.freq(pwm_freq)
x_negative_pwm.freq(pwm_freq)
y_positive_pwm.freq(pwm_freq)
y_negative_pwm.freq(pwm_freq)
z_positive_pwm.freq(pwm_freq)
z_negative_pwm.freq(pwm_freq)

# Enable the PWM outputs
x_positive_pwm.enable()
x_negative_pwm.enable()
y_positive_pwm.enable()
y_negative_pwm.enable()
z_positive_pwm.enable()
z_negative_pwm.enable()

# Function to control the x pair PWMs
def control_x_pair(value):
    if value < 0:
        x_positive_pwm.duty_u16(0)
        x_negative_pwm.duty_u16(int(abs(value) * 65535))
    else:
        x_positive_pwm.duty_u16(int(value * 65535))
        x_negative_pwm.duty_u16(0)

# Function to control the y pair PWMs
def control_y_pair(value):
    if value < 0:
        y_positive_pwm.duty_u16(0)
        y_negative_pwm.duty_u16(int(abs(value) * 65535))
    else:
        y_positive_pwm.duty_u16(int(value * 65535))
        y_negative_pwm.duty_u16(0)

# Function to control the z pair PWMs
def control_z_pair(value):
    if value < 0:
        z_positive_pwm.duty_u16(0)
        z_negative_pwm.duty_u16(int(abs(value) * 65535))
    else:
        z_positive_pwm.duty_u16(int(value * 65535))
        z_negative_pwm.duty_u16(0)
def setTorquerValue(value:list|tuple):
    val = list(value)
    for x in range(3):
        if val[x]>1:
            val[x]=1
    control_x_pair(val[0])  
    control_y_pair(val[1])  
    control_z_pair(val[2]) 
# Example usage of the functions
while True:
    setTorquerValue([0,2.3,4])
    time.sleep(1)
