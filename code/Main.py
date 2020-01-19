import serial
import serial.tools.list_ports
import keyboard
import time
import configparser
import threading
import queue

from sensors.pressure import pressure
from sensors.Thermo_1wire  import thermo
from sensors.dataq import dataq

press = pressure()
dataq = dataq()
thermo = Thermo()

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

    press.Init('temp')
    #Thermo.init - no init, yet.

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

    return dataq.out.get(),




init()

#while 'button not pushed':
#    'read button'

start_time = time.time()
counter = 0
data = []
dataq.go()
#this will eventually prevent button bouncing. currently does 5 secs of reading.
while time.time()-start_time <= 10 or not 'button pushed':
    #time.sleep(0.001)
    d = read()
    #print(d[-1])

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
