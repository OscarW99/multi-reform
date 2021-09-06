# multi-reform
A command-line script for editing genome files.

multi-reform is a modification of the reform tool (https://github.com/gencorefacility/reform) to allow for multiple edits to genome sequence (fasta) and genome sequence annotation (gff) files. This is a command line tool that requires only reform and Python 3 with the Biopython package insatlled.

multi-reform has three required inputs; A fasta file of the genome, a gff annotation file of the genome, and an excel spreadsheet containing information about the genome edits to be made. The excel spreadsheet can be donloaded from this repository (https://github.com/OscarW99/multi-reform/blob/main/custom_genome_and_annotation_sheet.xlsx) and instructions on how to fill it in are below.

![multi-reform flow diagram](https://github.com/OscarW99/multi-reform/blob/main/Multi-reform.png?raw=true)

