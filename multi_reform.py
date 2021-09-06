"""
Multi-reform is a command-line script that takes 3 three arguemnts (excel_table, fasta_file, gff_file) and returns a .bat file
containing commands to run reform multiple times, each reform command makes an edit corresponing to a row in the excel file.
"""
# command-line arguments must be in order: excel_table fasta_file gff_file

## IMPORTS ##
import sys
import pandas as pd
import numpy as np
import os
import shutil

##############################################################################################
# function to take excel sheet and put in pandas DF
def to_df(excel_file):

	df = pd.read_excel(excel_file)
	#Get edits section of excel file
	edits_section = df.iloc[:, 0:6].dropna(how='all')
	edits_df_precurser = []
	for index, row in edits_section.iterrows():
		edits = [row[0].lower(), row[1].replace(" ", "_"), row[2], row[3], row[4], row[5]]
		edits_df_precurser.append(edits)


	# finalise deletions and insertions dataframe
	edits = pd.DataFrame(np.array(edits_df_precurser[1:]), columns=edits_df_precurser[0])
	edits['insertion/deletion'] = edits['insertion/deletion'].map({'insertion': 1, 'deletion':0})
	edits = edits.sort_values(by=[edits.columns[2], edits.columns[3]], ascending=[False,False])
	return edits



edits = to_df(sys.argv[1])
fasta_in_file = sys.argv[2]
gff_in_file = sys.argv[3]
print(edits)
##############################################################################################

# A function to remove the fasta sequences from a gff file if they are there
def remove_seq_from_gff(gff_file):
	final_lines = []
	with open(gff_file) as in_file:
		lines = in_file.readlines()
		for line in lines:
			if line == '##FASTA':
				break
			else:
				final_lines.append(line)
	with open(sys.argv[3], 'w') as out_file:
		for line in final_lines:
			out_file.write(line)


remove_seq_from_gff(gff_in_file)
gff_in_file = os.getcwd() + '/' + str(sys.argv[3])

##############################################################################################

# A function to check fasta header and gff header are the same
# and if they aren't, ask the user if they would like the program to automatically change them

def check_and_change_headers(fasta_file, gff_file):

	### get fasta headers and sequences into lists
	file = open(fasta_file)
	list_of_lines = file.readlines()
	file.close()
	fasta_headers = []
	seqs = []
	string = ""
	for line in list_of_lines:
	    if line.startswith('>'):
	        fasta_headers.append(line.strip())
	        if len(string) > 1:
	            seqs.append(string)  
	            string = ""
	    else:
	        string += line.strip()
	seqs.append(string)
	###

	# get the number of chromosomes
	num_chromosomes = len(fasta_headers)

	### get the gff headers & sequences
	file = open(gff_file)
	list_of_lines = file.readlines()
	file.close()
	gff_headers = []
	i = 0
	for line in list_of_lines:
		if line.startswith('#'):
			continue
		elif line.startswith(' '):
			continue
		else:
			if i >= num_chromosomes:
				break
			header = line.split('\t')[0]
			gff_headers.append(header)
			i += 1

	# check equal number of fasta and gff chromosmes
	if num_chromosomes != len(gff_headers):
		raise Exception('There are a different number of chromosomes in the Fasta and GFF file')

	if set(fasta_headers) != set(gff_headers):
		print('The names of chromosomes in fatsa file and gff file are different')
		change = input('Would you like us to automatically change the names? [y/n]')
		ans = ['y', 'yes']
		if change.lower() in ans: # if the user wishes, change all the fasta headers to match those in the gff
			new_fasta_headers = ['>' + name for name in gff_headers]
			fasta_zip = list(zip(new_fasta_headers, seqs))
			with open(fasta_in_file, "w") as in_file:
				for pair in fasta_zip:
					in_file.write(pair[0])
					in_file.write("\n")
					in_file.write(pair[1])
					in_file.write("\n")
			print('Fasta headers changed')
		else:
			print('Fasta headers must match the chromosome names in the gff file')
			sys.exit()


	else:
		print('Chromosome names in fasta and gff are the same :)')


check_and_change_headers(fasta_in_file, gff_in_file)

##############################################################################################


