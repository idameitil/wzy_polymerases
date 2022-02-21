#! /usr/bin/python3
'''
Description:
	Master script for generating many individual bsub submission scripts.
	For use on the HPC.

	What this script does:
	(A) reads a FASTA inputfile as a list of records, then
	(B) for each fasta record, creates (as needed*)
		run/{THR}/ = output directory that will contain job input and output.
		run/{THR}/query.fa = fasta file for the individual record, input to blast.
		run/{THR}/blast.sh = shell script for running this one blast job.
	where {THR} is the fasta accession number.
	*If the output directory already exists, the fasta record is skipped.

Usage:
	First edit this script to contain the correct input FASTA file, and HPC parameters.
	Then:
		genscript.py > submit.sh
		sh submit.sh

Notes:
	The 'cache' output directory tested in this script is not used, and can be ignored or removed.
	The directory /work3/garryg/blast contains world-readable blast databases and executables, and
	/work3/garryg/bioP contains a library of Garry's Python modules and methods.
'''

RUN = 'run'
CACHE = 'cache'
GROOT = '/work3/garryg/'

# The string 'THR' in this blast string will be substituted by a Fasta accession.
blast=f"""#! /bin/sh 
### General options 
### -- specify queue -- 
#BSUB -q hpc
### -- set the job Name -- 
#BSUB -J blast_THR
### -- ask for number of cores (default: 1) -- 
#BSUB -n 1 
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 2GB of memory per core/slot -- 
#BSUB -R "rusage[mem=20GB]"
### -- specify that we want the job to get killed if it exceeds 3 GB per core/slot -- 
#BSUB -M 20GB
### -- set walltime limit: hh:mm -- 
#BSUB -W 24:00 
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
#BSUB -o {RUN}/THR/jobscript.out
#BSUB -e {RUN}/THR/jobscript.err
# here follow the commands you want to execute 
export BLASTDB={GROOT}/blast/db
$BLASTDB/../current/bin/makeblastdb -in {RUN}/THR/sequences.fa -dbtype prot -parse_seqids
$BLASTDB/../current/bin/blastp -db {RUN}/THR/sequences.fa -query {RUN}/THR/sequences.fa -max_target_seqs 100000 -out {RUN}/THR/blast.out
"""


import sys
import os
import hashlib
import pandas as pd

# Read tsv to retrieve sequences
seq_df = pd.read_csv("/zhome/2b/2/141636/wzy_blast/unique_blast_hits_Feb16.tsv", sep = '\t')

# Read infile
infile = open("/zhome/2b/2/141636/wzy_blast/blast_hits_Feb16")
hits_evalue_dict = dict()
for line in infile:
	accession, score, e_value = line.strip().split()
	# If accession is already there
	if accession in hits_evalue_dict:
		# Replace if e_value is lower
		if e_value < hits_evalue_dict[accession]['score']:
			hits_evalue_dict[accession] = {'score':score, 'e_value':e_value}
		else:
			pass
	# Add if accession is not already there
	else:
		hits_evalue_dict[accession] = {'score':str(score), 'e_value':str(e_value)}
evalue_df = pd.DataFrame.from_dict(hits_evalue_dict, orient='index', dtype = 'float64')

count = 0
expect = 10

if not os.path.isdir(RUN):
	os.makedirs(RUN)

thresholds = [10**(-200)]

for threshold in thresholds:

	def acc(fasta):
		return fasta['acc']
	def seq(fasta):
		return fasta['seq']
	def seq_md5(fasta):
		return hashlib.md5(seq(fasta).upper().encode('utf-8')).hexdigest()
	def output_directory(threshold):
		return f"{RUN}/{str(threshold)}"
	def output_name(threshold):
		return f"{output_directory(threshold)}/blast.out"
	def cache_directory(fasta):
		return f"{CACHE}/{seq_md5(fasta)}"
	def cache_name(fasta):
		return f"{cache_directory(fasta)}/blast.out"
	def skippable(fasta):
		''' decide whether record can be skipped,
			based entirely on fasta elements: acc, des, and seq,
			or values derived therefrom.
		'''
		if os.path.isdir(output_directory(fasta)):
			return True
		else:
			sys.stderr.write(f"DIAG output_directory does not exist\n")
		if os.path.isfile(output_name(fasta)):
			return True
		else:
			sys.stderr.write(f"DIAG output {output_name(fasta)} does not exist\n")
		if os.path.isfile(cache_name(fasta)):
			return True
		else:
			sys.stderr.write(f"DIAG cache {cache_name(fasta)} does not exist\n")
		''' ADD MORE REASONS HERE '''
		return False
	def write_fasta(threshold):
		filename = f"{output_directory(threshold)}/sequences.fa"
		with open(filename, 'w') as fp:
			condition = evalue_df.e_value < threshold
			indeces = evalue_df.index
			accessions_include = indeces[condition]
			print(len(accessions_include))
			sequences_include = seq_df.loc[seq_df.accession.isin(accessions_include), ('seq', 'accession')]
			for index, row in sequences_include.iterrows():
				fp.write(f'>{row.accession}\n{row.seq}\n')
		fp.close()
		sys.stderr.write(f"Wrote to {filename}\n")
	def write_script(threshold):
		filename = f"{output_directory(threshold)}/blast.sh"
		with open(filename, 'w') as fp:
			cmd = blast.replace('THR', str(threshold))
			fp.write(f"{cmd}\n")
		fp.close()
		sys.stderr.write(f"Wrote to {filename}\n")
	def prepare_submit_script(threshold):
		if not os.path.isdir(output_directory(threshold)):
			os.makedirs(output_directory(threshold))
		write_fasta(threshold)
		write_script(threshold)
		print(f"bsub < {output_directory(threshold)}/blast.sh")

	# finally look at the listed item
	#if skippable(item):
	#	continue
	#sys.stderr.write(f"NOT SKIPPABLE {count} {item}\n")

	prepare_submit_script(threshold)

	count += 1
	if count >= expect:
		sys.stderr.write(f"COUNT {count} TERMINATION\n")
		break