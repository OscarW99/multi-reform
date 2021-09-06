### multi-reform
A command-line script for editing genome files.

multi-reform is a modification of the reform tool (https://github.com/gencorefacility/reform) to allow for multiple edits to genome sequence (fasta) and genome sequence annotation (gff) files. This is a command line tool that requires only reform and Python 3 with the Biopython package insatlled.

multi-reform has three required inputs; A fasta file of the genome, a gff annotation file of the genome, and an excel spreadsheet containing information about the genome edits to be made. The excel spreadsheet can be donloaded from this repository (https://github.com/OscarW99/multi-reform/blob/main/custom_genome_and_annotation_sheet.xlsx) and instructions on how to fill it in are below.
\

![multi-reform flow diagram](https://github.com/OscarW99/multi-reform/blob/main/Multi-reform.png?raw=true)

## Installing and running mutli-reform
...


## How to fill out the excel spreadsheet:
The excel spreadsheet should contain a row for each insertion or deletion to be made.
There are 6 columns to fill out. Whether the edit is an insertion or deletion, the name of the edit (for the annotation file), The name of the chromosome the edit is on (must be the same naming convention as gff file), the start position of the deletion or position of insertion, the end position of the deletion (leave blank for insertions), and finally the sequence to be inserted (leave blank for deletions).


For an insertion, you 
For a deletion, you

If you want delete a sequence and insert a sequence in place of it (eg deleting gene and plcing a barcode in its place) then you...

