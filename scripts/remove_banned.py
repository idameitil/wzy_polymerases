import sys

original_list_path = sys.argv[1]
banned_list_path = sys.argv[2]
outfile_path = sys.argv[3]

# Make list of banned
banned = list()
banned_list_file = open(banned_list_path, "r")
for line in banned_list_file:
    ID = line.strip()
    banned.append(ID)
banned_list_file.close()

# Write outfile
outfile = open(outfile_path, "w")
original_list_file = open(original_list_path, "r")

for line in original_list_file:
    if line.startswith(">"):
        original_ID = line.strip().replace(">", "")
        if original_ID not in banned:
            outfile.write(line)
    else:
        if original_ID not in banned:
            outfile.write(line)

outfile.close()
original_list_file.close()