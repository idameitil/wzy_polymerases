import sys
phobius = {}

# Protein accessions (names in AF models)
AF_accessions = ["EHX11459.1", "CAI32705.1", "BAQ00736.1", "AHB32386.1", "CAI33105.1", \
                 "CAB63298.1", "AHB32538.1", "ADX97403.1", "EKI95922.1", "CAI32772.1", \
                 "BAQ02224.1", "AHB32490.1", "ACD37165.1"]

# Translation (with DNA accessions)
translation_dict = {"EHX11459.1": "AIGX01000028", "CAI32705.1":"CAI32705.1", \
                    "BAQ00736.1":"AB811606", "AHB32386.1": "AHB32386.1", \
                    "CAI33105.1":"CAI33105.1", "CAB63298.1":"CAB63298.1",\
                    "AHB32538.1":"AHB32538.1", "ADX97403.1":"ADX97403.1",\
                    "ADX97403.1":"ADX97403.1", "EKI95922.1":"JH953200", \
                    "CAI32772.1": "CAI32772.1", "BAQ02224.1":"AB972419",\
                    "AHB32490.1":"AHB32490.1", "ACD37165.1":"EU296422-EU296423"}

AF_accessions_phobius = ["AIGX01000028", "CAI32705.1", "AB811606", "AHB32386.1", "CAI33105.1", \
                 "CAB63298.1", "AHB32538.1", "ADX97403.1", "JH953200", "CAI32772.1", \
                 "AB972419", "AHB32490.1", "EU296422-EU296423"]

# Parse Phobius
with open("phobius.txt") as handle:
    for line in handle:
        # Find accession:
        if "Prediction of " in line:
            acc = line.strip("Prediction of ").strip("\n")
            if acc in AF_accessions_phobius:
                outfile.write(f"{acc}\n")
        elif line[:2] == "FT":
            splitted_line = line.strip("\n").strip(".").split()
            start, end, type, cyto = int(splitted_line[2]), int(splitted_line[3]), \
                                     splitted_line[1], "_".join(splitted_line[4:])
            if type == 'TRANSMEM':
                # Save in dict
                if acc in AF_accessions_phobius:
                    if acc in phobius:
                        phobius[acc] += list(range(start, end))
                    else:
                        phobius[acc] = list(range(start, end))

# Write Phobius to PDB
for accession in AF_accessions:
    pdb = f"data/AF_rank1_relaxed/{accession}.pdb"
    out_pdb = open(f"data/AF_rank1_relaxed_phobius/{accession}.pdb", "w")
    with open(pdb) as handle:
        phobius_accession = translation_dict[accession]
        for line in handle:
            if line.startswith('ATOM'):
                splitted_line = line.split()
                residue_position = splitted_line[5]
                if int(residue_position) in phobius[phobius_accession]:
                    transmembrane = '1    '
                else:
                    transmembrane = '0    '
                out_pdb.write(line[:61]+transmembrane+line[66:])
            else:
                out_pdb.write(line)
    out_pdb.close()