#!/usr/bin/env python

import sys
import subprocess as sp

if len(sys.argv)!=3:
	print "::usage: %s <db_snps> <vrt_file>" % sys.argv[0]
	sys.exit()

db_snps=sys.argv[1]
vrt_file=sys.argv[2]


#I build a db with the SNPs
snps={}

with open(db_snps,"r") as inp:
	for line in inp:
		if line.startswith("#"):
			continue
		data=line.rstrip("\n").split("\t")
		pos=data[1]
		snps[pos]={}
		snps[pos]["l"]={}
		snps[pos]["l"]=data[0]

		snp=data[3].split("/")
		snps[pos]["ref"]={}
		snps[pos]["ref"]=snp[0]
		snps[pos]["alt"]={}
		snps[pos]["alt"]=snp[1]

assignments={}

check_1759252=0
check_931123=0

with open(vrt_file,"r") as inp:
	for line in inp:
		data=line.rstrip("\n").split("\t")
		pos=data[1]
		if pos in snps.keys():
			ref=data[2]
			alt=data[3]
			if pos==str(1759252):
				if (ref==snps[pos]["ref"]) and (alt==snps[pos]["alt"]):
					check_1759252=1
					continue
			if pos==str(931123):
				if (ref==snps[pos]["ref"]) and (alt==snps[pos]["alt"]):
					check_931123=1
					continue
			if(ref==snps[pos]["ref"]) and (alt==snps[pos]["alt"]):
				lineage=snps[pos]["l"]
				assignments[lineage]=1

if check_931123==0:
	assignments["lineage4"]=1
if check_1759252==0:
	assignments["lineage4.9"]=1


print "--decision: "+",".join(sorted(assignments.keys()))




