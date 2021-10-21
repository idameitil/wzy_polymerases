
# outfile = open("C:/Users/s153020/GitHub/wzy_polymerases/data/itol_label_files_accessions/wzy1_image.txt", "w")

# outfile.write("DATASET_IMAGE\nSEPARATOR TAB\nDATASET_LABEL\timage\nCOLOR\t#ff0000\n")
# outfile.write("MARGIN\t0\nSHOW_INTERNAL\t0\nIMAGE_ROTATION\t0\nIMAGE_SHIFT_V\t0\n")
# outfile.write("IMAGE_SHIFT_H\t0\nSIZE_FACTOR\t1\nDATA")

# Make acinetobacter dict
acinetobacter_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases.tsv", "r")
acinetobacter_dict = dict()
for line in acinetobacter_file:
    splitted_line = line.split('\t')
    if len(splitted_line) == 1:
        continue
    if not splitted_line[1].startswith('LUH'):
        continue
    pol_accession = splitted_line[9]
    CSDB_ID = splitted_line[13]
    acinetobacter_dict[pol_accession] = CSDB_ID
    
# Make yersinia dict
yersinia_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/pseudotuberculosis/pseudotuberculosis_polymerases.tsv", "r")
yersinia_dict = dict()
for line in yersinia_file:
    splitted_line = line.split('\t')
    if len(splitted_line) == 1:
        continue
    if not splitted_line[1].startswith('O:'):
        continue
    pol_accession = splitted_line[4]
    if splitted_line[6] == '':
        CSDB_ID = ''
    else:
        CSDB_ID = str(int(float(splitted_line[6])))
    yersinia_dict[pol_accession] = CSDB_ID

# Make streptococcus dict
streptococcus_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/pneumoniae/pneumoniae_polymerases.tsv", "r")
streptococcus_dict = dict()
for line in streptococcus_file:
    splitted_line = line.split('\t')
    if len(splitted_line) == 1:
        continue
    elif splitted_line[1] == 'serotype':
        continue
    pol_accession = splitted_line[5]
    if splitted_line[6] == '':
        CSDB_ID = ''
    else:
        CSDB_ID = str(int(float(splitted_line[6])))
    streptococcus_dict[pol_accession] = CSDB_ID

tmpfile = open("C:/Users/s153020/GitHub/wzy_polymerases/data/tmp.txt", "r")
outfile = open("C:/Users/s153020/GitHub/wzy_polymerases/data/tmp2.txt", "w")
for line in tmpfile:
    accession, path = line.strip().split('\t')
    if line.startswith('AHB'):
        CSDB_ID = acinetobacter_dict[accession]
    elif line.startswith('CAI'):
        CSDB_ID = streptococcus_dict[accession]
    else:
        CSDB_ID = yersinia_dict[accession]
    if CSDB_ID != '':
        outfile.write(f'{accession}\t{path}{CSDB_ID}.gif\n')