## Purpose
Quickly call lineages from `.vcf` files using different SNP schemes. The package will be developed primarily to call *Mtb* (_Mycobacterium tuberculosis_) lineages, but if you build your own SNP scheme you can use it to call lineages for virtually any bacterial species.

## Installation
```
pip install fast-lineage-caller
```

## Usage
### Basic usage
The simplest way to call the lineages is to provide a `.vcf` file to `fast-lineage-caller`:
```
./bin/fast-lineage-caller genomic_data/SAMEA968141.vcf 
```
The program will output the lineage calls according to the available SNP schemes
```
Isolate coll2014        freschi2020     lipworth2019    shitikov2017
SAMEA968141     lineage2.2.1    2.2.1.1.1       beijing lin2.2.1,asian_african_2 
```
### Saving the output on a text file
It is possible to save the lineage calls on a text (`.tsv`) file using the `--out` option: 
```
fast-lineage-caller genomic_data/SAMEA968141.vcf --out results.tsv
```
### Using a custom SNP scheme
It is possible to call the lineages using a custom SNP scheme defined by the user: 
```
fast-lineage-caller genomic_data/SAMEA968141.vcf --scheme my_snp_schemes/freschi.tsv
```
### No header, please
It is possible to tell the `fast-lineage-caller` to do not display the header, *i.e.* the first line of the output that shows for instance the names of the SNP schemes:

```
fast-lineage-caller genomic_data/SAMEA968141.vcf --noheader
SAMEA968141                     beijing asian_african_2,lin2.2.1
```

Sometimes this option is very useful, for instance when you have a lot of `vcf` files (see below).

### Counting the SNPs that support a given lineage call

SNP schemes can include one or multiple SNP that define one lineage / sub-lineage. In order to get the conts of the number of SNPs that support each lineage call, you can use the `--count` option:

```
./bin/fast-lineage-caller ~/mfarhat/rollingDB/genomic_data/SAMEA968141/pilon/SAMEA968141.vcf --count
Isolate coll2014        freschi2020     lipworth2019    shitikov2017    stucki2016
SAMEA968141     lineage2.2.1(1) 2.2.1.1.1(1)    beijing(296)    lin2.2.1(3),asian_african_2(2)
```

### Calling lineages on thousands of VCFs

The simplest way to process thousands of VCFs is to use a `for` loop. You put your `vcf` files in one folder and then type:

```
for i in `ls |grep ".vcf"`; do
fast-lineage-caller genomic_data/SAMEA968141.vcf --noheader
done >> results.tsv
```

### Getting all the lineage calls without removing any redundancy

By default *fast-lineage-caller* will try to remove the redundancy in the lineage calls. What does this mean? The isolate `SAMEA968141`, for instance, belongs to the `lineage2.2.1` (according to the *coll2014* SNP scheme).  When *fast-lineage-caller* checks the variants present in the *vcf* of this isolate, it will find that it actually belongs to `lineage2`, `lineage2.2` and `lineage2.2.1`. The information contained in some these labels is redundant, so *fast-lineage-caller* by default will output only `lineage2.2.1`. However, for some use-cases it is relevant to get all the calls. You can do that by using the `--keepred` (keep redundancy) option:

```
./bin/fast-lineage-caller genomic_data/SAMEA968141.vcf --keepred
Isolate coll2014        freschi2020     lipworth2019    shitikov2017    stucki2016
SAMEA968141     lineage2,lineage2.2.1,lineage2.2        2,2.2.1.1,2.2.1,2.2.1.1.1,2.2   beijing lin2,lin2.2.1,asian_african_2,lin2.2
```

# Changelog

Version 0.2

- the user can decide to  remove (default) or keep the redundant lineage calls: `--keepred` option (feature)
- the user can get the count of the SNPs that support a given lineage call: `--count` option (feature)
- if multiple SNP schemes had the same SNP defining a given lineage / sub-lineage, only the lineage call of the last parsed SNP scheme was shown (bugfix; critical; please update from 0.1)

Version 0.1

- working python module (uploaded to pypi), only able to accept `vcf` files

