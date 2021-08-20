import serial
import threading
import time
import queue

class dataq(threading.Thread):

    def __init__(self):
        #initalize all stuff here.

        self.active = False
        self.sendAvg = False
        self.avg = 0

        self.out = queue.Queue()
        self.trigger = queue.Queue()

    def Init(self,config,ports):
        self.SAMPLE_RATE = 60000000//(config.getint("sampling_rate")*1000)
        self.decimation_factor = config.getint("decimation_factor")
        self.channel_count = config.getint("channel_count")
        deviceSerial = config["serial_number"]

        self.slist = [0x0000,0x0001,0x0002,0x0003][0:self.channel_count]

        if not self.setSerial(ports, deviceSerial):
            return False
        # Stop in case DI-1100 is already scanning
        self.send_cmd("stop")
        # Define binary output mode
        self.send_cmd("encode 0")
        # Keep the packet size small for responsiveness
        #we can increase this up to 'ps 7', for larger packets, which will prevent the
        #buffer from overflowing.
        self.send_cmd("ps 0")
        # Configure the instrument's scan list
        self.config_scn_lst()

        # Define sample rate = 1 Hz, where decimation_factor = 1000:
        # 60,000,000/(srate) = 60,000,000 / 60000 / decimation_factor = 1 Hz
        self.send_cmd("srate "+ str(self.SAMPLE_RATE))

        return True

    def send_output_fmt(self):
        out = []
        for i in range(self.channel_count):
            out.append("Channel#"+str(i))
        out += ['digital out', 'samples averaged']
        return out

    def setSerial(self, ports, deviceSerial):
        self.ser=serial.Serial()
        for p in ports:
            # Do we have a DATAQ Instruments device?
            if ("VID:PID=0683" in p.hwid and deviceSerial in p.hwid):
                # Yes!  Dectect and assign the hooked com port
                self.ser.timeout = 0
                self.ser.port = p.device
                self.ser.baudrate = 4000000
                self.ser.open()
                print('inwaiting:'+str(self.ser.inWaiting()))
                self.ser.flush()
                self.config_scn_lst()
                return True


        print("couldn't find DATAQ!")
        return False

    def go(self):
        if not self.active:
            threading.Thread.__init__(self)
            self.active = True
            self.send_cmd("start")

            self.start()


    def stop(self):
        if self.active:
            self.send_cmd("stop")
            time.sleep(1)
            print(str(self.ser.inWaiting()))
            self.ser.flushInput()

            self.active = False
            self.join(timeout=1)

    def run(self):
        slist_pointer = 0
        achan_number = 0
        samples = 0
        out_accumulator = [0]*self.channel_count
        while self.active:
            #read values
            channel_number = 0
            while (self.ser.inWaiting()>2*self.channel_count):
                num_bytes = self.ser.inWaiting()
                sets = num_bytes // (2*self.channel_count) #the number of sets to read in at once

                byte_group = self.ser.read(2*self.channel_count*num_bytes)

                for j in range(sets):
                    bytes = byte_group[2*self.channel_count*j:2*self.channel_count*(j+1)]

                    for i in range(self.channel_count):
                        # Always two bytes per sample...read them
                        #bytes = ser.read(2)

                        # Only analog channels for a DI-1100, with digital_in states appearing in the two LSBs of ONLY the first slist position
                        result = int.from_bytes(bytes[i*2:i*2+2],byteorder='little', signed=True)

                        # Since digital input states are embedded into the analog data stream there are four possibilities:
                        if (slist_pointer == 0):
                            samples +=1
                            #first slist position
                            # Two LSBs carry information only for first slist posiiton. So, ...
                            # Preserve lower two bits representing digital input states
                            dig_in = result & 0x3
                            # Strip two LSBs from value to be added to the analog channel accumulation, preserving sign
                            result = result >> 2
                            result = result << 2
                            # Add the value to the accumulator
                            out_accumulator[achan_number] = result + out_accumulator[achan_number]
                            achan_number += 1

                        else: #not at end of slist yet
                            # NOT the first slist position
                            # Two LSBs carry information only for first slist posiiton, which this isn't. So, ...
                            # Just add value to the accumulator
                            out_accumulator[achan_number] = result + out_accumulator[achan_number]
                            achan_number += 1

                        slist_pointer +=1
                        if (slist_pointer + 1) > (self.channel_count):
                            # End of a pass through slist items
                            slist_pointer = 0
                            achan_number = 0

                            #send values, if needed.
                            #if self.trigger.qsize()!=0:
                            if self.sendAvg == True:
                                self.avg = []
                                for i in range(self.channel_count):
                                    self.avg.append(out_accumulator[i] * 10 / 32768 / samples)
                                self.avg.append(dig_in)
                                self.avg.append(samples)
                                self.out.put(self.avg)
                                self.sendAvg = False
                                #self.trigger.get()

                                out_accumulator = [0]*self.channel_count
                                samples = 0




    # Configure the instrment's scan list
    def config_scn_lst(self):
        # Scan list position must start with 0 and increment sequentially
        position = 0
        for item in self.slist:
            self.send_cmd("slist "+ str(position ) + " " + str(item)) # send in format 'slist num config'
            position += 1

    # Sends a passed command string after appending <cr>
    def send_cmd(self,command):
        self.ser.write((command+'\r').encode())
        time.sleep(.1)
        if not(self.active):
            # Echo commands if not acquiring
            while True:
                if(self.ser.inWaiting() > 0):
                    while True:
                        try:
                            s = self.ser.readline().decode()
                            s = s.strip('\n')
                            s = s.strip('\r')
                            s = s.strip(chr(0))
                            break
                        except:
                            continue
                        if s != "":


                            break
                else:
                    break
