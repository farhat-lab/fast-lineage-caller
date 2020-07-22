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
fast-lineage-caller ~/mfarhat/rollingDB/genomic_data/SAMEA968141/pilon/SAMEA968141.vcf 
```
The program will output the lineage calls according to the available SNP schemes
```
Isolate coll2014        freschi2020     lipworth2019    shitikov2017
SAMEA968141                     beijing asian_african_2,lin2.2.1
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

### Calling lineages on thousands of VCFs

The simplest way to process thousands of VCFs is to use a `for` loop. You put your `vcf` files in one folder and then type:

```
for i in `ls |grep ".vcf"`; do
fast-lineage-caller genomic_data/SAMEA968141.vcf --noheader
done >> results.tsv
```

# Changelog (roadmap)

Version 0.1
- working python module (uploaded to pypi)

