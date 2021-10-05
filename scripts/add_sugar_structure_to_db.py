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
    
for ket in mydict:
    print(ket)
# Open outfile
#db_file = open("C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases.tsv", "r")
#db_file.close()
db_file = "C:/Users/s153020/GitHub/wzy_polymerases/data/baumanii/baumanii_polymerases.tsv"
df = pd.read_csv(db_file, sep='\t')

#print(df.Current_Serovar)