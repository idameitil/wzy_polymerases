import pandas as pd
import random

blast_hits_df = pd.read_csv("unique_blast_hits_Feb16_with_taxonomy.tsv", sep="\t")
annotated_df = pd.read_csv("polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep='\t')
annotated_df = annotated_df.rename(columns={'protein_accession':'accession'})

colnames = ['accession', 'species', 'annotated', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']

new_df = pd.concat([blast_hits_df[colnames], annotated_df[colnames]])
"""
# Make taxonomy label files
wanted_ranks = ['species', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']
for rank in wanted_ranks:
    print(rank)
    outfilename = f"label_files_expanded/wzy_{rank}.txt"
    with open(outfilename, "w") as file:
        header = f"DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,{rank}\nCOLOR,#ff0000\nDATA\n"
        file.write(header)
        tax2color = dict()
        accession2tax = dict()
        for index, row in new_df.iterrows():
            acc, tax = row.accession, row[rank]
            if tax not in tax2color:
                color = '#' + "%06x" % random.randint(0, 0xFFFFFF)
                tax2color[tax] = color
            file.write(f"{acc},{tax2color[tax]},{tax}\n")
"""
# Make seed label file
file = open(f"label_files_expanded/wzy_seed.txt", "w")
header = f"DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,SEED\nCOLOR,#ff0000\nDATA\n"
file.write(header)
for index, row in new_df.iterrows():
    seed, acc = row.annotated, row['accession']
    if seed == 1:
        color = "#000000"
    elif seed == 0:
        color = "#FFFFFF"
    else:
        print('error:', seed)
    file.write(f"{acc},{color},{seed}\n")
file.close()