import serial
import serial.tools.list_ports
import keyboard
import time
import configparser
import threading
import queue

from sensors.Thermo_MAX31855 import thermo
from sensors.dataq import dataq

dataq = dataq()
thermo = Thermo(1,0)

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

    return dataq.out.get().append(thermo.read())




init()

#while 'button not pushed':
#    'read button'

start_time = time.time()
counter = 0
data = []
dataq.go()
#this will eventually prevent button bouncing. currently does 5 secs of reading.
#while time.time()-start_time <= 10 or not 'button pushed':
while True:
    #time.sleep(0.001)
    d = read()
    #print(d[-1])

    if d[4] > 0: # If the digital out(the event buttons) get pushed, exit.
        break

    data.append(d)
    counter +=1
    if counter>= 10:

        "write data to file"
        f.writelines(str(i) + '\n' for i in data)
        counter = 0
        data = []

dataq.stop()
f.writelines(str(i) + '\n' for i in data)

f.close()
