import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_excel("data/shigella/shigella_original_table2.xlsx")

new_df = df[df['Gene identifier(s)'] == 'wzy']['Accession no.']

new_df.to_csv(r'data/shigella/operon_accession_list.txt', header=None, index=None, sep=' ', mode='a')