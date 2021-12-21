from Bio import SeqIO
import pandas as pd

def get_cds_feature_with_qualifier_value(seq_record, name, value):
    """Function to look for CDS feature by annotation value in sequence record.

    e.g. You can use this for finding features by locus tag, gene ID, or protein ID.
    """
    # Loop over the features
    for feature in seq_record.features:
        if feature.type == "CDS" and value in feature.qualifiers.get(name, []):
            return feature
    # Could not find it
    return None

def get_serotype(seq_record):
    """Function to look for CDS feature by annotation value in sequence record.

    e.g. You can use this for finding features by locus tag, gene ID, or protein ID.
    """
    # Loop over the features
    for feature in seq_record.features:
        if feature.type == "source":
            if feature.qualifiers.get("note", []) != []:
                return feature.qualifiers.get("note", [])[0].replace('type: ', '')
            elif feature.qualifiers.get("serovar", []) != []:
                return feature.qualifiers.get("serovar", [])[0]
            elif feature.qualifiers.get("serotype", []) != []:
                return feature.qualifiers.get("serotype", [])[0]
            else:
                return 'NA'
    # Could not find it
    return None

gb_file = "../Downloads/sequence.gb"
outfile = open("data/shigella/shigella_polymerases.fasta", "w")
tsv_outfile = open("data/shigella/shigella_polymerases.tsv", "w")
tsv_outfile.write(f"protein_accession\torganism\tsertyope\toperon_accession\tprotein_seq\n")
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    operon_accession = gb_record.name
    organism = gb_record.annotations['organism']
    serotype = get_serotype(gb_record)
    cds_feature = get_cds_feature_with_qualifier_value(gb_record, "gene", "wzy")
    if cds_feature is not None:
        protein_accession = cds_feature.qualifiers.get('protein_id')[0]
        protein_seq = cds_feature.qualifiers.get('translation')[0]
        outfile.write(f">{protein_accession} {organism}\n{protein_seq}\n")
        tsv_outfile.write(f"{protein_accession}\t{organism}\t{serotype}\t{operon_accession}\t{protein_seq}\n")

outfile.close()
