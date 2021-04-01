#!/usr/bin/python
import os
import smbus
import bme280
import time
import glob

bme_port = 1
bme_address = 0x76
bme_bus = smbus.SMBus(bme_port)

AIR_Temp = WATER_Temp = 0.0

# Setup for DS18B20 probe

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


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


# if airdata.humidity is not None and airdata.temperature is not None:
def output_data(Water_Temp, Air_Temp):
    f = open('/home/pi/hydroponic_tank1_data.csv', 'a+')
    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), Water_Temp, Air_Temp))
#    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), airdata.temperature, airdata.humidity))
    f.close()
    return

# Get water temp using DS18B20

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def get_water_temp(WATER_Temp):
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c



AIR_Temp = get_airtemp(AIR_Temp)
WATER_Temp = get_water_temp(WATER_Temp)
output_data(WATER_Temp, AIR_Temp)



