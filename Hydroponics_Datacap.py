#!/usr/bin/python
import os
import smbus
import bme280
import time

bme_port = 1
bme_address = 0x76
bme_bus = smbus.SMBus(bme_port)

AIR_Temp = WATER_Temp = 0.0

# Create data file
try:
    f = open('/home/pi/hydroponic_tank1_data.csv', 'a+')
    if os.stat('/home/pi/hydroponic_tank1_data.csv').st_size == 0:
        f.write('Date,Time,Water Temp,Air Temp\r\n')
    f.close()
except:
    pass

calibration_params = bme280.load_calibration_params(bme_bus, bme_address)

def get_airtemp(Temp):
# the sample method will take a single reading and return a
# compensated_reading object
   airdata = bme280.sample(bme_bus, bme_address, calibration_params)
   Temp = airdata.temperature
   return (Temp)

def get_watertemp(Temp):
# the sample method will take a single reading and return a
# compensated_reading object
   airdata = bme280.sample(bme_bus, bme_address, calibration_params)
   Temp = airdata.temperature
   return (Temp)


# if airdata.humidity is not None and airdata.temperature is not None:
def output_data(Water_Temp, Air_Temp):
    f = open('/home/pi/hydroponic_tank1_data.csv', 'a+')
    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), Water_Temp, Air_Temp))
#    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), airdata.temperature, airdata.humidity))
    f.close()
    return

AIR_Temp = get_airtemp(AIR_Temp)
WATER_Temp = get_watertemp(WATER_Temp)
output_data(WATER_Temp, AIR_Temp)



