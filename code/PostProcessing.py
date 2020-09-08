import Format


infile_name = input("File to postprocess: ")

infile = open(infile_name, mode='r')
outfile = open("post_" + infile_name, mode='w')

line = infile.readline() #skip the first line - it has the labels.
line = infile.readline()
while line:
    data = line.strip().strip("[]").split(",")

    outfile.write(Format.format(data) + "\n")
    line = infile.readline()

infile.close()
outfile.close()

