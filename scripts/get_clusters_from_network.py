
network_file = open("ssn/polymerases_all_vs_all_60_feb2.txt", "r")

# Create neighbor dict
neighbor_dict = {}
for line in network_file:
    if line.startswith('source'):
        continue
    splitted_line = line.split('\t')
    first_accession = splitted_line[0]
    second_accession = splitted_line[1]
    if first_accession in neighbor_dict:
        neighbor_dict[first_accession].append(second_accession)
    else:
        neighbor_dict[first_accession] = [second_accession]
    if second_accession in neighbor_dict:
        neighbor_dict[second_accession].append(first_accession)
    else:
        neighbor_dict[second_accession] = [first_accession]
network_file.close()

# Get cluster members
def get_cluster(accession, accessions_cluster, already_done):
    """Recursive function for getting whole cluster"""
    if accession in neighbor_dict:
        neighbor_accessions = neighbor_dict[accession]
        for neighbor_accession in neighbor_accessions:
            accessions_cluster.add(neighbor_accession)
            if neighbor_accession in already_done:
                pass
            else:
                already_done.append(accession)
                get_cluster(neighbor_accession, accessions_cluster, already_done)

# Make fasta
def make_fasta_and_txt(start_accession):
    # Get accession in cluster
    accessions_cluster = set()
    already_done = [start_accession]
    get_cluster(start_accession, accessions_cluster, already_done)

    # Make fasta and accession txt if cluster is bigger that 3
    if len(accessions_cluster) > 3:
        # Make fasta
        combined_fasta = open("data/combined_polymerases.fasta")
        fasta_outfile = open(f"ssn/cluster60/cluster_60_{start_accession}.fasta", "w")
        flag = False
        for line in combined_fasta:
            if line.startswith(">"):
                accession = line.strip()[1:]
                if accession in accessions_cluster:
                    flag = True
                    fasta_outfile.write(line)
                else:
                    flag = False
            else:
                if flag:
                    fasta_outfile.write(line)
        # Make txt
        list_outfile = open(f"ssn/cluster60/cluster_60_{start_accession}.txt", "w")
        for accession in accessions_cluster:
            list_outfile.write(accession+'\n')

    return accessions_cluster

# Run for all clusters in network
accessions_done = []
for start_accession in neighbor_dict:
    if start_accession not in accessions_done:
        accessions_cluster = make_fasta_and_txt(start_accession)
        accessions_done.extend(accessions_cluster)