from Bio import SeqIO
import sys

def get_cds_feature_with_qualifier_value(seq_record, name, value):
    """ Used for getting wzy sequence"""
    # Loop over the features
    for feature in seq_record.features:
        if feature.type == "CDS" and value in feature.qualifiers.get(name, []):
            return feature
    # Could not find it
    return None

gb_file = sys.argv[1] # wzz.gb
tsv_outfile = open(sys.argv[2], "w")
tsv_outfile.write(f"protein_accession\torganism\toperon_accession\tprotein_seq\n")
count_failed = 0
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    operon_accession = gb_record.name
    organism = gb_record.annotations['organism']
    # Look for feature
    feature = ''
    cds_feature_wzz = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzz")
    if cds_feature_wzz is not None:
        feature = cds_feature_wzz
    cds_feature_wzz_rol = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzz (rol)")
    if cds_feature_wzz_rol is not None:
        feature = cds_feature_wzz_rol
    cds_feature_wzzE = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzzE")
    if cds_feature_wzzE is not None:
        feature = cds_feature_wzzE
    cds_feature_wzzB = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzzB")
    if cds_feature_wzzB is not None:
        feature = cds_feature_wzzB
    cds_feature_wzzfepE = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzz(fepE)")
    if cds_feature_wzzfepE is not None:
        feature = cds_feature_wzzfepE
    cds_feature_product = get_cds_feature_with_qualifier_value(gb_record, "product", "Wzz")
    if cds_feature_product is not None:
        feature = cds_feature_product
    if feature != '':
        wzz_accession = feature.qualifiers.get('protein_id')[0]
        wzz_seq = feature.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzz_accession}\t{organism}\t{operon_accession}\t{wzz_seq}\n")
    else:
        #print("Could not find wzz for " + operon_accession)
        count_failed += 1
print('Count failed:', count_failed)

tsv_outfile.close()