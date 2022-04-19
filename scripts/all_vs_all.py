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

RUN = '/work3/idamei/wzy_ssn/run'
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
#BSUB -W 72:00 
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
/work3/idamei/bin/muscle5.1.linux_intel64 -super5 {RUN}/THR/sequences.fa -output {RUN}/THR/sequences.afa
"""


from multiprocessing import Condition
import sys
import os
import hashlib
import pandas as pd
sys.path.append(f"{GROOT}/bioP/lib")
from Fasta import read_fasta

sys.stderr.write("Parsing blast results\n")

##########################
### Parse blast output ###
##########################

if os.path.exists("unique_hits.tsv"):
	sys.stderr.write('Skipping parsing blast output. unique_hits.tsv already exists.\n')
	hit2evalue_series = pd.read_csv("unique_hits.tsv", header = None, index_col=0, squeeze = True, sep = '\t')
else:
	blast_run_path = "/work3/idamei/wzy_blast/run/"
	directories = os.listdir(blast_run_path)

	hit2evalue = dict() # All hits
	alignment_hits = set() # The hits that are actually in Genbank
	sys.stderr.write(str(len(directories))+'\n')
	count = 0
	for accession in directories:
		sys.stderr.write(str(count)+'\n')
		count += 1
		blast_file = open(blast_run_path + accession + "/blast.out")
		header_hit_list = False
		hits_list_section = False
		for line in blast_file:
			# Two lines before hits list section
			if line.startswith('Sequences producing significant alignments:'):
				header_hit_list = True
			# One line before hits list section
			elif header_hit_list:
				# End of hits section
				if line.strip() == '':
					header_hit_list = False
					hits_list_section = True
			# Hits list section
			elif hits_list_section:
				# End of hits list section
				if line.strip() == '':
					hits_list_section = False
				# Hits
				else:
					splitted_line = line.split()
					hit_accession = splitted_line[0]
					e_value = float(splitted_line[-1])
					if hit_accession in hit2evalue:
						# Save this e-value if it's smaller
						if e_value < hit2evalue[hit_accession]:
							hit2evalue[hit_accession] = e_value
					else:
						hit2evalue[hit_accession] = e_value
			# Alignment section
			elif line.startswith('>'):
				alignment_accession = line.split()[0][1:]
				alignment_hits.add(alignment_accession)

	# Write file with unique hits and their best e-value
	hit2evalue_series = pd.Series(hit2evalue)
	condition = hit2evalue_series.index.isin(alignment_hits)
	hit2evalue_series[condition].to_csv("unique_hits.tsv", sep = '\t', header=False)

# Retrieve sequences with blastdbcmd
if os.path.exists('unique_hits.seq'):
	sys.stderr.write('Skipping retrieval of sequences for hits. File already exists.\n')
else:
	sys.stderr.write('Retrieving sequences for blast hits\n')
	os.system(f'blastdbcmd -db nr -entry_batch unique_hits.tsv -outfmt "%a, %L, %T, %s" > unique_hits.seq')

# Write fasta with unique hits
# Length filter and M start filter
if os.path.exists('unique_hits_filtered.fasta'):
	sys.stderr.write('Skipping generation of fasta file for blast hits. unique_hits.fasta already exists.\n')
if True:
	sys.stderr.write('Making fasta file for blast hits\n')
	infile = open('unique_hits.seq')
	outfile = open("unique_hits_filtered.fasta", 'w')
	outfile_tsv = open("unique_hits_filtered.tsv", 'w')
	outfile_tsv.write('accession\tsequence\n')
	for line in infile:
		splitted_line = line.strip().split(', ')
		acc, seq = splitted_line[0], splitted_line[3]
		if acc in hit2evalue_series.index and len(seq) > 250 and len(seq) < 500 and seq.startswith("M"):
			outfile.write(f'>{acc}\n{seq}\n')
			outfile_tsv.write(f'{acc}\t{seq}\n')
	infile.close()
	outfile.close()
	outfile_tsv.close()

# CD-HIT
if os.path.exists('unique_hits_filtered_cdhit.fasta'):
	sys.stderr.write('Skipping CD-HIT. File already exists.\n')
else:
	sys.stderr.write('Running CD-HIT on all hits.\n')
	os.system(f'cd-hit -i unique_hits_filtered.fasta -o unique_hits_filtered_cdhit.fasta -c 0.95 > /dev/null 2>&1')

# Read CD-HIT output
result = read_fasta('unique_hits_filtered_cdhit.fasta')
reduced = dict()
for entry in result:
	reduced[entry['acc']] = entry['seq']
reduced_hit2seq = pd.Series(reduced)
reduced_hit2evalue_series = hit2evalue_series[reduced_hit2seq.index]

# Read annotated fasta file
annotated_fasta = "/work3/idamei/wzy_blast/wzy.fasta"
result = read_fasta(annotated_fasta)
annotated = dict()
for entry in result:
	annotated[entry['acc']] = entry['seq']

count = 0
expect = 10

if not os.path.isdir(RUN):
	os.makedirs(RUN)

thresholds = [10**(-50)]

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
	def threshold_filter(threshold):
		''' Get blast hits that are below threshold '''
		condition = reduced_hit2evalue_series < threshold
		indeces = reduced_hit2evalue_series.index
		accessions_include = indeces[condition]
		sequences_include = reduced_hit2seq[accessions_include]
#		sequences_include = seq_df.loc[seq_df.accession.isin(accessions_include), ('seq', 'accession')]
		return accessions_include, sequences_include
	def write_fasta(threshold):
		filename = f"{output_directory(threshold)}/sequences.fa"
		with open(filename, 'w') as fp:
			
			accessions_include, sequences_include = threshold_filter(threshold)
			# Write blast hits to fasta
			for index, value in sequences_include.iteritems():
				fp.write(f'>{index}\n{value}\n')
			# Write annotated polymerases to fasta
			for acc in annotated:
				if acc not in accessions_include: # only add those that are not already there
					seq = annotated[acc]
					fp.write(f'>{acc}\n{seq}\n')
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
		sys.stdout.write(f"bsub < {output_directory(threshold)}/blast.sh\n")

	# finally look at the listed item
	#if skippable(item):
	#	continue
	#sys.stderr.write(f"NOT SKIPPABLE {count} {item}\n")

	prepare_submit_script(threshold)

	count += 1
	if count >= expect:
		sys.stderr.write(f"COUNT {count} TERMINATION\n")
		break
