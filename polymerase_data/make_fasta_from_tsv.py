import pandas as pd
import math
tsv_file_df = pd.read_csv("wzy.tsv", sep='\t')
outfile = open("wzy.fasta", "w")

for index, row in tsv_file_df.iterrows():
    accession = row['protein_accession']
    sequence = row['sequence']
    # Check for nan
    try:
        if math.isnan(accession):
            print('No accession')
            continue
    except:
        pass
    # Save to file
    outfile.write(f">{accession}\n{sequence}\n")

outfile.close()