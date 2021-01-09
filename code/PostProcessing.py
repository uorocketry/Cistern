import Format

import sys

infile_name = ""

if len(sys.argv) == 2:
    infile_name = sys.argv[1]
else:
    infile_name = input ("File to postprocess: ")

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
