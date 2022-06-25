#Force gauges calibration
#S-gauge
def force1(num):
    return num * 6.235 + 0.0624
# Load cell
def force2(num):
    return num * 1529.0627 - 109.848

#Pressure gauges calibration
#Swagelock: Volt -> PSI
def press1(num):
    return num * 1000

    #return num**2 * 154.76 - num*398.39 + 253.85   # previous calibration

    #if num < 4.616: 
    #    return num * 389.19 - 806.76
    #else: 
    #    return num * 705.86 - 2268.4
#MSP: 
def press2(num):
    return 620.07 * num - 330.083

    #return num * 627.11 - 140.53                    # previous calibration

def format(data, dataq1_len, dataq2_len):
    dq_len = dataq1_len + dataq2_len
    dq_1_len = dataq1_len 
    if dataq1_len != 0:
        dq_len += 2
        dq_1_len += 2
    if dataq2_len != 0:
        dq_len += 2
    
    out = [] 

    if dataq1_len != 0:
        for i in range(dataq1_len):
            num = float(data[i])
            #do conversion here
            if i == 0:
               num = press2(num)
            if i == 1:
                num = press1(num)
            #Not connected currently
            if i == 2:
               num = force1(num)
            if i == 3:
                num = force2(num)
    
            out.append(num)
        
        #Append digital inputs and sample count
        out.append(int(data[dataq1_len]))
        out.append(int(data[dataq1_len + 1]))

    if dataq2_len != 0:
        for i in range(dataq2_len):
            num = float(data[dq_1_len + i])
            # Add new conversion factors here
            if i == 0:
               num = force1(num)
            if i == 1:
                num = force2(num)
            #Not connected currently
            if i == 2:
               num = press1(num)
            if i == 3:
                num = press2(num)
    
            out.append(num)
        
        #Append digital inputs and sample count
        out.append(int(data[dq_1_len + dataq2_len]))
        out.append(int(data[dq_1_len + dataq2_len + 1]))
    
    #Append all temperature probe readings
    out += [data[d] for d in range(dq_len, len(data))]

    return ",".join([str(p) for p in out])


def pretty(data, dataq1_len, dataq2_len):
    out = ""
    if dataq1_len != 0:
        for i in range(dataq1_len):
            num = float(data[i])
            #do conversion for sensors connected to the first Dataq here
            if i == 0:
               num = '{: 3.3f} PSI\t'.format( press2(num))
            if i == 1:
               num = '{: 3.3f} PSI\t'.format( press1(num))
            # Not currently connected
            if i == 2:
               num = '{: 3.3f} Kg\t'.format( force1(num))
            if i == 3:
               num = '{: 3.3f} Kg\t'.format( force2(num))
            out += num
        data = data[dataq1_len:]
        # Copy digital channel + sample count to output
        out += "\t".join(str(d) for d in data[:2])
        data = data[2:]

    if dataq2_len != 0:
        for i in range(dataq2_len):
            num = float(data[i])
            #do conversion for sensors connected to the first Dataq here
            if i == 0:
               num = '{: 3.3f} Kg\t'.format( force1(num))
            if i == 1:
               num = '{: 3.3f} Kg\t'.format( force2(num))
            # Not currently connected
            if i == 2:
               num = '{: 3.3f} PSI\t'.format( press1(num))
            if i == 3:
               num = '{: 3.3f} PSI\t'.format( press2(num))
            out += num
        data = data[dataq2_len:]
        # Copy digital channel + sample count to output
        out += "\t".join(str(d) for d in data[:2])
        data = data[2:]

    # Copy thermo sensors to output unchanged
    return out + "\t" + "\t".join(str(d) for d in data)

