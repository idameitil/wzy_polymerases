infile = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/wzy1_info.tab", "r")

"""
# Count frequency of domains
domain_dict = dict()
for line in infile:
    splitted_line = line.split("\t")
    domains = splitted_line[18].split('+')
    for domain in domains:
        domain_name = domain.split('(')[0]
        if domain_name in domain_dict:
            domain_dict[domain_name] += 1
        else:
            domain_dict[domain_name] = 1
print(domain_dict)
"""

"""
selected_domains = ["O-ag_pol_Wzy", "Wzy_C", "EpsG"]
groupA_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupA_EpsG.fsa", "w")
groupB_O_ag_pol_Wzy_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_O-ag_pol_Wzy.fsa", "w")
groupB_Wzy_C_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_Wzy_C.fsa", "w")
groupB_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_EpsG.fsa", "w")

groupA_cupp_groups = ["wzy1:1.1", "wzy1:8.1", "wzy1:1.2", "wzy1:84.1", "wzy1:67.1", "wzy1:70.1", "wzy1:469.1", "wzy1:148.1", "wzy1:57.1", "wzy1:330.1"]

for line in infile:
    splitted_line = line.strip().split("\t")
    accession = splitted_line[0]
    cupp_group = splitted_line[7]
    # Remove original entries that were sorted out in CD-HIT
    if cupp_group.endswith("*"):
        continue
    # Divide in A and B
    if cupp_group in groupA_cupp_groups:
        group = "A"
    else:
        group = "B"
    seq = splitted_line[46]
    domains = splitted_line[18].split('+')
    no_selected_domains = 0
    for domain in domains:
        domain_name = domain.split('(')[0]
        if domain_name in selected_domains:
            no_selected_domains += 1
            selected_domain = domain_name
    if no_selected_domains > 1:
        print(domains)
    elif no_selected_domains == 0:
        continue
    else:
        if group == "A":
            if selected_domain == "EpsG":
                groupA_EpsG_file.write(f">{accession}\n{seq}\n")
        elif group == "B":
            if selected_domain == "O-ag_pol_Wzy":
                groupB_O_ag_pol_Wzy_file.write(f">{accession}\n{seq}\n")
            elif selected_domain == "Wzy_C":
                groupB_Wzy_C_file.write(f">{accession}\n{seq}\n")
            elif selected_domain == "EpsG":
                groupB_EpsG_file.write(f">{accession}\n{seq}\n")
infile.close()

groupA_EpsG_file.close()
groupB_O_ag_pol_Wzy_file.close()
groupB_Wzy_C_file.close()
groupB_EpsG_file.close()
"""

"""
selected_domains = ["O-ag_pol_Wzy", "Wzy_C", "EpsG"]
groupA_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupA_EpsG.fsa", "w")
groupB_O_ag_pol_Wzy_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_O-ag_pol_Wzy.fsa", "w")
groupB_Wzy_C_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_Wzy_C.fsa", "w")
groupB_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_EpsG.fsa", "w")

groupA_cupp_groups = ["wzy1:1.1", "wzy1:8.1", "wzy1:1.2", "wzy1:84.1", "wzy1:67.1", "wzy1:70.1", "wzy1:469.1", "wzy1:148.1", "wzy1:57.1", "wzy1:330.1"]

for line in infile:
    splitted_line = line.strip().split("\t")
    accession = splitted_line[0]
    cupp_group = splitted_line[7]
    seq = splitted_line[46]
    domains = splitted_line[18].split('+')
    # Remove original entries that were sorted out in CD-HIT
    if cupp_group.endswith("*"):
        continue
    # Divide in A and B
    if cupp_group in groupA_cupp_groups:
        group = "A"
    else:
        group = "B"
    # Check if enzyme has one of the abundant domains
    no_selected_domains = 0
    for domain in domains:
        domain_name = domain.split('(')[0]
        if domain_name in selected_domains:
            no_selected_domains += 1
            selected_domain = domain_name
    # Continue if it has more than one of the abundant domains
    if no_selected_domains > 1:
        print(domains)
    elif no_selected_domains == 0:
        continue
    # Write to one of the fasta files
    else:
        if group == "A":
            if selected_domain == "EpsG":
                groupA_EpsG_file.write(f">{accession}\n{seq}\n")
        elif group == "B":
            if selected_domain == "O-ag_pol_Wzy":
                groupB_O_ag_pol_Wzy_file.write(f">{accession}\n{seq}\n")
            elif selected_domain == "Wzy_C":
                groupB_Wzy_C_file.write(f">{accession}\n{seq}\n")
            elif selected_domain == "EpsG":
                groupB_EpsG_file.write(f">{accession}\n{seq}\n")
                """
A_EpsG_dict = dict()
B_O_ag_pol_Wzy_dict = dict()
B_Wzy_C_dict = dict()
B_EpsG_dict = dict()

A_no_domain_dict = dict()
B_no_domain_dict = dict()

groupA_cupp_groups = ["wzy1:1.1", "wzy1:8.1", "wzy1:1.2", "wzy1:84.1", "wzy1:67.1", "wzy1:70.1", "wzy1:469.1", "wzy1:148.1", "wzy1:57.1", "wzy1:330.1"]
selected_domains = ["O-ag_pol_Wzy", "Wzy_C", "EpsG"]

