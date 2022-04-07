from Bio import SeqIO
import sys

def get_cds_feature_with_qualifier_value(seq_record, name, value):
    """ Used for getting wzx sequence"""
    # Loop over the features
    for feature in seq_record.features:
        if feature.type == "CDS" and value in feature.qualifiers.get(name, []):
            return feature
    # Could not find it
    return None

gb_file = sys.argv[1] # wzx.gb
tsv_outfile = open(sys.argv[2], "w")
tsv_outfile.write(f"protein_accession\torganism\toperon_accession\tprotein_seq\n")
count_failed = 0
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    operon_accession = gb_record.name
    organism = gb_record.annotations['organism']
    # Look for feature
    feature = ''
    cds_feature_wzx = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzx")
    if cds_feature_wzx is not None:
        feature = cds_feature_wzx
    cds_feature_wzxC = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzxC")
    if cds_feature_wzxC is not None:
        feature = cds_feature_wzxC
    cds_feature_wzxE = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzxE")
    if cds_feature_wzxE is not None:
        feature = cds_feature_wzxE
    if feature != '':
        wzx_accession = feature.qualifiers.get('protein_id')[0]
        wzx_seq = feature.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzx_accession}\t{organism}\t{operon_accession}\t{wzx_seq}\n")
    else:
        #print("Could not find wzx for " + operon_accession)
        count_failed += 1
print('Count failed:', count_failed)

tsv_outfile.close()