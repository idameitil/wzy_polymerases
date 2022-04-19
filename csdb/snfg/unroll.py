#! /usr/bin/python3
''' Download png images for csdb sugars
'''

WZY = "/Users/idamei/wzy_polymerases"
DB = WZY + "/csdb/dat/CSDB_slice_for_Ida.txt"

import os
import re
import sys
import csv
import wget
import pandas as pd

os.system("ls -l {}".format(DB))

# root of images directory
images = WZY + "/csdb/snfg"

def doit(cmd, forgive=False):
	s = os.system(cmd)
	if s != 0 :
		sys.stderr.write("{} = system({})\n".format(s, cmd))
		if not forgive :
			raise Exception("system call non zero")
	return s

def fetch_snfg_image(record_id, csdb_linear, scale=3, overwrite=False):
	outdir ="{}/{}".format(images,scale)
	outfil ="{}/{}.gif".format(outdir,record_id)
	clean = False
	if clean :
		cmd = "/bin/rm -f {}".format(outfil)
		doit(cmd)
	if os.path.isfile(outfil) :
		if not overwrite :
			print("File exists {}, and not overwrite ... skipping\n".format(outfil))
			return
	os.makedirs(outdir, exist_ok=True)
	print("record_id: {} linear: {}\n".format(record_id, csdb_linear))
	'''
		Some of the direct CSDB_linear images are not rendered properly by csdb themselves, therefore we allow to strip comment sections.

		Some of these rendering failures are mitigated by removal of square-bracketed sections. Others are not so easy.
		For example 110981
	'''
	# if re.search(r"\[[^\]]*\]", csdb_linear):
	# 	print("Removing bracket section from record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))
	# 	csdb_linear = re.sub("\[[^\]]*\]", "", csdb_linear)
	# 	print("After bracket removal for  record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))
	# if re.search(r",*\d*\%Ac\(1-2\)", csdb_linear):
	# 	print("Removing percent section from record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))
	# 	csdb_linear = re.sub(r",*\d*\%Ac\(1-2\)", "", csdb_linear)
	# 	print("After percent removal for  record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))
	# # Change this
	# if re.search(r"\%\d*", csdb_linear):
	# 	print("Removing percent section from record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))
	# 	csdb_linear = re.sub(r"\%\d*", "", csdb_linear)
	# 	print("After percent removal for  record_id {} csdb_linear structure {}\n".format(record_id, csdb_linear))

	print("record_id: {} linear: {}\n".format(record_id, csdb_linear))
	image_url = "http://csdb.glycoscience.ru/database/core/graphic.php?to_draw={}&scale={}&on_white=0&backdrop=checkers&no_reducing=0".format(csdb_linear, scale)
	print("IMAGE_URL:".format(image_url))
	try:
		# Use wget download method to download specified image url.
		image_filename = wget.download(image_url)
		# move to specific image file
		cmd = 'mv -f graphic.php {}'.format(outfil)
		doit(cmd)
		print("record_id: {} linear: {}, outfile %s created".format(record_id, csdb_linear, outfil))
	except:
		print("Cannot get image for CSDB id", record_id)
		leave_evidence_of_having_tried = True
		if leave_evidence_of_having_tried :
			if not os.path.isfile(outfil):
				doit('touch ' + outfil)
			
	print("DONE {} {}\n".format(record_id, csdb_linear))

polymerase_df = pd.read_csv(WZY + "/polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep='\t', dtype={'CSDB_record_ID':'string'})
wanted = list(polymerase_df.CSDB_record_ID.dropna())

# Open DB file, iterate over rows, avoiding record_ids we have already seen
seen = []
columns = []
count = 0
with open(DB, 'r') as fp:
	table = csv.reader(fp, delimiter="\t")

	for row in table:
		''' First row contains column names, not column data.'''
		if row[0] == 'CSDB_record_ID':
			columns = row
			print("COLUMNS", columns)
			continue
		# a specific data model, just to make life simpler
		CSDB_record_ID, CSDB_Linear, glycoct, CSDB_nonpersistent_article_ID, doi, pmid, Taxonomic_name, Strain_or_Serogroup, NCBI_TaxID = row
		#print( CSDB_record_ID, CSDB_Linear, glycoct, CSDB_nonpersistent_article_ID, doi, pmid, Taxonomic_name, Strain_or_Serogroup, NCBI_TaxID)
		# Avoid repeating an id
		if CSDB_record_ID in seen:
			continue
		seen.append(CSDB_record_ID)

		if len(wanted) > 0 and CSDB_record_ID not in wanted:
			continue

		fetch_snfg_image(CSDB_record_ID, CSDB_Linear)
