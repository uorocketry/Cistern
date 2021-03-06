import time
import spidev
import gpiozero

class Thermo:
    #def __init__(self, bus, device):
    def __init__(self, pin, spi):
        self.spi = spi
        
        
        self.ce = gpiozero.DigitalOutputDevice(pin, active_high=False,initial_value=True)



    def read(self):
        self.ce.on()  #We control the chip enable pin manually. 
        data = self.spi.readbytes(4)  #read 32 bits from the interface.
        self.ce.off()

        data = int.from_bytes(data, "big")

        # We now decode the bits to get the temperature.
        # Go to https://cdn-shop.adafruit.com/datasheets/MAX31855.pdf
        # to get the datasheet. Page 10 contains the
        # description of the format of the data.

        if data & (0b1<<31): #negative! drop the lower 18 bits and extend the sign.
            #bit twiddling to get the bits we want.
            #We first find and separate the
            #bits containing the temperature data,
            #then we xor it with all 1's (to flip it from positive to negative) and add 1, then convert
            # to a negative number within python (because python ints are weird).
            # we then divide by 4, because the lcb of this int represents 0.25C.
            return (~((data >> 18) ^ 0b111111111111111)+1)/4
        else:
            #since it's positive, we don't convert to negative. We just separate
            #out the temperature.
            return (data >> 18) / 4
