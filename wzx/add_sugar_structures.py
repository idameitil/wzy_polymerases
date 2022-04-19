from heapq import merge
import pandas as pd

polymerase_df = pd.read_csv("../polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep = '\t', dtype=object)
wzz_df = pd.read_csv("wzx.tsv", sep = '\t')

merged_df = pd.merge(wzz_df, polymerase_df, left_on='operon_accession', right_on='dna_accession', how='left', suffixes=('_wzx', '_wzy'))

merged_df['CSDB_record_ID'] = merged_df['CSDB_record_ID'].astype(int, errors='ignore')

merged_df.to_csv("wzx_with_sugars_and_taxonomy.tsv", sep='\t', index=False)