import pandas as pd

outpath = "../label_files_annotated/"

# Wzy
# Open files
wzy_df = pd.read_csv("../polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep='\t', dtype=object)
wzy_serotype_file = open(outpath + "wzy_serotype.txt", "w")
wzy_species_file = open(outpath + "wzy_species.txt", "w")
wzy_genus_file = open(outpath + "wzy_genus.txt", "w")
wzy_image_file = open(outpath + "wzy_image.txt", "w")
wzy_csdbid_file = open(outpath + "wzy_csdbid.txt", "w")
# Write headers
header_serotype = "DATASET_TEXT\nSEPARATOR TAB\nDATASET_LABEL\tSerotype\nCOLOR\t#ff0000\nDATA\n"
wzy_serotype_file.write(header_serotype)
header_species = "DATASET_TEXT\nSEPARATOR TAB\nDATASET_LABEL\tSpecies\nCOLOR\t#ff0000\nDATA\n"
wzy_species_file.write(header_species)
header_genus = "DATASET_TEXT\nSEPARATOR TAB\nDATASET_LABEL\tGenus\nCOLOR\t#ff0000\nDATA\n"
wzy_genus_file.write(header_genus)
header_image = "DATASET_IMAGE\nSEPARATOR TAB\nDATASET_LABEL\timage\nCOLOR,#ff0000\nMARGIN\t0\nSHOW_INTERNAL\t"\
                "t0\nIMAGE_ROTATION\t0\nIMAGE_SHIFT_V\t0\nIMAGE_SHIFT_H\t0\nSIZE_FACTOR	1\nDATA\n"
wzy_image_file.write(header_image)
header_csdbid = "DATASET_TEXT\nSEPARATOR TAB\nDATASET_LABEL\tCSDB ID\nCOLOR\t#ff0000\nDATA\n"
wzy_csdbid_file.write(header_csdbid)
# Write data
for index, row in wzy_df.iterrows():
    wzy_serotype_file.write(f"{row.protein_accession}\t{row.serotype}\t-1\t\tbold\t3\t0\n")
    wzy_species_file.write(f"{row.protein_accession}\t{row.species_short}\t-1\t\tbold\t3\t0\n")
    wzy_genus_file.write(f"{row.protein_accession}\t{row.genus}\t-1\t\tbold\t3\t0\n")
    wzy_image_file.write(f"{row.protein_accession}\t-1\t1\t0\t0\t0\t{row.csdb_image_path}\n")
    wzy_csdbid_file.write(f"{row.protein_accession}\t{row.CSDB_record_ID}\t-1\t\tbold\t3\t0\n")
wzy_serotype_file.close()
wzy_species_file.close()
wzy_genus_file.close()
wzy_image_file.close()

# Wzx
# Open files
wzx_df = pd.read_csv("../wzx/wzx_with_sugars_and_taxonomy.tsv", sep='\t', dtype=object)
wzx_serotype_file = open(outpath + "wzx_serotype.txt", "w")
wzx_species_file = open(outpath + "wzx_species.txt", "w")
wzx_genus_file = open(outpath + "wzx_genus.txt", "w")
wzx_image_file = open(outpath + "wzx_image.txt", "w")
wzx_csdbid_file = open(outpath + "wzx_csdbid.txt", "w")
# Write headers
wzx_serotype_file.write(header_serotype)
wzx_species_file.write(header_species)
wzx_genus_file.write(header_genus)
wzx_image_file.write(header_image)
wzx_csdbid_file.write(header_csdbid)
# Write data
for index, row in wzx_df.iterrows():
    wzx_serotype_file.write(f"{row.protein_accession_wzx}\t{row.serotype}\t-1\t\tbold\t3\t0\n")
    wzx_species_file.write(f"{row.protein_accession_wzx}\t{row.species_short}\t-1\t\tbold\t3\t0\n")
    wzx_genus_file.write(f"{row.protein_accession_wzx}\t{row.genus}\t-1\t\tbold\t3\t0\n")
    wzx_image_file.write(f"{row.protein_accession_wzx}\t-1\t1\t0\t0\t0\t{row.csdb_image_path}\n")
    wzx_csdbid_file.write(f"{row.protein_accession_wzx}\t{row.CSDB_record_ID}\t-1\t\tbold\t3\t0\n")
wzx_serotype_file.close()
wzx_species_file.close()
wzx_genus_file.close()
wzx_image_file.close()
wzx_csdbid_file.close()

# Wzz
# Open files
wzz_df = pd.read_csv("../wzz/wzz_with_sugars_and_taxonomy.tsv", sep='\t', dtype=object)
wzz_serotype_file = open(outpath + "wzz_serotype.txt", "w")
wzz_species_file = open(outpath + "wzz_species.txt", "w")
wzz_genus_file = open(outpath + "wzz_genus.txt", "w")
wzz_image_file = open(outpath + "wzz_image.txt", "w")
wzz_csdbid_file = open(outpath + "wzz_csdbid.txt", "w")
# Write headers
wzz_serotype_file.write(header_serotype)
wzz_species_file.write(header_species)
wzz_genus_file.write(header_genus)
wzz_image_file.write(header_image)
wzz_csdbid_file.write(header_csdbid)
# Write data
for index, row in wzz_df.iterrows():
    wzz_serotype_file.write(f"{row.protein_accession_wzz}\t{row.serotype}\t-1\t\tbold\t3\t0\n")
    wzz_species_file.write(f"{row.protein_accession_wzz}\t{row.species_short}\t-1\t\tbold\t3\t0\n")
    wzz_genus_file.write(f"{row.protein_accession_wzz}\t{row.genus}\t-1\t\tbold\t3\t0\n")
    wzz_image_file.write(f"{row.protein_accession_wzz}\t-1\t1\t0\t0\t0\t{row.csdb_image_path}\n")
    wzz_csdbid_file.write(f"{row.protein_accession_wzz}\t{row.CSDB_record_ID}\t-1\t\tbold\t3\t0\n")
wzz_serotype_file.close()
wzz_species_file.close()
wzz_genus_file.close()
wzz_image_file.close()
wzx_csdbid_file.close()