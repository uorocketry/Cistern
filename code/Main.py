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

dataq = dataq()
thermo1 = Thermo(23, spi)
thermo2 = Thermo(24, spi)
thermo3 = Thermo(25, spi)
thermo4 = Thermo(16, spi)

config = configparser.ConfigParser()
config.read("config.txt")

f = open("data-"+str(time.time())+".txt", "w+") #write to file, if not there, create it.

def init():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    ports = list(serial.tools.list_ports.comports())

    if dataq.Init(config['DATAQ'], ports):
        print("Found DATAQ!")
        f.write(dataq.send_output_fmt()+"\n")
    else:
        print("Didn't find DATAQ! Aborting!")
        input("")
        exit()

#def read_dataq():


def read():
    '''None -> list of floats
    '''
    #press.readvals()
    #return dataq.readvals()
    #dataq.trigger.put(1)
    dataq.sendAvg=True

    # while dataq.sendAvg ==True:
    #     pass
    #     #do nothing

    data = dataq.out.get() 
    data.append(thermo1.read())
    data.append(thermo2.read())
    data.append(thermo3.read())
    data.append(thermo4.read())
    return data



init()

#while 'button not pushed':
#    'read button'

start_time = time.time()
t = start_time

counter = 0
data = []
dataq.go()

try:
    while True: #time.time()-start_time <= 10:
        #time.sleep(0.001)
        d = read()

        #Every second, print some data to the file.
        if time.time() - t > 1:
            print(Format.pretty(d))
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
dataq.stop()
f.writelines(str(i) + '\n' for i in data)
print("Exiting!")
f.close()
