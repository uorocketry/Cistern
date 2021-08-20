import configparser
import sys

import Format

config = configparser.ConfigParser()
config.read("config.txt")

dataq1_len = 0
dataq2_len = 0

if config['DATAQ']['enabled'] == 'true':
    dataq1_len = int(config['DATAQ']['channel_count'])
if config['DATAQ_2']['enabled'] == 'true':
    dataq1_len = int(config['DATAQ_2']['channel_count'])

infile_name = ""
outfile_name = ""
if len(sys.argv) > 1:
    infile_name = sys.argv[1]
else: 
    infile_name = input("File to postprocess: ")

if len(sys.argv) > 2:
    outfile_name = sys.argv[2]
else:
    outfile_name = "post_" + infile_name

infile = open(infile_name, mode='r')
outfile = open(outfile_name, mode='w')

outfile.write(infile.readline()) #Copy the first line (with the labels) to the output file
line = infile.readline()
while line:
    data = line.strip().strip("[]").split(",")

    outfile.write(Format.format(data, dataq1_len, dataq2_len) + "\n")
    line = infile.readline()

infile.close()
outfile.close()

