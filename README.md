# multi-reform
### A command-line script for editing genome files.

multi-reform is a modification of the reform tool (https://github.com/gencorefacility/reform) to allow for multiple edits to genome sequence (fasta) and genome sequence annotation (gff) files. This is a command line tool that requires only reform and Python 3 with the Biopython package insatlled.

multi-reform has three required inputs; A fasta file of the genome, a gff annotation file of the genome, and an excel spreadsheet containing information about the genome edits to be made. The excel spreadsheet can be donloaded from this repository (https://github.com/OscarW99/multi-reform/blob/main/custom_genome_and_annotation_sheet.xlsx) and instructions on how to fill it in are below.<br />
<br />

![multi-reform flow diagram](https://github.com/OscarW99/multi-reform/blob/main/Multi-reform.png?raw=true) <br />
<br />

## Installing and running mutli-reform
...


## How to fill out the excel spreadsheet:
Fill out one row of the excel spreadsheet for each insertion or deletion to be made. <br />

![unfilled_excel spreadsheet](https://github.com/OscarW99/multi-reform/blob/main/unfilled_excel.PNG?raw=true) <br />

There are 6 columns to fill out. (1) Either insertion or deletion, (2) the name of the edit, (3) the name of the chromosome the edit is on (must be the same naming convention as in gff file), (4) the start position of the deletion or position of insertion, (5) the end position of the deletion (Not required for insertions), and finally (6) the sequence to be inserted (leave blank for deletions). <br />
<br />
Below is an exampe of a filled in spreadsheet.
<br />
![filled_excel_spreadsheet](https://github.com/OscarW99/multi-reform/blob/main/filled.PNG?raw=true) <br />
1) In the first row is an insertion which we name Cluster_insert. It is on a chromosome labelled chr05 in the gff file. We want to insert the sequence at base position 2334. End position is not required for inserts. In the final column we paste the sequence to be inserted. 
2) In the second row we want to delete a sequence called 'gene_name' on chromosome 'chr03'. The sequence begins at base position 344,555 and ends at position 345892. As we have no replacement sequence we do not fill in the last column.
3) In the third column we want to delete a sequence we call 'CLN2' on a chromsome called 'chr16'. The sequence begins at base position 64,977 and ends at position 66,614. This time we want to insert a sequence in place of the deletion and so we paste this into the final column.

Note the sequence name does not have to be the same as any gene name, it can be whatever you want. The sequence name will be used in the edited gff file.
