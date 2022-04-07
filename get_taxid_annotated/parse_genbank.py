from asyncio import proactor_events
from Bio import SeqIO
import sys
import pandas as pd

def get_taxon(seq_record):
    taxon = 'NA'
    # Loop over the features
    for feature in seq_record.features:
        # look in source feature
        if feature.type == "source":
            if feature.qualifiers.get("db_xref", []) != []:
                for value in feature.qualifiers.get("db_xref", []):
                    if value.startswith('taxon:'):
                        taxon = value.replace('taxon:', '')
    return taxon

# Parse genbank batch entrez
gb_file = sys.argv[1]
tsv_outfile = open(sys.argv[2], "w")
tsv_outfile.write(f"protein_accession\ttaxon\n")
count_failed = 0
protein_accessions = []
taxons = []
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank"):
    protein_accession = gb_record.annotations['accessions'][0]
    protein_accessions.append(protein_accession)
    taxon = get_taxon(gb_record)
    taxons.append(taxon)
    tsv_outfile.write(f"{protein_accession}\t{taxon}\n")
tsv_outfile.close()
# Make pandas df
taxon_df = pd.DataFrame(list(zip(protein_accessions, taxons)), columns=['protein_accession', 'genbank_taxon'])

# Read tsv
combined_polymerases_df = pd.read_csv('../data/combined_polymerases_with_csdb.tsv', sep='\t')
def clean_accession(acc):
    try:
        return acc.split('.')[0]
    except:
        return ''
combined_polymerases_df.protein_accession = combined_polymerases_df.protein_accession.apply(clean_accession)

# Merge
merged_df = pd.merge(combined_polymerases_df, taxon_df, on="protein_accession", how='left')

merged_df.to_csv('../data/combined_polymerases_with_csdb_and_taxon.tsv', sep='\t', index=False)
