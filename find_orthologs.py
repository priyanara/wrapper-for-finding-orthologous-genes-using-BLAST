#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

def main():

	    
	parser=argparse.ArgumentParser(description="The goal is to get the reciprocal blast hits for two species")
	parser.add_argument("-i1","--input1",help="Enter the first input file")
	parser.add_argument("-i2","--input2",help="Enter the second input file")
	parser.add_argument("-o","--output",help="Enter the output file")
	parser.add_argument("-t","--type",help="Sequence type -n/p")
	args=parser.parse_args()
	print(args)
 
	file_one=args.input1
	file_two=args.input2
	output_file=args.output
	input_sequence_type=args.type

	
	
	command_nuc_blast1=["makeblastdb", "-in", file_one, "-dbtype", "nucl", "-out", "tmp/output1"]
	command_nuc_blast2=["makeblastdb", "-in", file_two, "-dbtype", "nucl", "-out", "tmp/output2"]
	command_prot_blast1=["makeblastdb", "-in",file_one, "-dbtype", "prot", "-out", "tmp/output1"]
	command_prot_blast2=["makeblastdb", "-in",file_two,"-dbtype", "prot", "-out","tmp/output2"]

	 
	final1_nuc_command=["blastn", "-query",file_one,"-db","tmp/output2","-outfmt","6","-max_target_seqs", "1","-max_hsps", "1","-out" ,"seqA.txt"]
	final2_nuc_command=["blastn", "-query",file_two,"-db","tmp/output1","-outfmt","6","-max_target_seqs", "1","-max_hsps", "1","-out" ,"seqB.txt"]
#-db file_two figures out the database for the second file

	final1_prot_command=["blastp", "-query",file_one,"-db","tmp","-outfmt","6","-max_target_seqs", "1","-max_hsps", "1","-out" ,"seqA.txt"]
	final2_prot_command=["blastp", "-query",file_two,"-db","tmp","-outfmt","6","-max_target_seqs", "1","-max_hsps", "1","-out", "seqB.txt"]

	
	if (input_sequence_type == "n"):
		subprocess.call(command_nuc_blast1)
		subprocess.call(command_nuc_blast2)
		subprocess.check_output(final1_nuc_command)
		subprocess.check_output(final2_nuc_command)

	elif (input_sequence_type == "p"):
		subprocess.call(command_prot_blast1)
		subprocess.call(command_prot_blast2)
		subprocess.check_output(final1_prot_command)
		subprocess.check_output(final2_prot_command)

	else:
		print("Sequence type not specified")
		sys.exit()

	output_list = get_reciprocal_hits(file_one, file_two, input_sequence_type)
	with open(output_file, 'w') as output_fh:
		for ortholog_pair in output_list:
			output_fh.write(ortholog_pair+'\n')

def get_reciprocal_hits(file_one, file_two, input_sequence_type):

	blast_hits1='seqA.txt'
	blast_hits2='seqB.txt'

	seqA={}
	seqB={}

	with open(blast_hits1,'r') as f:

		for lineA in f:
			lineA=lineA.split('\t')
			(key1,val1)=lineA[0],lineA[1]
			seqA[key1]=val1


	with open(blast_hits2,'r') as g:

		for lineB in g:
			lineB=lineB.split('\t')
			(key2,val2)=lineB[0],lineB[1]
			seqB[key2]=val2
	
	output_list=[]

	for key,value in seqB.items():
		if key==seqA[value]:
			output_list.append(key+'\t'+value)
	return output_list


if __name__ == "__main__":
	main()

