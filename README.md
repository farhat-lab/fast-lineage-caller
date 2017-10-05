#The following commands were launched inside the strain_typed directory 


#########################################
##I try to characterize M. tuberculosis##
#########################################

#I select from the table the strains for which we have a complete genome
head -1 table_1773.tsv > table_complete_genomes_1773.tsv 
cat table_1773.tsv |grep "Complete Genome" >> table_complete_genomes_1773.tsv

#I download the genomes
~/lf61/check_strains_maha/scripts/download-fasta-from-tables.py table_complete_genomes_1773.tsv 1 10000
gunzip *.fna.gz

#rename the files to fasta
for i in `ls|grep fna|sed -e 's/.fna//'`;do mv ${i}.fna ${i}.fasta;done

#I characterize the strains
for i in `ls|grep fasta`;do
echo "--strain: "${i}
~/lf61/mic_assemblies/18-pilot_cmp_pilon_denovo_00-R0025/bin/run_mummer.py ../../data/h37rv.fasta ${i} mummer
~/lf61/mic_assemblies/18-pilot_cmp_pilon_denovo_00-R0025/bin/snps2vrt.py mummer.snps ../../data/h37rv.fasta ${i} out.vrt
~/lf61/check_strains_maha/12-strain-typing/bin/assign2lineage.py ~/lf61/check_strains_maha/12-strain-typing/data/db_snps.tsv out.vrt 
done > log_assignments.txt

cat log_assignments.txt |grep "^--" > tmp_assignments.txt

cat tmp_assignments.txt |tr -d "\n"|sed -e 's/.fasta//g'|sed -e 's/--decision://g'|sed -e 's/--strain://g'|sed -e 's/GCA/\nGCA/g' > final_table.tsv

#I generated an ods file -- it is easier to put some notes.
#I get the names of the strains
for i in `ls|grep fasta|sed -e 's/.fasta//'`;do printf ${i}"\t";head -1 ${i}.fasta|cut -d" " -f4-10|sed -e 's/, complete genome//';done


######################################
##I try to characterize M. africanum##
######################################
mkdir africanum
head -1 table_33894.tsv > table_complete_genomes_33894.tsv 
cat table_33894.tsv |grep "Complete Genome" >> table_complete_genomes_33894.tsv

#I downloaded the genomes by hand since there was a problem with the download script (ERROR 500: Internal Server Error)
gunzip *.fna.gz


#rename the files to fasta
for i in `ls|grep fna|sed -e 's/.fna//'`;do mv ${i}.fna ${i}.fasta;done

#I characterize the strains
for i in `ls|grep fasta`;do
echo "--strain: "${i}
~/lf61/mic_assemblies/18-pilot_cmp_pilon_denovo_00-R0025/bin/run_mummer.py ../../data/h37rv.fasta ${i} mummer
~/lf61/mic_assemblies/18-pilot_cmp_pilon_denovo_00-R0025/bin/snps2vrt.py mummer.snps ../../data/h37rv.fasta ${i} out.vrt
~/lf61/check_strains_maha/12-strain-typing/bin/assign2lineage.py ~/lf61/check_strains_maha/12-strain-typing/data/db_snps.tsv out.vrt 
done > log_assignments.txt

cat log_assignments.txt |grep "^--" > tmp_assignments.txt

cat tmp_assignments.txt |tr -d "\n"|sed -e 's/.fasta//g'|sed -e 's/--decision://g'|sed -e 's/--strain://g'|sed -e 's/GCA/\nGCA/g' > final_table.tsv


#I made my selection of strains. I am missing strains from lineages 5 and 7
#the final selection can be found on the directory selection_strains








