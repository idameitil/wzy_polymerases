from os import listdir
from os.path import isfile, join

path = "C:/Users/s153020/GitHub/wzy_polymerases/kristian/label_files_original/"
label_files = [f for f in listdir(path) if isfile(join(path, f))]

outpath = "C:/Users/s153020/GitHub/wzy_polymerases/data/label_files_accessions/"

for label_file in label_files:
    infile = open(path + label_file, "r")
    outfile = open(outpath + label_file, "w")
    flag = False
    for line in infile:
        if flag:
            splitted_line = line.split('\t')
            ID = splitted_line[0]
            accession = ID.split('-')[0]
            outfile.write(accession + '\t' + '\t'.join(splitted_line[1:]))
        else:
            outfile.write(line)
        if line.strip() == "DATA":
            flag = True
    infile.close()
    outfile.close()