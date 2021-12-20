import sys
from Bio import SeqIO

id_list_file_name = open(sys.argv[1])
outfile = open(sys.argv[2], 'w')
combined_fasta = "data/polymerases_combined.fsa"

# Read combined fasta
combined_dict = {}
for record in SeqIO.parse(open(combined_fasta), 'fasta'):
    combined_dict[record.id] = record.seq

for line in id_list_file_name:
    id = line.strip()
    seq = combined_dict[id]
    outfile.write(f">{id}\n{seq}\n")

outfile.close()
id_list_file_name.close()