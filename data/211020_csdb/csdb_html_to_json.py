#! /usr/bin/python3
# Generate a JSON file containing a table, where each row corresponds to a CSDB record id.
#
# Step 1, on the CSDB site, enter list of CSDB record ids, and click 'Make RDF in RDF/JSON'.
# Step 2, save the data as RDFx.html
# Step 3, change the 'file_prefix' in this script to what you chose for 'RDFx'.
# Step 4, run this script. It will overwrite 'RDFx.json' <file_prefix>.json
#
# Author: G.P.Gippert, DTU Bioengineering, 2021 Sept 29, garryg@dtu.dk

file_prefix = 'RDF3'

input_file = "{}.html".format(file_prefix)
output_file = "{}.json".format(file_prefix)

import re
import json
import sys

# read file content as ASCII string and remove newlines
with open(input_file, 'r', encoding='latin-1') as fp:
    data = fp.read().replace('\n', '')

# remove HTML header and footer
# NOTE: uncomment one of the following lines whether you saved in Safari or Chrome (not tested for other browsers)
# Safari
data = re.sub(r'<HTML>.*<pre>{', '{', data)
# for Chrome
# data = re.sub(r'<!-- saved from url.*<pre>{', '{', data)
data = re.sub(r'}</pre>.*', '}', data)

# reinterpret JSON
data = json.loads(data)

# temporary variables for storing data
bacteria = {}
relation = {}
compound = {}

# The structure sections we want to pull out
sections = ('GLYCAN_CSDB', 'GLYCAN_WURCS', 'GLYCAN_GLYCOCT')

taxon_number = 0
for k,v in sorted(data.items()):

	# extract relation for Compound Publication Bacteria embedded in URL
	m = re.search(r'db=(?:database|bacterial)&mode=relation&id_list=c(\d+)p(\d+)b(\d+)', k)
      	#{ "value" : "http://csdb.glycoscience.ru/integration/make_rdf.php?db=database&mode=relation&id_list=c118p4827b31034", "type" : "uri" },

	if m:
		compound_id = m.group(1)
		publicat_id = m.group(2)
		bacteria_id = m.group(3)
		relation[bacteria_id] = compound_id

	# extract bacteria taxonomy information
	m = re.search(r'db=(?:database|bacterial)&mode=(?:source|record)&id_list=(\d+)', k)
	if m:
		bacteria_id = m.group(1)
		print("bacteria_id", bacteria_id)
		if type(v) is not dict:
			raise Exception("Value is not dict", v)
		bacteria[bacteria_id] = "Unidentified" + str(taxon_number)
		taxon_number += 1
		for i,j in v.items():
			if re.search('has_taxon', i):
				if type(j) is not list:
					raise Exception("J is not list", j)
				if len(j) == 0:
					raise Exception("J has length zero", len(j), j)
				if len(j) > 1:
					sys.stderr.write("J taxonomy length > 1, {} {}\n".format(len(j), j))
				if type(j[0]) is not dict:
					raise Exception("J[0] is not dict", type(j[0]), j[0])
				if 'value' not in j[0]:
					raise Exception("J[0] does not contain 'value'", j[0])
				bacteria[bacteria_id] = j[0]['value']
			# to accommodate CSDB id 22620, the following was needed
			if re.search('has_destination_organism', i):
				if type(j) is not list:
					raise Exception("J is not list", j)
				if len(j) == 0:
					raise Exception("J has length zero", len(j), j)
				if len(j) > 1:
					sys.stderr.write("J taxonomy length > 1, {} {}\n".format(len(j), j))
				if type(j[0]) is not dict:
					raise Exception("J[0] is not dict", type(j[0]), j[0])
				if 'value' not in j[0]:
					raise Exception("J[0] does not contain 'value'", j[0])
				bacteria[bacteria_id] = j[0]['value']

	# extract compound structure information in different sections
	for section in sections:
		m = re.search(r'mode=structure&id_list=(\d+)#{}'.format(section), k)
		if m:
			compound_id = m.group(1)
			if type(v) is not dict:
				raise Exception("Value is not dict", v)
			for i,j in v.items():
				if re.search('has_sequence', i):
					if type(j) is not list:
						raise Exception("J is not list", j)
					if len(j) != 1:
						raise Exception("J has length != 1 ", len(j), j)
					if type(j[0]) is not dict:
						raise Exception("J[0] is not dict", type(j[0]), j[0])
					if 'value' not in j[0]:
						raise Exception("J[0] does not contain 'value'", j[0])
					if compound_id not in compound:
						compound[compound_id] = {}
					compound[compound_id][section] = j[0]['value']

if( False ):
	print("Compound", compound)
	print("Bacteria")
	for k, v in sorted(bacteria.items()):
		print(k, v)
	print("Relation", relation)

# Generate a list of CSDB entries
csdb = []

for bacteria_id, compound_id in relation.items():
	if bacteria_id not in bacteria:
		raise Exception("bacteria_id not in bacteria list", bacteria_id, bacteria)
	if compound_id not in compound:
		raise Exception("compound_id not in compound list", compound_id, compound)
	this = []
	this.append({'key': 'source', 'value': 'CSDB'})
	this.append({'key': 'record_id', 'value': bacteria_id})
	this.append({'key': 'taxon', 'value': bacteria[bacteria_id]})
	this.append({'key': 'structure_id', 'value': compound_id})
	for section in sections:
		this.append({'key': section, 'value': compound[compound_id].get(section)})
	csdb.append(this)

with open(output_file, 'w') as fp:
	json.dump(csdb, fp, sort_keys=True, indent=4, ensure_ascii=True)
	fp.write('\n')
