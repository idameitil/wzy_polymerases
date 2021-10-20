#! /usr/bin/python3
# Download gif images from CSDB for record_ids in an RDFx.json file.
#
# For each row in the JSON table, find the cell containing the record_id (writes
# <record_id>.gif, and find the cell containing the GLYCAN_CSDB string, which becomes
# a url parameter used by wget.

#
# Note, two kinds of errors occur that cause missing or faulty images.
#       The first is captured by the try block, where an image is apparently not
#	available, and wget returns an error.
#	The second error is that CSDB does return a gif image, but the image
#	contains a text message describing a parsing error.
# SO, check the resulting images carefully.
#
# Written Oct 20, 2021, G.P.Gippert GarryG@dtu.dk

import wget
import re
import json
import os

# todo: move to some table.py methods
def getcell(row, key='record_id', strict=True):
	for cell in row:
		if 'key' not in cell:
			raise Exception("Row cell does not contain 'key' element", cell)
		if cell['key'] == key:
			return cell
	if strict:
		raise Exception("No cell in row matches key '{}': {}", key, row)
	return None

def getcellvalue(row, key='record_id', strict=True):
	cell = getcell(row, key, strict)
	if strict and 'value' not in cell:
		raise Exception("Row cell does not contain 'value' element", cell)
	return cell['value']

def table_load(filename):
	table = []
	with open(filename, 'r') as fp:
		table = json.load(fp)
	print("Have read table {} rowcount {}".format(filename, len(table)))
	return table

# Which json to load from 'RDFx.json'
images = 'RDF6'

table = table_load('{}.json'.format(images))
os.mkdir(images)
scale=19 # large images
scale=3	# small images

for row in table:
	record_id = getcellvalue(row, 'record_id')
	glycan_csdb = str(getcellvalue(row, 'GLYCAN_CSDB'))

	# Set up the image URL
	image_url = "http://csdb.glycoscience.ru/database/core/graphic.php?to_draw={}&scale={}&on_white=0&backdrop=checkers&no_reducing=0".format(glycan_csdb, scale)

	try:
		# Use wget download method to download specified image url.
		image_filename = wget.download(image_url)
		print('Image Successfully Downloaded: ', image_filename)

		# move to specific image file
		cmd = 'mv -f graphic.php {}/{}.gif'.format(images, record_id)
		s = os.system(cmd)
		print(s, cmd)
	except:
		print("Cannot get image for CSDB id", record_id)

