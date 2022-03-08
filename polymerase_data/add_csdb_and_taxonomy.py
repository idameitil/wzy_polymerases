from ete3 import NCBITaxa
import pandas as pd

### READ ORIGINAL TSV ###
polymerase_df = pd.read_csv("polymerases.tsv", sep='\t')

### ADD TAXONOMY ###
print('getting taxonomy')
ncbi = NCBITaxa()

def get_taxon(taxid, rank):
    try:
        lineage = ncbi.get_lineage(taxid)
        lineage2ranks = ncbi.get_rank(lineage)
        ranks2lineage = dict((rank, taxid) for (taxid, rank) in lineage2ranks.items())
        taxon = ncbi.get_taxid_translator([ranks2lineage[rank]])[ranks2lineage[rank]]
    except:
        taxon = 'NA'
    return taxon
desired_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
for rank in desired_ranks:
    polymerase_df[rank] = polymerase_df.genbank_taxon.apply(lambda x: get_taxon(x, rank))

### ADD CSDB ###
# Load CSDB df
csdb_df = pd.read_csv("../csdb/dat/CSDB_slice_for_Ida.txt",
                      dtype={'pmid':'object', 'CSDB_record_ID': 'object', 'CSDB_nonpersistent_article_ID':'object'},
                      sep = '\t')
polymerase_df['id'] = polymerase_df['species_original'].astype('str') + polymerase_df['serotype'].astype('str')

# Make new dataframe with csdb info
data = []
row_id_done = []
print('getting csdb')
for index, row in polymerase_df.iterrows():
    rows_condition_true = csdb_df[(csdb_df.Taxonomic_name == row.species) & (csdb_df.Strain_or_Serogroup == row.serotype)]
    if len(rows_condition_true) > 0 and row.id not in row_id_done:
        data.append(list(rows_condition_true.iloc[0])+[row.id])
        row_id_done.append(row.id)
new_df = pd.DataFrame(data, columns=list(csdb_df.columns)+['id'])
new_df.drop(['Taxonomic_name', 'Strain_or_Serogroup'], axis = 1, inplace = True)

# Join dataframes
merged = pd.merge(polymerase_df, new_df, on='id', how='left')

### ADD ANNOTATED COLUMN ###
merged['annotated'] = 1

### WRITE NEW TSV ###
merged.to_csv("polymerases_with_csdb_and_taxonomy.tsv", sep = '\t', index=False)
