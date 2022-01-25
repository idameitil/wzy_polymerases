import pandas as pd
tsv_file_df = pd.read_csv("data/combined_polymerases.tsv", sep='\t')
outfile = open("combined_polymerases.fasta", "w")

for index, row in tsv_file_df.iterrows():
    accession = row['protein_accession']
    species = row['species']
    sequence = row['sequence']
    outfile.write(f">{accession}|{species}\n{sequence}\n")

outfile.close()