#Force gauges calibration
def force1(num):
    return num * 1 + 0
def force2(num):
    return num * 1 + 0

#Pressure gauges calibration
def press1(num):
    return num * 1 + 0
def press2(num):
    return num * 1 + 0

def format(data):
    out = [0,0,0,0]
    #we only want to modify the first four elements. The rest are fine.
    for i in range(4):
        num = float(data[i])
        #do conversion here
        if i == 0:
           num = force1(num)
        if i == 1:
            num = force2(num)
        if i == 2:
           num = press1(num)
        if i == 3:
            num = press2(num)

        out[i] = num
    
    #Append digital inputs and sample count
    out.append(int(data[4]))
    out.append(int(data[5]))

    #Append all 4 temperature probe readings
    out.append(float(data[6]))
    out.append(float(data[7]))
    out.append(float(data[8]))
    out.append(float(data[9]))

    return str(out).strip().strip("[]")


def pretty(data):
    out = ""
    #we only want to modify the first four elements. The rest are fine.
    for i in range(min(4,len(data))):
        num = float(data[i])
        #do conversion here
        if i == 0:
           num = '{: 3.3f} Kg\t'.format( force1(num))
        if i == 1:
           num = '{: 3.3f} Kg\t'.format( force2(num))
        if i == 2:
           num = '{: 3.3f} KPa\t'.format( press1(num))
           #print("Formatting the third one!")
        if i == 3:
           num = '{: 3.3f} KPa\t'.format( press2(num))
           #print("Formatting the fourth one!")
        out =out + num

    return str(out) + "\t".join(str(d) for d in data[4:])
