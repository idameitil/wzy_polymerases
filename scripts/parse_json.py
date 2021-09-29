import json

f = open("C:/Users/s153020/GitHub/wzy_polymerases/data/210928_BCSDB/210928_CSDB_baumanii_Sv.txt")

data = json.load(f)

for i in data:
    print(i)
    print("!!!!!")

