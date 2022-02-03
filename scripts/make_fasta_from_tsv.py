import pandas as pd
import math
tsv_file_df = pd.read_csv("data/combined_polymerases.tsv", sep='\t')
outfile = open("data/combined_polymerases.fasta", "w")

for index, row in tsv_file_df.iterrows():
    accession = row['protein_accession']
    species = row['species']
    sequence = row['sequence']
    # Check for nan
    try:
        if math.isnan(accession):
            print('hej')
            continue
    except:
        pass
    # Save to file
    outfile.write(f">{accession}\n{sequence}\n")

outfile.close()