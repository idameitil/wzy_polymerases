from cProfile import label
import random

#cluster_path = "clusters_ssns/"
cluster_path = ""
#outpath = "label_files_expanded/"
outpath = ""

#blast_thresholds = [1e-30, 1e-50]
blast_thresholds = [1e-30]
for blast_threshold in blast_thresholds:
    #ssn_thresholds = [100, 150, 200]
    ssn_thresholds = [150]
    for ssn_threshold in ssn_thresholds:
        #cluster_filename = f"{cluster_path}clusters_{blast_threshold}_{ssn_threshold}.tsv"
        cluster_filename = f"{cluster_path}clusters.tsv"
        label_file = open(outpath + cluster_filename.replace('tsv', 'txt'), "w")
        arrow_label_file = open(outpath + cluster_filename.replace('.tsv', '_arrow.txt'), "w")
        name = cluster_filename.replace('.tsv', '').replace("/Users/idamei/wzy_polymerases/", '')
        header = f"DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,{name}\nCOLOR,#ff0000\nDATA\n"
        label_file.write(header)
        header_arrow = f"DATASET_CONNECTION\nSEPARATOR COMMA\nDATASET_LABEL,{name}_Arrows\nCOLOR,#ff0ff0\nALIGN_TO_LABELS,1\nCENTER_CURVES,1\nCENTER_CURVES,1\nDATA\n"
        arrow_label_file.write(header_arrow)
        cluster2color = dict()
        accession2cluster = dict()
        cluster_file = open(cluster_filename, 'r')
        for line in cluster_file:
            splitted_line = line.strip().split()
            acc, cluster = splitted_line[0], splitted_line[1]
            if cluster not in cluster2color:
                color = '#' + "%06x" % random.randint(0, 0xFFFFFF)
                cluster2color[cluster] = color
                first_acc = acc
            # Write arrow file
            else:
                arrow_label_file.write(f"{first_acc},{acc},2,{cluster2color[cluster]},dashed,{cluster}\n")
            if acc.endswith('.1') or acc.endswith('.2') or acc.endswith('.3'):
                acc_write = acc
            else:
                acc_write = acc + '.1'
            label_file.write(f"{acc_write},{cluster2color[cluster]},{cluster}\n")
        label_file.close()
        arrow_label_file.close()
        cluster_file.close()