from heapq import merge
import pandas as pd

polymerase_df = pd.read_csv("../polymerase_data/polymerases_with_csdb_and_taxonomy.tsv", sep = '\t')

wzz_df = pd.read_csv("wzz1.tsv", sep = '\t')

merged_df = pd.merge(wzz_df, polymerase_df, left_on='operon_accession', right_on='dna_accession', how='left', suffixes=('_wzz', '_wzy'))


#merged_df['CSDB_record_ID'] = pd.to_numeric(merged_df['CSDB_record_ID'], downcast='integer')
merged_df['CSDB_record_ID'] = merged_df['CSDB_record_ID'].astype(int, errors='ignore')

merged_df.to_csv("wzz_with_sugars_and_taxonomy.tsv", sep='\t', index=False)