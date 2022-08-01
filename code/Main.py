import serial
import serial.tools.list_ports
import socketserver
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
server_enabled = False
items = queue.Queue()

config = configparser.ConfigParser()
config.read("config.txt")

f = open("data-"+str(time.time())+".txt", "w+") #write to file, if not there, create it.

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client

        print("{} connected".format(self.client_address[0]))
        try:
            while True:
                data = items.get(timeout=3)

                dq_chans = 0
                if dataq2 != None:
                    dq_chans = dataq2.channel_count

                d = Format.format(data, dataq1.channel_count, dq_chans) + "\r\n"
                #d = "1,2,3,4,5,6,7,8,9,10,11.0\r\n"

                self.request.sendall(d.encode('utf-8'))

        except(ConnectionResetError, BrokenPipeError):
            pass


def init():
    global thermos, server_enabled, server
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
            #dataq2 = dataq()
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

    server_enabled = False
    if config['Server']['enabled'] == 'true':
        server_enabled = True
        host = config['Server']['host']
        port = config['Server']['port']
        
        server = socketserver.ThreadingTCPServer((host, int(port)), MyTCPHandler)
        server.daemon_threads = True

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    f.write('\t'.join(header) + '\n')

def read():
    '''None -> list of floats
    '''
    dataq1.sendAvg=True

    if dataq2 != None:
        dataq2.sendAvg=True

    data = dataq1.out.get() 

    if dataq2 != None:
        data += dataq2.out.get()
    
    data += [thermo.read() for thermo in thermos]

    data += [int((time.time()-start_time)*1000)]
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
    while True:
        d = read()
        data.append(d)

        if server_enabled:
            items.put_nowait(d)

        counter += 1
        if counter >= 10:
            #Write data to file
            f.writelines(str(i) + '\n' for i in data)

            dq_chans = 0
            if dataq2 != None:
                dq_chans = dataq2.channel_count

            print(Format.pretty(d, dataq1.channel_count, dq_chans))

            counter = 0
            data = []

        remaining = 0.1 - (time.time() - t)
        if remaining > 0:
            time.sleep(remaining)
        t = time.time()

except:
    print("Exception caught!")
dataq1.stop()
if dataq2 != None:
    dataq2.stop()

if server_enabled:
    server.shutdown()

f.writelines(str(i) + '\n' for i in data)
print("Exiting!")
f.close()
