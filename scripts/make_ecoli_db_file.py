
infile = open("data/coli/ecoli_wzy.fsa", "r")
outfile = open("data/coli/ecoli_wzy.tsv", "w")

outfile.write("#id\tserotype\taccession\tsequence\n")

for line in infile:
    if line.startswith(">"):
        _, id, accession, serotype = line[1:].strip().split('_')
    else:
        seq = line.strip()
        outfile.write(f"{id}\t{serotype}\t{accession}\t{seq}\n")

infile.close()
outfile.close()