for line in infile:
    if line.startswith("#"):
        continue
    splitted_line = line.strip().split("\t")
    accession = splitted_line[0]
    cupp_group = splitted_line[7]
    seq = splitted_line[46]
    domains = splitted_line[18].split('+')
    # Remove original entries that were sorted out in CD-HIT
    if cupp_group.endswith("*"):
        continue
    # Divide in A and B
    if cupp_group in groupA_cupp_groups:
        group = "A"
    else:
        group = "B"
    # Check if enzyme has one of the abundant domains
    no_selected_domains = 0
    for domain in domains:
        domain_name = domain.split('(')[0]
        if domain_name in selected_domains:
            no_selected_domains += 1
            selected_domain = domain_name
    # Count in negative dict
    if no_selected_domains != 1:
        if group == "A":
            if cupp_group not in A_no_domain_dict:
                A_no_domain_dict[cupp_group] = []
            A_no_domain_dict[cupp_group].append([accession, seq])
        if group == "B":
            if cupp_group not in B_no_domain_dict:
                B_no_domain_dict[cupp_group] = []
            B_no_domain_dict[cupp_group].append([accession, seq])
    # Count in positive dicts
    else:
        if group == "A":
            if selected_domain == "EpsG":
                if cupp_group not in A_EpsG_dict:
                    A_EpsG_dict[cupp_group] = []
                A_EpsG_dict[cupp_group].append([accession, seq])
        elif group == "B":
            if selected_domain == "O-ag_pol_Wzy":
                if cupp_group not in B_O_ag_pol_Wzy_dict:
                    B_O_ag_pol_Wzy_dict[cupp_group] = []
                B_O_ag_pol_Wzy_dict[cupp_group].append([accession, seq])
            elif selected_domain == "Wzy_C":
                if cupp_group not in B_Wzy_C_dict:
                    B_Wzy_C_dict[cupp_group] = []
                B_Wzy_C_dict[cupp_group].append([accession, seq])
            elif selected_domain == "EpsG":
                if cupp_group not in B_EpsG_dict:
                    B_EpsG_dict[cupp_group] = []
                B_EpsG_dict[cupp_group].append([accession, seq])

infile.close()

groupA_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupA_EpsG_whole_group.fsa", "w")
groupB_O_ag_pol_Wzy_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_O-ag_pol_Wzy_whole_group.fsa", "w")
groupB_Wzy_C_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_Wzy_C_whole_group.fsa", "w")
groupB_EpsG_file = open("C:/Users/s153020/Documents/HCP Anywhere/kristian_polymerase_analyse/groupB_EpsG_whole_group.fsa", "w")

# Write to file if more than half of a cupp group has the domain
for group in A_EpsG_dict:
    try:
        if len(A_EpsG_dict[group]) > A_no_domain_dict[group]:
            for i in range(len(A_EpsG_dict[group])):
                acc, seq = A_EpsG_dict[group][i]
                groupA_EpsG_file.write(f">{acc}\n{seq}\n")
            for i in range(len(A_no_domain_dict[group])):
                acc, seq = A_no_domain_dict[group][i]
                groupA_EpsG_file.write(f">{acc}\n{seq}\n")
    except:
        for i in range(len(A_EpsG_dict[group])):
            acc, seq = A_EpsG_dict[group][i]
            groupA_EpsG_file.write(f">{acc}\n{seq}\n")
for group in B_EpsG_dict:
    try:
        if len(B_EpsG_dict[group]) > B_no_domain_dict[group]:
            for i in range(len(B_EpsG_dict[group])):
                acc, seq = B_EpsG_dict[group][i]
                groupB_EpsG_file.write(f">{acc}\n{seq}\n")
            for i in range(len(B_no_domain_dict[group])):
                acc, seq = B_no_domain_dict[group][i]
                groupB_EpsG_file.write(f">{acc}\n{seq}\n")
    except:
        for i in range(len(B_EpsG_dict[group])):
            acc, seq = B_EpsG_dict[group][i]
            groupB_EpsG_file.write(f">{acc}\n{seq}\n")
for group in B_O_ag_pol_Wzy_dict:
    try:
        if len(B_O_ag_pol_Wzy_dict[group]) > B_no_domain_dict[group]:
            for i in range(len(B_O_ag_pol_Wzy_dict[group])):
                acc, seq = B_O_ag_pol_Wzy_dict[group][i]
                groupB_O_ag_pol_Wzy_file.write(f">{acc}\n{seq}\n")
            for i in range(len(B_no_domain_dict[group])):
                acc, seq = B_no_domain_dict[group][i]
                groupB_O_ag_pol_Wzy_file.write(f">{acc}\n{seq}\n")
    except:
        for i in range(len(B_O_ag_pol_Wzy_dict[group])):
            acc, seq = B_O_ag_pol_Wzy_dict[group][i]
            groupB_O_ag_pol_Wzy_file.write(f">{acc}\n{seq}\n")
for group in B_Wzy_C_dict:
    try:
        if len(B_Wzy_C_dict[group]) > B_no_domain_dict[group]:
            for i in range(len(B_Wzy_C_dict[group])):
                acc, seq = B_Wzy_C_dict[group][i]
                groupB_Wzy_C_file.write(f">{acc}\n{seq}\n")
            for i in range(len(B_no_domain_dict[group])):
                acc, seq = B_no_domain_dict[group][i]
                groupB_Wzy_C_file.write(f">{acc}\n{seq}\n")
    except:
        for i in range(len(B_Wzy_C_dict[group])):
            acc, seq = B_Wzy_C_dict[group][i]
            groupB_Wzy_C_file.write(f">{acc}\n{seq}\n")

groupA_EpsG_file.close()
groupB_O_ag_pol_Wzy_file.close()
groupB_Wzy_C_file.close()
groupB_EpsG_file.close()
