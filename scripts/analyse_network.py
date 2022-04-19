import os
import sys
import pandas as pd
import random

RUN = f'/work3/idamei/wzy_ssn/run'
# The string 'THR' and 'CLUSTER' in this blast string will be substituted by
jobscript=f"""#! /bin/sh 
### General options 
### -- specify queue -- 
#BSUB -q hpc
### -- set the job Name -- 
#BSUB -J muscle_THR_CLUSTER
### -- ask for number of cores (default: 1) -- 
#BSUB -n 1 
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 5GB of memory per core/slot -- 
#BSUB -R "rusage[mem=5GB]"
### -- specify that we want the job to get killed if it exceeds 5 GB per core/slot -- 
#BSUB -M 5GB
### -- set walltime limit: hh:mm -- 
#BSUB -W 10:00 
### -- set the email address -- 
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
#BSUB -u idamei@dtu.dk
### -- send notification at start -- 
#BSUB -B 
### -- send notification at completion -- 
#BSUB -N 
### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -o {RUN}/EXP_THR/run/SSN_THR/MSA_jobscripts/CLUSTER.out
#BSUB -e {RUN}/EXP_THR/run/SSN_THR/MSA_jobscripts/CLUSTER.err
# here follow the commands you want to execute 
/work3/idamei/bin/muscle5.1.linux_intel64 -align {RUN}/EXP_THR/run/SSN_THR/fastas/CLUSTER.fa -output {RUN}/EXP_THR/run/SSN_THR/MSAs/CLUSTER.afa
python2 /work3/idamei/bin/seq2logo-2.1/Seq2Logo.py -f {RUN}/EXP_THR/run/SSN_THR/MSAs/CLUSTER.afa -o {RUN}/EXP_THR/run/SSN_THR/logos/CLUSTER.logo 
"""

# Make network files
def make_network_file(threshold):

    outfilename = output_name(expansion_threshold, ssn_threshold)

    if os.path.exists(outfilename):
        sys.stderr.write(f"Skipping creation of network file for threshold {threshold}. Already exists.\n")
        return

    outfile = open(outfilename, "w")
    outfile.write("source\ttarget\tscore\tevalue\n")

    done = []
    header_hit_list = False
    hit_list_section = False
    infile = open(blast_file)
    for line in infile:
        # Query accession line
        if line.startswith("Query="):
            query_accession = line.strip()[7:]
            done.append(query_accession)
        # Two lines before hit list section
        elif line.startswith('Sequences producing significant alignments:'):
            header_hit_list = True
        # One line before hit list section
        elif header_hit_list:
            if line.strip() == '':
                header_hit_list = False
                hit_list_section = True
        # Hit list section
        elif hit_list_section:
            # End of hit list section
            if line.strip() == '':
                hit_list_section = False
            # Hits
            else:
                splitted_line = line.split()
                target_accession = splitted_line[0]
                score = splitted_line[-2]
                e_value = splitted_line[-1]
                if float(score) > threshold and target_accession != query_accession:
                    if target_accession not in done:
                        outfile.write(f"{query_accession}\t{target_accession}\t{score}\t{e_value}\n")
    infile.close()
    outfile.close()

# Create neighbor dict
def create_neighbor_dict(threshold):
    """Creates a dict with each accession as key and a list of all its neighbors as value"""
    sys.stderr.write("Creating neighbor dict\n")
    network_file = open(output_name(expansion_threshold, ssn_threshold))
    neighbor_dict = {}
    for line in network_file:
        if line.startswith('source'):
            continue
        splitted_line = line.split('\t')
        first_accession = splitted_line[0]
        second_accession = splitted_line[1]
        # Add first accession
        if first_accession in neighbor_dict:
            neighbor_dict[first_accession].append(second_accession)
        else:
            neighbor_dict[first_accession] = [second_accession]
        # Add second accession
        if second_accession in neighbor_dict:
            neighbor_dict[second_accession].append(first_accession)
        else:
            neighbor_dict[second_accession] = [first_accession]
    network_file.close()
    return neighbor_dict

def get_clusters(neighbor_dict):
    sys.stderr.write("Getting clusters\n")
    to_visit = neighbor_dict
    to_visit_next = set()
    visited = set()
    clusters = list()
    while len(to_visit) > 0:
        # Choose random from to_visit
        this_acc, neighbors = random.choice(list(to_visit.items()))
        # Remove this_acc from to_visit
        to_visit.pop(this_acc)
        # Add to visited
        visited.add(this_acc)
        # Initialize cluster
        cluster = {this_acc}
        # Add neighbors to to_visit_next
        to_visit_next.update(neighbors)
        # Loop through neighbors
        while len(to_visit_next) > 0:
             # Choose random from to_visit_next
            this_acc = to_visit_next.pop()
            visited.add(this_acc)
            # Get neighbors (and remove from to_visit)
            neighbors = to_visit.pop(this_acc)
            # Add to cluster
            cluster.add(this_acc)
            # Add neighbors to to_visit_next
            for neighbor in neighbors:
                if neighbor not in visited:
                    to_visit_next.add(neighbor)
        clusters.append(cluster)
    return clusters

def count_nodes(clusters):
    count = 0
    for cluster in clusters:
        count += len(cluster)
    return count

