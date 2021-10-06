import json
import pandas as pd
import re

# Read json
json_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/210930_BCSDB_parsed/a_baumanii.json", 'r')
json_baumanii = json.load(json_file)
mydict = dict()
for i in json_baumanii:
    # Make dict for this entry
    entry_dict = dict()
    for j in i:
        key = j['key']
        value = j['value']
        entry_dict[key] = value
    x = re.search("(Sv\d+)", entry_dict['taxon'])
    serotype = x[0]
    mydict[serotype] = entry_dict

# Make into pandas dataframe
repeating_unit_df = pd.DataFrame.from_dict(mydict).T

# Open outfile
db_file = "C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases.tsv"
df = pd.read_csv(db_file, sep='\t')
#df.repeating_unit = 
#print(list(repeating_unit_df.index))
repeating_unit_df['Current_Serovar'] = list(repeating_unit_df.index)
#print(repeating_unit_df.Current_Serovar)
#merged_df = pd.merge(df, repeating_unit_df, on='Current_Serovar')

merged_df = df.merge(repeating_unit_df, how='left', on='Current_Serovar')
pd.set_option('display.max_columns', 500)
#print(repeating_unit_df)
print(merged_df)

merged_df.to_csv("C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases_new.tsv", sep='\t')