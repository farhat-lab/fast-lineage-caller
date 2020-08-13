
import sys
sys.path.append('.')
from fast_lineage_caller import utils

def assign_lineage_from_vcf(id_isolate: str, vcf: str, dict_snp_schemes: dict, list_allele_changes_not_same_lineage_reference: list, tag_list: list, print_header: str, out_file: str, rem_redundancy: int, pass_filter: int) -> None:
    """
    Takes dict with one or multiple SNP schemes, a VCF and the list of positions that define 
    lineage allele changes in the reference and returns the lineage calls
    """
    lineage_assignments = {} # I will store the lineage assigmnments here
    d_ref_strain_lineage_snps = {}
    for allele in list_allele_changes_not_same_lineage_reference:
        d_ref_strain_lineage_snps[allele] = True
    with open(vcf, "r") as inp:
        for line in inp:
            if line.startswith("#"):
                continue
            else:
                data_vcf = line.rstrip("\n").split("\t")
                #check the PASS filter
                if (pass_filter == 1):
                    pass_info = data_vcf[6]
                    if pass_info != "PASS":
                        continue
                pos = data_vcf[1]
                ref_alt = "/".join([data_vcf[3], data_vcf[4]])
                current_allele = "_".join([pos, ref_alt])
                if current_allele in dict_snp_schemes:
                    if current_allele in d_ref_strain_lineage_snps:
                        d_ref_strain_lineage_snps[current_allele] = False
                    else:
                        list_tags=dict_snp_schemes[current_allele].keys()
                        for tag in list_tags:
                            if tag not in lineage_assignments:
                                lineage_assignments[tag]={}
                            for lineage_assigned in dict_snp_schemes[current_allele][tag]:
                                lineage_assignments[tag][lineage_assigned]={}
    for current_allele in d_ref_strain_lineage_snps:
        if d_ref_strain_lineage_snps[current_allele]:
            list_tags=dict_snp_schemes[current_allele].keys()
            for tag in list_tags:
                if tag not in lineage_assignments:
                    lineage_assignments[tag]={}
                for lineage_assigned in dict_snp_schemes[current_allele][tag]:
                    lineage_assignments[tag][lineage_assigned]={}
    #print(lineage_assignments)
    if rem_redundancy == 1:
        final_lineage_assignments = utils.remove_redundancy(lineage_assignments)
    else:
        final_lineage_assignments = lineage_assignments
    utils.write_down_results(id_isolate, final_lineage_assignments, tag_list, print_header, out_file)


def assign_lineage_from_vcf_snp_counts(id_isolate: str, vcf: str, dict_snp_schemes: dict, list_allele_changes_not_same_lineage_reference: list, tag_list: list, dict_snps_per_tag_lineage: dict, print_header: str, out_file: str, rem_redundancy: int, pass_filter: int) -> None:
    """
    Takes dict with one or multiple SNP schemes, a VCF and the list of positions that define 
    lineage allele changes in the reference and returns the lineage calls
    """
    #print(dict_snp_schemes)
    lineage_assignments = {} # I will store the lineage assigmnments here
    d_ref_strain_lineage_snps = {}
    for allele in list_allele_changes_not_same_lineage_reference:
        d_ref_strain_lineage_snps[allele] = True
    with open(vcf, "r") as inp:
        for line in inp:
            if line.startswith("#"):
                continue
            else:
                data_vcf = line.rstrip("\n").split("\t")
                #check the PASS filter
                if (pass_filter == 1):
                    pass_info = data_vcf[6]
                    if pass_info != "PASS":
                        continue
                pos = data_vcf[1]
                ref_alt = "/".join([data_vcf[3], data_vcf[4]])
                current_allele = "_".join([pos, ref_alt])
                if current_allele in dict_snp_schemes:
                    if current_allele in d_ref_strain_lineage_snps:
                        d_ref_strain_lineage_snps[current_allele] = False
                    else:
                        list_tags=dict_snp_schemes[current_allele].keys()
                        for tag in list_tags:
                            if tag not in lineage_assignments:
                                lineage_assignments[tag]={}
                            for lineage_assigned in dict_snp_schemes[current_allele][tag]:
                                if lineage_assigned not in lineage_assignments[tag]:
                                    lineage_assignments[tag][lineage_assigned]={}
                                    lineage_assignments[tag][lineage_assigned]=1
                                else:
                                    lineage_assignments[tag][lineage_assigned] = lineage_assignments[tag][lineage_assigned] + 1
    for current_allele in d_ref_strain_lineage_snps:
        if d_ref_strain_lineage_snps[current_allele]:
            list_tags=dict_snp_schemes[current_allele].keys()
            for tag in list_tags:
                if tag not in lineage_assignments:
                    lineage_assignments[tag]={}
                for lineage_assigned in dict_snp_schemes[current_allele][tag]:
                    if lineage_assigned not in lineage_assignments[tag]:
                        lineage_assignments[tag][lineage_assigned]={}
                        lineage_assignments[tag][lineage_assigned]=1
                    else:
                        lineage_assignments[tag][lineage_assigned] = lineage_assignments[tag][lineage_assigned] + 1
    #print(lineage_assignments)
    if rem_redundancy == 1:
        final_lineage_assignments = utils.remove_redundancy(lineage_assignments)
    else:
        final_lineage_assignments = lineage_assignments
    #print(final_lineage_assignments)
    utils.write_down_results_snp_counts(id_isolate, final_lineage_assignments, tag_list, dict_snps_per_tag_lineage, print_header, out_file)

