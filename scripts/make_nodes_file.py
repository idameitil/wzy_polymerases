import pandas as pd

blast_hits_df = pd.read_csv("unique_blast_hits_Feb16_with_taxonomy.tsv", sep="\t")

annotated_df = pd.read_csv("combined_polymerases_with_taxonomy.tsv", sep='\t')
annotated_df = annotated_df.rename(columns={'protein_accession':'accession'})
colnames_blast_hits = ['accession', 'species', 'annotated', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']
colnames_annotated = ['accession', 'species', 'annotated', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']

new_df = pd.concat([blast_hits_df[colnames_blast_hits], annotated_df[colnames_annotated]])

new_df.to_csv("ssn_nodes.tsv", sep = '\t')