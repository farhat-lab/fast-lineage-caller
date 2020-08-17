import re
import os

def extract_file_name(file_name: str, file_type: str) -> str:
    extracted = os.path.basename(file_name)
    extracted_noext = extracted.replace("."+file_type,"")
    return(extracted_noext)

def detect_file_type(file_name: str) -> str:
    """
    Reads a file name and determines the file type from the extension
    """
    file_type = ""
    if re.search(r'\.vcf$', file_name):
        file_type = "vcf"
    elif re.search(r'\.fasta$', file_name):
        file_type = "fasta"
    return(file_type)


def write_down_results(id_isolate: str, d: dict, tag_list: list, print_header: str, out_file: str) -> None:
    to_print=[]
    for tag in sorted(tag_list):
        if tag in d:
            to_print.append(",".join(d[tag].keys()))
        else:
            to_print.append("NA")
    if not out_file:
        if print_header == "y":
            print("Isolate\t"+"\t".join(sorted(tag_list)))
        print(id_isolate+"\t"+"\t".join(to_print))
    else:
        with open(out_file,"w") as outf:
            if print_header == "y":
                outf.write("Isolate\t"+"\t".join(sorted(tag_list)) + "\n")
                outf.write(id_isolate+"\t"+"\t".join(to_print) + "\n")

def write_down_results_snp_counts(id_isolate: str, d: dict, tag_list: list, dict_snps_per_tag_lineage: dict, print_header: str, out_file: str) -> None:
    to_print=[]
    for tag in sorted(tag_list):
        if tag in d:
            #print([l+"(" + str(d[tag][l]) + ")" for l in d[tag].keys()])
            lcalls_counts = ",".join([l+"(" + str(d[tag][l]) + "/" + str(len(dict_snps_per_tag_lineage[tag][l])) + ")" for l in d[tag].keys()])
            to_print.append(",".join([lcalls_counts]))
        else:
            to_print.append("NA")
    if not out_file:
        if print_header == "y":
            print("Isolate\t"+"\t".join(sorted(tag_list)))
        print(id_isolate+"\t"+"\t".join(to_print))
    else:
        with open(out_file,"w") as outf:
            if print_header == "y":
                outf.write("Isolate\t"+"\t".join(sorted(tag_list)) + "\n")
                outf.write(id_isolate+"\t"+"\t".join(to_print) + "\n")



def remove_redundancy(d: dict) -> dict:
    non_red_d={}
    for tag in d:
        non_red_d[tag]={}
        for l in d[tag]:
            if not any([l in r for r in d[tag] if l != r]):
                non_red_d[tag][l]=d[tag][l]
    return(non_red_d)

