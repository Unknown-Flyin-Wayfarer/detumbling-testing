# BMX160 Imu Calibration Using Pi Pico

## Information
This repo contains method to calibrate the BMX160X imu from bosch sensortec.

## Install & Dependence in pico
- machine
- math
- time

## Datasheets
| Datasheet | Download |
| ---     | ---   |
| BMX160 | [download](https://www.mouser.com/pdfdocs/BST-BMX160-DS000-11.pdf) |
| Pi Pico | [download](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) |
| Pi Pico Pinout | [download](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf) |


## Directory Hierarchy
```
|—— .picowgo
|—— lib
|    |—— bangbang
|        |—— bangbang.py
|    |—— bmx160.py
|    |—— codes.py
|    |—— deltat.py
|    |—— fusion.py
|    |—— imu.py
|    |—— Lora
|        |—— lora.py
|        |—— sx1262.py
|        |—— sx126x.py
|        |—— _sx126x.py
|    |—— npy.py
|    |—— OnBoardComputer.code-workspace
|    |—— pwm
|        |—— pwm.py
|    |—— torquer
|        |—— logger.py
|        |—— torquer.py
|    |—— triad
|        |—— triad.py
|—— main.py
|—— README.md
```
## Code Details
### Tested Platform
- software
  ```
  Python: 3.8.5 (anaconda)
  Micropython
  ```
- hardware
  ```
  Pi Pico H
  ```
 
## References
- [Accelerometer Calibration - Code](https://github.com/michaelwro/accelerometer-calibration)
- [Sensor Fusion Calibration - Code](https://github.com/micropython-IMU/micropython-fusion) 
  
## License
