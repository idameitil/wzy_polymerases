import json
import pandas as pd
import re

# Read json
#json_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/210930_BCSDB_parsed/a_baumanii.json", 'r')
json_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/210930_BCSDB_parsed/s_pneumoniae.json", 'r')
#json_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/210930_BCSDB_parsed/y_pseudotuberculosis.json", 'r')
json_csdb = json.load(json_file)
mydict = dict()
for i in json_csdb:
    # Make dict for this entry
    entry_dict = dict()
    for j in i:
        key = j['key']
        value = j['value']
        entry_dict[key] = value
    #x = re.search("(Sv\d+)", entry_dict['taxon']) # for baumanii
    x = re.search("_:(taxon|organism)_Streptococcus_pneumoniae(_type)?_(.+)$", entry_dict['taxon'])
    #x = re.search("_:(taxon|organism)_Yersinia_(pseudotuberculosis|similis)(_type)?_(.+)$", entry_dict['taxon'])
    if x is None:
        if entry_dict['record_id'] == "12123":
            serotype = 'O:1b'
    else:
        serotype = x[3]
    print(serotype)
    mydict[serotype] = entry_dict

# Make into pandas dataframe
repeating_unit_df = pd.DataFrame.from_dict(mydict).T

# Open outfile
#db_file = "C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases.tsv"
db_file = "C:/Users/s153020/GitHub/wzy_polymerases/data/pneumoniae/pneumoniae_polymerases.tsv"
#db_file = "C:/Users/s153020/GitHub/wzy_polymerases/data/pseudotuberculosis/pseudotuberculosis.txt"
df = pd.read_csv(db_file, sep='\t')
#repeating_unit_df['Current_Serovar'] = list(repeating_unit_df.index)
repeating_unit_df['serotype'] = list(repeating_unit_df.index)
#repeating_unit_df['Serotype'] = list(repeating_unit_df.index)

#merged_df = df.merge(repeating_unit_df, how='left', on='Current_Serovar')
merged_df = df.merge(repeating_unit_df, how='left', on='serotype')
#merged_df = df.merge(repeating_unit_df, how='left', on='Serotype')
pd.set_option('display.max_columns', 500)

merged_df.to_csv("C:/Users/s153020/GitHub/wzy_polymerases/data/pneumoniae/pneumoniae_polymerases_new.tsv", sep='\t')
#merged_df.to_csv("C:/Users/s153020/GitHub/wzy_polymerases/data/pseudotuberculosis/pseudotuberculosis_polymerases.tsv", sep='\t')