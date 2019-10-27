

infile_name = input("File to postprocess: ")

infile = open(infile_name, mode='r')
outfile = open("post_" + infile_name, mode='w')

line = infile.readline()
while line:
    outfile.write(line.strip().strip("[]")+"\n")
    line = infile.readline()

infile.close()
outfile.close()
