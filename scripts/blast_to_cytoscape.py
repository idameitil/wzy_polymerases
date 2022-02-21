# Takes all-vs-all blast output file and generates a network file for cytoscape
# Each row in the network file is a pair of sequences and their blast score and E-value
# A threshold is used for the blast score

import sys

blast_output = open(sys.argv[1]) # 

threshold = int(sys.argv[2])

outfilename = f"polymerases_all_vs_all_{str(threshold)}_feb10.txt"
outfile = open(outfilename, "w")
outfile.write("source\ttarget\tscore\tevalue\n")

done = []
flag1 = False
flag2 = False
for line in blast_output:
    if line.startswith("Query="):
        query_accession = line.strip()[7:]
        done.append(query_accession)
    elif line.startswith('Sequences producing significant alignments:'):
        flag1 = True
    elif flag1:
        if line.strip() == '':
            flag1 = False
            flag2 = True
    elif flag2:
        if line.strip() == '':
            flag2 = False
        else:
            splitted_line = line.split()
            target_accession = splitted_line[0]
            score = splitted_line[-2]
            e_value = splitted_line[-1]
            if float(score) > threshold and target_accession != query_accession:
                if target_accession not in done:
                    outfile.write(f"{query_accession}\t{target_accession}\t{score}\t{e_value}\n")

outfile.close()