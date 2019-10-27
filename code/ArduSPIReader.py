import serial
import serial.tools.list_ports
import time

ser= serial.Serial()
f = open("data.txt", "w+") #write to file, if not there, create it.

def discovery():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = list(serial.tools.list_ports.comports())
    # Will eventually hold the com port of the detected device, if any
    hooked_port = ""
    for p in available_ports:
        # Do we have a DATAQ Instruments device?
        if ("VID:PID=0403" in p.hwid):
            # Yes!  Dectect and assign the hooked com port
            hooked_port = p.device
            break

    if hooked_port:
        print("Found an ardunio? device on", hooked_port)
        ser.timeout = 0
        ser.port = hooked_port
        ser.baudrate = '9600'
        ser.open()
        return(True)
    else:
        # Get here if no DATAQ Instruments devices are detected
        print("Please connect an ardunio")
        input("Press ENTER to try again...")
        return(False)


discovery()
start_time = time.time()

num = ''
try:
    while True:
        while(ser.inWaiting()>0):
            num += ser.read(1).decode('utf-8')
            if num[-1] == '\n':
                #print(num, str((time.time() - start_time)*1000), 'ms')
                f.write(num.strip()+', '+ str((time.time() - start_time)*1000) + '\n')
                num = ''
finally:
    f.close()
    ser.close()
