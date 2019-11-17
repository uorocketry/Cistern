
import serial
import serial.tools.list_ports
import keyboard
import time

#min SAMPLE_RATE =  1500 with 1 channel,
#                   2000 with 2 channels,
#                   2500 with 3 channels,
#                   3000 with 4 channels active.
#max SAMPLE_RATE =  65535
#the effective sample rate (in Hz) is 60,000,000/(SAMPLE_RATE).
SAMPLE_RATE = 60000

"""
Example slist for model DI-1100
0x0000 = Analog channel 0, ±10 V range
0x0001 = Analog channel 1, ±10 V range
0x0002 = Analog channel 2, ±10 V range
0x0003 = Analog channel 3, ±10 V range
"""
slist = [0x0000,0x0001,0x0002,0x0003]

# Configure the instrment's scan list
def config_scn_lst():
    #TODO: determie possible values, understand this command further.
    # Scan list position must start with 0 and increment sequentially
    position = 0
    for item in slist:
        send_cmd("slist "+ str(position ) + " " + str(item))
        # Add the channel to the logical list.
        #achan_accumulation_table.append(0)
        position += 1

""" Discover DATAQ Instruments devices and models.
Note that if multiple devices are connected, only the
device discovered first is used."""

def discover(ser):
    have_device = False
    while not have_device:
        # Get a list of active com ports to scan for possible DATAQ Instruments devices
        available_ports = list(serial.tools.list_ports.comports())
        # Will eventually hold the com port of the detected device, if any
        hooked_port = ""
        for p in available_ports:
            # Do we have a DATAQ Instruments device?
            if ("VID:PID=0683" in p.hwid):
                # Yes!  Dectect and assign the hooked com port
                hooked_port = p.device
                break

        if hooked_port:
            print("Found a DATAQ Instruments device on",hooked_port)
            ser.timeout = 0
            ser.port = hooked_port
            ser.baudrate = '115200'
            ser.open()
            have_device = True
        else:
            # Get here if no DATAQ Instruments devices are detected
            print("Please connect a DATAQ Instruments device")
            input("Press ENTER to try again...")
            have_device = False
#
# Sends a passed command string after appending <cr>
def send_cmd(command):
    ser.write((command+'\r').encode())
    time.sleep(.1)
    # if not(acquiring):
    #     # Echo commands if not acquiring
    #     while True:
    #         if(ser.inWaiting() > 0):
    #             while True:
    #                 try:
    #                     s = ser.readline().decode()
    #                     s = s.strip('\n')
    #                     s = s.strip('\r')
    #                     s = s.strip(chr(0))
    #                     break
    #                 except:
    #                     continue
    #             if s != "":
    #                 print (s)   #printing the command we are sending,
    #                 break       #can probably be removed at some point.





ser = serial.Serial()

discover(ser) #find the DAC, and connect to it.

# Stop in case DI-1100 is already scanning
send_cmd("stop")
# Define binary output mode
send_cmd("encode 0")
# Keep the packet size small for responsiveness
send_cmd("ps 0")
# Configure the instrument's scan list

config_scn_lst()



f = open("data.txt", "w+") #write to file, if not there, create it.

# Define flag to indicate if we are currently acquiring data
acquiring = False
# This is the main program loop, broken only by typing a command key as defined
while True:
    # If key 'G' start scanning
    if keyboard.is_pressed('g' or  'G'):
         keyboard.read_key()
         acquiring = True

         send_cmd("start")
    # If key 'S' stop scanning
    if keyboard.is_pressed('s' or 'S'):
         keyboard.read_key()
         send_cmd("stop")
         time.sleep(1)
         ser.flushInput()
         print ("")
         print ("stopped")

         acquiring = False
    # If key 'Q' exit
    if keyboard.is_pressed('q' or 'Q'):
         keyboard.read_key()
         send_cmd("stop")
         ser.flushInput()
         f.close() #close the file.
         break
    # This is the slist position pointer. Ranges from 0 (first position)
    # to len(slist). Tells us what channel we are currently reading.
    slist_pointer = 0
#while the # of bytes ready to be read is greater than the number of bytes in
    while (ser.inWaiting() > (2 * len(slist))): # a message, read them.

        output_string = ""
        for i in range(len(slist)):

            # Always two bytes per sample...read them
            bytes = ser.read(2)
            # Only analog channels for a DI-1100, with digital_in states
            #appearing in the two LSBs of ONLY the first slist position
            result = int.from_bytes(bytes,byteorder='little', signed=True)

            # Since digital input states are embedded into the
            #analog data stream there are two possibilities:
            if (slist_pointer == 0):
                # first slist position
                # Two LSBs carry information only for first slist posiiton.
                # So... Preserve lower two bits representing digital input states
                dig_in = result & 0x3
                # Strip two LSBs from value to be added to the analog
                #channel accumulation, preserving sign
                result = result >> 2
                result = result << 2

                output_string = str(round(result/32768,3))

            elif (slist_pointer != 0):
                # NOT the first slist position
                # Two LSBs carry information only for first slist posiiton,
                # which this isn't. So, ...

                output_string = output_string + ", " + str(round(result/32768,3))

            # Get the next position in slist
            slist_pointer += 1

            if (slist_pointer + 1) > (len(slist)):
                # End of a pass through slist items
                # Append digital inputs to output string
                output_string = output_string + ", " + str(dig_in) + "\n"
                #print(output_string.rstrip(", ") + "           ", end="\r\n")
                f.write(output_string)
                output_string = ""
                slist_pointer = 0


ser.close()
SystemExit
