import pandas as pd
import os
import sys

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 10)

# Set working directory to script path
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

# Load CSDB df
csdb_df = pd.read_csv("../csdb/dat/CSDB_slice_for_Ida.txt",
                      dtype={'pmid':'object', 'CSDB_record_ID': 'object', 'CSDB_nonpersistent_article_ID':'object'},
                      sep = '\t')

# Read polymerase tsv
polymerase_df = pd.read_csv("../data/combined_polymerases.tsv", sep = '\t')
# Make id column
polymerase_df['id'] = polymerase_df['species'].astype('str') + polymerase_df['serotype'].astype('str')
polymerase_df.drop(['csdb_structure_id', 'csdb_record_id', 'csdb_glycan', 'original_sequence'], axis=1, inplace=True)

# Make new dataframe
data = []
row_id_done = []
for index, row in polymerase_df.iterrows():
    rows_condition_true = csdb_df[(csdb_df.Taxonomic_name == row.species) & (csdb_df.Strain_or_Serogroup == row.serotype)]
    if len(rows_condition_true) > 0 and row.id not in row_id_done:
        data.append(list(rows_condition_true.iloc[0])+[row.id])
        row_id_done.append(row.id)
new_df = pd.DataFrame(data, columns=list(csdb_df.columns)+['id'])
new_df.drop(['Taxonomic_name', 'Strain_or_Serogroup'], axis = 1, inplace = True)

# Join dataframes
merged = pd.merge(polymerase_df, new_df, on='id', how='left')

# Write to file
merged.to_csv("../data/combined_polymerases_with_csdb.tsv", sep = '\t', index = False)