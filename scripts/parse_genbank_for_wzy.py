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

def get_serotype(seq_record):
    serotype = 'NA'
    # Loop over the features
    for feature in seq_record.features:
        # look in source feature
        if feature.type == "source":
            if feature.qualifiers.get("note", []) != []:
                serotype = feature.qualifiers.get("note", [])[0].replace('type: ', '').replace('serogroup: ', '')
            elif feature.qualifiers.get("serovar", []) != []:
                serotype = feature.qualifiers.get("serovar", [])[0]
            elif feature.qualifiers.get("serotype", []) != []:
                serotype = feature.qualifiers.get("serotype", [])[0]
            elif feature.qualifiers.get("serogroup", []) != []:
                serotype = feature.qualifiers.get("serogroup", [])[0]
    return serotype

gb_file = sys.argv[1]
tsv_outfile = open(sys.argv[3], "w")
tsv_outfile.write(f"protein_accession\torganism\tsertyope\toperon_accession\tprotein_seq\n")
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    operon_accession = gb_record.name
    organism = gb_record.annotations['organism']
    serotype = get_serotype(gb_record)
    cds_feature_wzy = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzy")
    if cds_feature_wzy is not None:
        wzy_accession = cds_feature_wzy.qualifiers.get('protein_id')[0]
        wzy_seq = cds_feature_wzy.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")

tsv_outfile.close()