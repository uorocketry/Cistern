import serial
import serial.tools.list_ports
import keyboard
import time
import configparser
import threading
import queue
import spidev

from sensors.Thermo_MAX31855 import Thermo
from sensors.dataq import dataq

import Format

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0
spi.max_speed_hz = 500000

dataq1 = dataq()
dataq2 = dataq()

thermos = []

config = configparser.ConfigParser()
config.read("config.txt")

f = open("data-"+str(time.time())+".txt", "w+") #write to file, if not there, create it.

def init():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    ports = list(serial.tools.list_ports.comports())
    header = []
    if config['DATAQ']['enabled']=='true':
        if dataq1.Init(config['DATAQ'], ports):
            dataq1_len = int(config['DATAQ']['channel_count'])
            print("Found DATAQ!")
            header += dataq1.send_output_fmt()
        else:
            print("Didn't find DATAQ! Aborting!")
            input("")
            exit()

    if config['DATAQ_2']['enabled']=='true':
        if dataq2.Init(config['DATAQ_2'], ports):
            dataq2_len = int(config['DATAQ_2']['channel_count'])
            print("Found second DATAQ!")
            header += dataq2.send_output_fmt()
        else:
            print("Didn't find second DATAQ! Aborting!")
            input("")
            exit()

    if config['Thermometers']['enabled'] == 'true':
        pins = config['Thermometers']['probes'].split(',')
        thermos = [Thermo(int(x), spi) for x in pins] 
        header += ['Thermo_' + str(x) for x in range(len(pins))] 
    f.write('\t'.join(header) + '\n')

def read():
    '''None -> list of floats
    '''
    dataq1.sendAvg=True

    if dataq2 != None:
        dataq2.sendAvg=True

    # while dataq.sendAvg ==True:
    #     pass
    #     #do nothing

    data = dataq1.out.get() 

    if dataq2 != None:
        data += dataq2.out.get()
    
    data += [thermo.read() for thermo in thermos]

    return data

init()

start_time = time.time()
t = start_time

counter = 0
data = []

dataq1.go()
if dataq2 != None:
    dataq2.go()

try:
    while True: #time.time()-start_time <= 10:
        d = read()

        #Every second, print some data to the file.
        if time.time() - t > 1:
            print(Format.pretty(d, dataq1.channel_count, dataq1.channel_count))
            t = time.time()

        data.append(d)
        counter +=1
        if counter>= 10:
            #write data to file
            f.writelines(str(i) + '\n' for i in data)
            counter = 0
            data = []
except:
    print("Exception caught!")
dataq1.stop()
if dataq2 != None:
    dataq2.stop()

f.writelines(str(i) + '\n' for i in data)
print("Exiting!")
f.close()
