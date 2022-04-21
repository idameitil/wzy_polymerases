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
tsv_outfile = open(sys.argv[2], "w")
tsv_outfile.write(f"protein_accession\torganism\tsertyope\toperon_accession\tprotein_seq\n")
count_failed = 0
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    operon_accession = gb_record.name
    organism = gb_record.annotations['organism']
    serotype = get_serotype(gb_record)
    # name "wzy"
    cds_feature_wzy = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzy")
    #cds_feature_wzyE = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzyE")
    cds_feature_rfc = get_cds_feature_with_qualifier_value(gb_record, "gene", "rfc")
    cds_feature_o_antigen = get_cds_feature_with_qualifier_value(gb_record, "product", "O-antigen polymerase")
    cds_feature_oligo = get_cds_feature_with_qualifier_value(gb_record, "product", "oligosaccharide repeat unit polymerase")
    if cds_feature_wzy is not None:
        wzy_accession = cds_feature_wzy.qualifiers.get('protein_id')[0]
        wzy_seq = cds_feature_wzy.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")
    # name "wzyE" THIS IS NOT O-ANTIGEN POLYMERASE
    #elif cds_feature_wzyE is not None:
    #    wzy_accession = cds_feature_wzyE.qualifiers.get('protein_id')[0]
    #    wzy_seq = cds_feature_wzyE.qualifiers.get('translation')[0]
    #    tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")
    elif cds_feature_rfc is not None:
        wzy_accession = cds_feature_rfc.qualifiers.get('protein_id')[0]
        wzy_seq = cds_feature_rfc.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")
    elif cds_feature_o_antigen is not None:
        wzy_accession = cds_feature_o_antigen.qualifiers.get('protein_id')[0]
        wzy_seq = cds_feature_o_antigen.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")
    elif cds_feature_oligo is not None:
        wzy_accession = cds_feature_oligo.qualifiers.get('protein_id')[0]
        wzy_seq = cds_feature_oligo.qualifiers.get('translation')[0]
        tsv_outfile.write(f"{wzy_accession}\t{organism}\t{serotype}\t{operon_accession}\t{wzy_seq}\n")
    else:
        print("Could not find wzy for " + operon_accession)
        count_failed += 1
print(count_failed)


tsv_outfile.close()