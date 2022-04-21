import pandas as pd
import random
import sys

blast_hits_df = pd.read_csv("unique_blast_hits_Feb16_with_taxonomy.tsv", sep="\t")
annotated_df = pd.read_csv("polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep='\t')
annotated_df = annotated_df.rename(columns={'protein_accession':'accession'})

annotated_df.rename(columns={'sequence':'seq'}, inplace=True)

colnames = ['accession', 'species', 'annotated', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'seq']

new_df = pd.concat([blast_hits_df[colnames], annotated_df[colnames]])

new_df['length'] = new_df.seq.apply(lambda x: len(x))

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


from colour import Color
red = Color("white")
n = 500-320
colors = list(red.range_to(Color("black"),n))
# Make length label file
file = open(f"label_files_expanded/wzy_length.txt", "w")
header = f"DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,length\nCOLOR,#ff0000\nDATA\n"
file.write(header)
for index, row in new_df.iterrows():
    length, acc = row.length, row['accession']
    if length > 500:
        color = colors[0]
    elif length < 320:
        color = colors[n-1]
    else:
        color=colors[length-320-1].hex
        file.write(f"{acc},{color},{length}\n")
file.close()


infile = open("100_wzy_polymerases_for_AF.txt")
modeled = list()
for line in infile:
    modeled.append(line.strip())

new_df['modeled'] = new_df.accession.apply(lambda x: 1 if x in modeled else 0)

file = open(f"label_files_expanded/wzy_alphafold.txt", "w")
header = f"DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,alphafold\nCOLOR,#ff0000\nDATA\n"
file.write(header)
for index, row in new_df.iterrows():
    modeled, acc = row.modeled, row['accession']
    if modeled == 1:
        color = "#00ff00"
    elif modeled == 0:
        color = "#FFFFFF"
    else:
        print('error:', modeled)
    file.write(f"{acc},{color},{modeled}\n")
file.close()