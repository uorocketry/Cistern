
class pressure(object):
    def Init(self, port):
        ''' I2C port -> bool
            initalizes the pressure sensor on the I2C bus.
            Returns True if successful, False otherwise.'''


        return True

    def readvals(self):
        '''None -> float [or possibly list]
        Returns the value sensed by the sensor.'''

        return 0.5
