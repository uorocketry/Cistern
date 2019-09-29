#testing writing to CSV files. making sure that we can write fast enough.

import time

f = open("test.txt", "w+")#write to file, if not there, create it.

start = time.time()

for i in range(0,40000):
    f.write(str(i) + ";\n") #note, to get this speed, we can't
                            #print every piece of data we get.


end = time.time()

print("it took", (end-start)*1000, "ms to write all the data.")

f.write(str((start-end)*1000))
f.close()
