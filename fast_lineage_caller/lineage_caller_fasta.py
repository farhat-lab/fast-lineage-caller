#!/usr/bin/env python3

from importlib import reload
import argparse
import sys
import re

def read_snp_scheme(file_snp_scheme: str) -> tuple:
    """
    Reads a file with a SNP scheme. Returns a dictionary representation of the SNP scheme.
    """
    snp_scheme = {}
    list_positions_lineage_snps_reference = [] # if these snps are present
    # we are not dealing with a strain that has the same lineage as the
    # reference strain
    re_to_check_ref_strain_lineage = re.compile("\*\*$")
    with open(file_snp_scheme, "r") as inp:
        for line in inp:
            if line.startswith("#"):
                continue
            data = line.rstrip("\n").split("\t")
            pos = data[1]
            snp_scheme[pos] = {}
            snp_scheme[pos]["lineage"] = {}
            snp_scheme[pos]["to_check_ref_strain_lineage"] = {}
            if bool(re_to_check_ref_strain_lineage.search(data[0])):
                list_positions_lineage_snps_reference.append(pos)
                snp_scheme[pos]["lineage"] = data[0].replace("*","")
            else:
                snp_scheme[pos]["lineage"] = data[0]
            snp = data[3].split("/")
            snp_scheme[pos]["ref"] = {}
            snp_scheme[pos]["ref"] = snp[0]
            snp_scheme[pos]["alt"] = {}
            snp_scheme[pos]["alt"] = snp[1]
    return(snp_scheme, list_positions_lineage_snps_reference)

def assign_lineage(vcf: str, snp_scheme: dict, list_positions_lineage_snps_reference: list) -> str:
    """
    Takes a SNP scheme, a VCF and the list of positions that define lineage SNPs in the reference and returns the lineage calls
    """
    lineage_assignments = [] # I will store the lineage assigmnments here
    d_ref_strain_lineage_snps = {}
    for pos in list_positions_lineage_snps_reference:
        d_ref_strain_lineage_snps[pos] = False
    with open(vcf, "r") as inp:
        for line in inp:
            if line.startswith("#"):
                continue
            else:
                data_vcf = line.rstrip("\n").split("\t")
                pos = data_vcf[1]
                if pos in snp_scheme.keys():
                    ref = data_vcf[3]
                    alt = data_vcf[4]
                    if (ref == snp_scheme[pos]["ref"]) and (alt == snp_scheme[pos]["alt"]):
                        if pos in d_ref_strain_lineage_snps:
                            d_ref_strain_lineage_snps[pos] = True
                        else:
                            lineage_assignments.append(snp_scheme[pos]["lineage"])
    for pos in d_ref_strain_lineage_snps:
        if not d_ref_strain_lineage_snps[pos]:
            lineage_assignments.append(snp_scheme[pos]["lineage"])
    final_string = ",".join(sorted(set(lineage_assignments)))
    return(final_string)

parser = argparse.ArgumentParser()
parser.add_argument("vcf_file", type=str,
                    help="Input VCF (variants called against the reference of a given SNP scheme)")
parser.add_argument('snp_scheme', type=str,
                    help="TSV containing the SNP scheme")
args = parser.parse_args()

(snp_scheme, list_positions_lineage_snps_reference) = read_snp_scheme(args.snp_scheme)
lineage = assign_lineage(args.vcf_file, snp_scheme, list_positions_lineage_snps_reference)
print(lineage)
