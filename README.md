## Purpose
Quickly call lineages from `.vcf` files using different SNP schemes. The package will be developed primarily to call *Mtb* (_Mycobacterium tuberculosis_) lineages, but if you build your own SNP scheme you can use it to call lineages for virtually any bacterial species.

## Installation

### with pip

```
pip install fast-lineage-caller
```

### with conda

```
conda install -c ejfresch fast-lineage-caller
```

## Usage
### Basic usage
The simplest way to call the lineages is to provide a `.vcf` file to `fast-lineage-caller`:
```
fast-lineage-caller genomic_data/SAMEA968141.vcf 
```
The program will output the lineage calls according to the available SNP schemes
```
Isolate coll2014        freschi2020     lipworth2019    shitikov2017    stucki2016
SAMEA968141     lineage2.2.1    2.2.1.1.1       beijing lin2.2.1,asian_african_2        NA
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
SAMEA968141     lineage2.2.1    2.2.1.1.1       beijing lin2.2.1,asian_african_2        NA
```

Sometimes this option is very useful, for instance when you have a lot of `vcf` files (see below).

### Counting the SNPs that support a given lineage call

SNP schemes can include one or multiple SNP that define one lineage / sub-lineage. In order to get the conts of the number of SNPs that support each lineage call, you can use the `--count` option:

```
fast-lineage-caller genomic_data/SAMEA968141.vcf --count
Isolate coll2014        freschi2020     lipworth2019    shitikov2017    stucki2016
SAMEA968141     lineage2.2.1(1/1)       2.2.1.1.1(1/1)  beijing(296/296)        lin2.2.1(3/3),asian_african_2(2/2)      NA
```

### Calling lineages on thousands of VCFs

The simplest way to process thousands of VCFs is to use a `for` loop. You put your `vcf` files in one folder and then type:

```
for i in `ls |grep ".vcf"`; do
fast-lineage-caller genomic_data/SAMEA968141.vcf --noheader
done >> results.tsv
```

### Getting all the lineage calls without removing any redundancy

By default *fast-lineage-caller* will try to remove the redundancy in the lineage calls. What does this mean? The isolate `SAMEA968141`, for instance, belongs to the `lineage2.2.1` (according to the *coll2014* SNP scheme).  When *fast-lineage-caller* checks the variants present in the *vcf* of this isolate, it will find that it actually belongs to `lineage2`, `lineage2.2` and `lineage2.2.1`. The information contained in some these labels is redundant, so *fast-lineage-caller* by default will output only `lineage2.2.1`. However, for some use-cases it is relevant to get all the calls. You can do that by using the `--keep` (keep redundancy) option:

```
fast-lineage-caller genomic_data/SAMEA968141.vcf --keep
Isolate coll2014        freschi2020     lipworth2019    shitikov2017    stucki2016
SAMEA968141     lineage2,lineage2.2.1,lineage2.2        2,2.2.1.1,2.2.1.1.1,2.2.1,2.2   beijing lin2,lin2.2.1,asian_african_2,lin2.2    NA
```

## SNP schemes

### Default SNP schemes (for *Mtb*)

These are the SNP schemes currently available on `fast-lineage-caller`. They are the most widely used SNP schemes to call Mycobacterium tuberculosis lineages / sub-lineages. However, if this is not enough or you want to use `fast-lineage-caller` to call lineages in other bacterial species, please remember that you can build your own SNP scheme (see section below).

| Tag          | Reference                                                    | Notes                                                        |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| coll2014     | Coll, F. *et al.* A robust SNP barcode for typing Mycobacterium tuberculosis complex strains. *Nat. Commun.* **5**, 4812 (2014) |                                                              |
| lipworth2019 | Samuel Lipworth *et al.* SNP-IT Tool for Identifying Subspecies and Associated Lineages of Mycobacterium tuberculosis Complex. *Emerging Infectious Disease journal* **25**, (2019) | This SNP barcode is implemented in [SNPit](https://github.com/philipwfowler/snpit). |
| freschi2020  | Soon on BioRXiv!                                             |                                                              |
| shitikov2017 | Shitikov, E. *et al.* Evolutionary pathway analysis and unified classification of East Asian lineage of Mycobacterium tuberculosis. *Sci. Rep.* **7**, 9227 (2017) |                                                              |
| stucki2016   | Stucki, D. *et al.* Mycobacterium tuberculosis lineage 4 comprises globally distributed and geographically restricted sublineages. *Nat. Genet.* **48**, 1535–1543 (2016) |                                                              |

### Building your own SNP scheme

You just need to create a `.tsv` file (it is a tab separated value file) with the following columns:

|    Column     | Description                                                  |
| :-----------: | ------------------------------------------------------------ |
|    lineage    | Name of the lineage or group of isolates                     |
|   position    | Genomic position of the SNP in the reference sequence (usually H37Rv for *Mtb*) |
| allele_change | `<Reference_allele>/<Alternate_allele>`. For instance: `C/T`. |
|      tag      | Name of this SNP scheme                                      |

**Note: please remember that the order the columns is important!**



Here is an example. I created a new file named `my_snp_scheme.tsv`:

```
#lineage        position        allele_change   tag
lineage2        497491  G/A     new_SNP_scheme
lineage2.2      2505085 G/A     new_SNP_scheme
```

**Note**: the SNP scheme parser skips all the lines that start with a `#`, so you can put a `#` at the beginning of the line if you want to add comments or temporarily remove SNPs from a SNP scheme.



Now you can use `fast-lineage-caller` to call the lineages with the new SNP scheme:

```
fast-lineage-caller genomic_data/SAMEA968141.vcf --scheme ./my_snp_scheme.tsv 
Isolate new_SNP_scheme
SAMEA968141     lineage2.2
```



## Changelog

Version 0.3.1

- previous versions of fast-lineage-caller (0.1-0.3) contained an outdated version of the freschi2020 barcode (bugfix; critical; please upgrade from 0.3)
- if the user did  not use the `--count` function, the program was returning `<blank>` instead of `NA` when no SNP was found in the .vcf for a given SNP scheme (bugfix)
- improved documentation: simpler and more consistent examples (README.md)

Version 0.3

- the user can choose to use all the variants (default) or only the ones with the PASS flag for the lineage calling: `--pass` option (feature)
- show a denominator when counting the SNPs (`--count` option) (bugfix)
- renamed the option `--keepred` to `--keep` (bugfix)
- use `NA` instead of ` <blank>` as output when no SNP is found in the .vcf for a given SNP scheme (bugfix)

Version 0.2

- the user can decide to  remove (default) or keep the redundant lineage calls: `--keep` option (feature)
- the user can get the count of the SNPs that support a given lineage call: `--count` option (feature)
- module available on conda (feature)
- added information on how to build a custom SNP scheme (feature)
- if multiple SNP schemes had the same SNP defining a given lineage / sub-lineage, only the lineage call of the last parsed SNP scheme was present in the output (bugfix; critical; please upgrade from 0.1)

Version 0.1

- working python module (uploaded to pypi), only able to accept `vcf` files

