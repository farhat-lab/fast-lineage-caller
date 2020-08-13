from importlib import reload
import sys
import re


def read_snp_schemes(list_snp_schemes: str) -> dict:
    """
    Reads a directory with SNP schemes. Returns a dictionary representation of the SNP schemes.
    """
    d_snps = {}
    d_tags = {}
    d_snps_per_tag_lineage = {}
    list_allele_changes_isolates_not_same_lineage_reference = [] # if these snps are present
    # we are dealing with a strain that does NOT have the same lineage as the
    # reference strain
    for current_file in list_snp_schemes:
        re_to_check_ref_strain_lineage = re.compile("\*\*$")
        with open(current_file, "r") as inp:
            for line in inp:
                if line.startswith("#"):
                    continue
                data = line.rstrip("\n").split("\t")
                lineage = data[0]
                pos = data[1]
                allele_change = "_".join([pos, data[2]])
                tag = data[3]
                d_tags[tag]=1
                if allele_change not in d_snps:
                    d_snps[allele_change]={}
                d_snps[allele_change][tag]={}
                if bool(re_to_check_ref_strain_lineage.search(data[0])):
                    list_allele_changes_isolates_not_same_lineage_reference.append(allele_change)
                    lineage = lineage.replace("*","")
                d_snps[allele_change][tag][lineage]={}
                # I populat the d_tags_snps_per_lineage dictionary (important to calculate the SNPs per lineage per tag)
                if tag not in d_snps_per_tag_lineage:
                    d_snps_per_tag_lineage[tag]={}
                if lineage not in d_snps_per_tag_lineage[tag]:
                    d_snps_per_tag_lineage[tag][lineage]={}
                d_snps_per_tag_lineage[tag][lineage][allele_change]={}
    list_tags = sorted(d_tags.keys())
    return(d_snps, list_allele_changes_isolates_not_same_lineage_reference, list_tags, d_snps_per_tag_lineage)