def get_reform_files(fasta_file, gff_file, df):

	# A function to get both the up and downstream 50bp and to create the fasta files of both (using unique naming convention)
	# Also create inset sequence using up and downstream sequences around actual insert sequence
	# also creat custom gff file

	batch_script = open('multi_reform.bat', 'w')

	### Creat dictionary of headers and sequences from fasta file ###
	with open(fasta_file, 'r') as in_file:
		list_of_lines = in_file.readlines()
	headers = []
	seqs = []
	string = ""
	for line in list_of_lines:
	    if line.startswith('>'):
	        headers.append(line.strip())
	        if len(string) > 1:
	            seqs.append(string)  
	            string = ""
	    else:
	        string += line.strip()
	seqs.append(string)
	pairs = dict(zip(headers,seqs))
	###
	### loop through df and create all files (fasta*3, gff)
	for index, row in df.iterrows():

		if row[0] == 0: # aka if edit is deletion

			directory_name = 'edits/' + row[1] #make directory to hold subfiles for each deletion edit
			if os.path.exists(directory_name):
				shutil.rmtree(directory_name)
			os.makedirs(directory_name)


			chromosome = '>' + row[2]
			start = int(row[3])
			end = int(row[4])
			
			### file contents ###
			upstream = pairs[chromosome][start-50:start]
			downstream = pairs[chromosome][end+1:end+51]
			insert = upstream + row[-1] + downstream
			gff = row[2] + '\t' + 'crispr_edit' + '\t' + 'engineered_insert' + '\t' + str(0) + '\t' + str(len(row[5])) + '\t' + '.' + '\t' + '+' + '\t' + '.' + '\t'+ 'ID=deletion_of_' + row[1] + ';Name=' + row[1] + '_barcode'
			# if closer than 50 to start?
			### file names ###
			upstream_file_name = 'edits/' + row[1] + '/' + row[1] + '_upstream.fa'
			downstream_file_name = 'edits/' + row[1] + '/' + row[1] + '_downstream.fa'
			insert_file_name = 'edits/' + row[1] + '/' + row[1] + '_insert.fa'
			gff_file_name = 'edits/' + row[1] + '/' + row[1] + '_deletion.gff'
			###
			### writing files ###
			with open(upstream_file_name, 'w') as in_file:
					header = '>'+row[1]+'_upstream'+'\n'
					in_file.write(header)
					in_file.write(upstream)
			with open(downstream_file_name, 'w') as in_file:
					header = '>'+row[1]+'_downstream'+'\n'
					in_file.write(header)
					in_file.write(downstream)
			with open(insert_file_name, 'w') as in_file:
					header = '>'+row[1]+'_insert'+'\n'
					in_file.write(header)
					in_file.write(insert)
			with open(gff_file_name, 'w') as in_file:
				in_file.write('##gff-version 3\n')
				in_file.write(gff)
			###
			### write reform command to batch script ###
			batch_script.write("python ~/bin/reform/reform.py --chrom='"+chromosome[1:]+"' --upstream_fasta='"+upstream_file_name+"'  --downstream_fasta='"+downstream_file_name+"' --in_fasta='"+insert_file_name+"' --in_gff='"+gff_file_name+"' --ref_fasta='"+fasta_file+"' --ref_gff='"+gff_file+"'\n")
			changed_fasta_name = fasta_file.split('.')[0] + '_reformed.fa'
			changed_gff_name = gff_file.split('.')[0] + '_reformed.gff'
			batch_script.write('mv ' + str(changed_fasta_name) + ' ' + str(fasta_file) + '\n')
			batch_script.write('mv ' + str(changed_gff_name) + ' ' + str(gff_file) + '\n')

		elif row[0] == 1: # aka edit is insertion
			
			directory_name = 'edits/' + row[1] #make directory to hold subfiles for each insertion edit
			if os.path.exists(directory_name):
				shutil.rmtree(directory_name)
			os.makedirs(directory_name)

			chromosome = '>' + row[2]
			### file information ###
			insert = row[-1] #sequence
			insert_pos = str(row[3]) # position of insert
			gff = row[2] + '\t' + 'crispr_edit' + '\t' + 'engineered_insert' + '\t' + str(0) + '\t' + str(len(row[5])) + '\t' + '.' + '\t' + '+' + '\t' + '.' + '\t'+ 'ID=insertion_of_' + row[1] + ';Name=' + row[1] + '_insertion'

			### file names ###
			insert_file_name = 'edits/' + row[1] + '/' + row[1] + '_insert.fa'
			gff_file_name = 'edits/' + row[1] + '/' + row[1] + '_insertion.gff'
			insert_pos_file = 'edits/' + row[1] + '/' + row[1] + '_insertion_pos.txt'

			### write files ###
			with open(insert_file_name, 'w') as in_file:
				header = '>'+row[1]+'_insert'+'\n'
				in_file.write(header)
				in_file.write(insert)
			with open(gff_file_name, 'w') as in_file:
				in_file.write('##gff-version 3\n')
				in_file.write(gff)
			with open(insert_pos_file, 'w') as in_file:
				in_file.write(insert_pos)

			batch_script.write("python ~/bin/reform/reform.py --chrom='"+chromosome[1:]+"' --position="+insert_pos+" --in_fasta='"+insert_file_name+"' --in_gff='"+gff_file_name+"' --ref_fasta='"+fasta_file+"' --ref_gff='"+gff_file+"'\n")
			changed_fasta_name = fasta_file.split('.')[0] + '_reformed.fa'
			changed_gff_name = gff_file.split('.')[0] + '_reformed.gff'
			batch_script.write('mv ' + str(changed_fasta_name) + ' ' + str(fasta_file) + '\n')
			batch_script.write('mv ' + str(changed_gff_name) + ' ' + str(gff_file) + '\n')


	batch_script.close()
	print('edits made to fasta and gff file')

get_reform_files(fasta_in_file, gff_in_file, edits)
##############################################################################################