def get_number_of_singletons(expansion_threshold, count_nodes):
    fasta = open(f"/work3/idamei/wzy_ssn/run/{expansion_threshold}/sequences.fa")
    count_total = 0
    for line in fasta:
        if line.startswith('>'):
            count_total += 1
    count_singletons = count_total - count_nodes
    sys.stderr.write(f"Total number of blast hits: {count_total} \n")
    sys.stderr.write(f"Number of singletons: {count_singletons} \n")
    sys.stderr.write(f"Number of nodes in clusters: {count_nodes} \n")
    outfile = open(f"/work3/idamei/wzy_ssn/run/{expansion_threshold}/run/{ssn_threshold}/info", "w")
    outfile.write(f"Total number of proteins: {count_total} \n")
    outfile.write(f"Number of singletons: {count_singletons} \n")
    outfile.write(f"Number of nodes in clusters: {count_nodes} \n")
    outfile.write(f"Number of clusters: {len(clusters)} \n")
    outfile.close()

# Make fasta
def make_fastas(clusters):
    """Writes fasta file for each cluster."""
    # Make directory
    fasta_dir = f"{output_directory(expansion_threshold, ssn_threshold)}/fastas"
    if not os.path.isdir(fasta_dir):
        os.makedirs(fasta_dir)
    count = 0
    for cluster in clusters:
        count += 1
        # Filename
        cluster_size = str(len(cluster)).zfill(4)
        fasta_outfile = open(f"{fasta_dir}/{cluster_size}_{count}.fa", "w")
        accessions_done = list()
        # Write annotated
        annotated_in_cluster = annotated_df.loc[annotated_df['protein_accession'].isin(cluster), ['protein_accession', 'sequence']]
        for index, row in annotated_in_cluster.iterrows():
            accessions_done.append(row.protein_accession)
            fasta_outfile.write(f">{row.protein_accession}\n{row.sequence}\n")
        # Write blast hits
        blast_hits_in_cluster = blast_hits_df.loc[blast_hits_df['accession'].isin(cluster), ['accession', 'sequence']]
        for index, row in blast_hits_in_cluster.iterrows():
            if row.accession not in accessions_done:
                fasta_outfile.write(f">{row.accession}\n{row.sequence}\n")
    return fasta_dir

def make_alignments(expansion_threshold, ssn_threshold, fasta_dir):
    sys.stderr.write('Making alignments\n')
    alignment_dir = f"{output_directory(expansion_threshold, ssn_threshold)}/MSAs"
    if not os.path.isdir(alignment_dir):
        os.makedirs(alignment_dir)
    alignment_jobscript_dir = f"{output_directory(expansion_threshold, ssn_threshold)}/MSA_jobscripts"
    if not os.path.isdir(alignment_jobscript_dir):
        os.makedirs(alignment_jobscript_dir)
    logos_dir = f"{output_directory(expansion_threshold, ssn_threshold)}/logos"
    if not os.path.isdir(logos_dir):
        os.makedirs(logos_dir)
    for fasta in os.listdir(fasta_dir):
        cluster_name = fasta.replace('.fa', '')
        filename = f"{alignment_jobscript_dir}/{cluster_name}.sh"
        with open(filename, 'w') as fp:
            cmd = jobscript.replace('EXP_THR', str(expansion_threshold)).replace('SSN_THR', str(ssn_threshold)).replace('CLUSTER', cluster_name)
            fp.write(f"{cmd}\n")
        fp.close()
        print(f"bsub < {filename}")

def output_directory(expansion_threshold, ssn_threshold):
    return f"{RUN}/{str(expansion_threshold)}/run/{ssn_threshold}"

def output_name(expansion_threshold, ssn_threshold):
    return f"{output_directory(expansion_threshold, ssn_threshold)}/network"

# Thresholds (first number is expansion threshold, second number is SSN threshold)
threshold_pairs = [(1e-50, 150)]

# Read sequence files
annotated_df = pd.read_csv("/work3/idamei/wzy_ssn/wzy.tsv", sep='\t')
blast_hits_df = pd.read_csv("/work3/idamei/wzy_ssn/unique_hits_filtered.tsv", sep='\t')

# Pipeline
for threshold_pair in threshold_pairs:
    expansion_threshold = threshold_pair[0]
    ssn_threshold = threshold_pair[1]
    sys.stderr.write(str(f"Running expansion threshold {expansion_threshold}, ssn_threshold {ssn_threshold}")+'\n')
    # Make directory
    if not os.path.isdir(output_directory(expansion_threshold, ssn_threshold)):
        os.makedirs(output_directory(expansion_threshold, ssn_threshold))

    blast_file = f"/work3/idamei/wzy_ssn/run/{expansion_threshold}/blast.out"

    # Make network file
    make_network_file(ssn_threshold)

    # Create neighbordict
    neighbor_dict = create_neighbor_dict(ssn_threshold)

    # Get clusters
    clusters = get_clusters(neighbor_dict)

    # Make fasta for each cluster
    fasta_dir = make_fastas(clusters)

    # Count total number of nodes in clusters
    count_nodes = count_nodes(clusters)

    # Get number of singletons
    get_number_of_singletons(expansion_threshold, count_nodes)

    # Make MSA for each cluster
    make_alignments(expansion_threshold, ssn_threshold, fasta_dir)

    # Maybe include singletons somehow

    # Logoplots
