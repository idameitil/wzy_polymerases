import pandas as pd
import math
import sys
infilename = sys.argv[1]
outfilename = sys.argv[2]
tsv_file_df = pd.read_csv(infilename, sep='\t')
outfile = open(outfilename, "w")

accessions_done = set()

for index, row in tsv_file_df.iterrows():
    accession = row['protein_accession']
    if accession in accessions_done:
        continue
    accessions_done.add(accession)
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