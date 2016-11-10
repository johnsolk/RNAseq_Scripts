#!/bin/bash

import os
import argparse


def get_sample_dictionary(trim_out_file):
	sample_dictionary={}
	outfile = open(trim_out_file)
	lines = outfile.readlines()
	outfile.close()
	for line in lines:
		line_split = line.split()
		if line_split[0].startswith("TrimmomaticPE:") and line_split[1].startswith("Started"):
			sample=line_split[4].split("/")[7].split("_")[0]
			print sample
		if line_split[0].startswith("Input"):
			num_reads_input=line_split[3]
			print num_reads_input
			num_reads_surviving=line_split[6]
			print num_reads_surviving
			perc_reads_surviving=line_split[7][1:-2]
			print perc_reads_surviving
			sample_dictionary[sample]=[num_reads_input,num_reads_surviving,perc_reads_surviving]						
    	return sample_dictionary

def trim_table(trim_out_file,trim_table_filename):
    header=["Sample","Input Reads","Surviving Reads","Percent Surviving"]
    sample_dictionary=get_sample_dictionary(trim_out_file)
    print sample_dictionary
    with open(trim_table_filename,"w") as datafile:
        datafile.write("\t".join(header))
        datafile.write("\n")
        for sample in sample_dictionary.keys():
            important_nums=sample_dictionary[sample]
            datafile.write(sample+"\t")
            datafile.write("\t".join(important_nums))
            datafile.write("\n")
    datafile.close()
    print "Trimmomatic stats written:",trim_table_filename

parser = argparse.ArgumentParser(description='Summarize Trimmomatic stats in a table. Usage: python trimmomatic_out_parse.py --trim_out <filename> --summary_out <filename>')
parser.add_argument('-t','--trim_out',help='Name of Trimmomatic output file. Used as input for this program.')
parser.add_argument('-o','--summary_out', help='File summary table.')
args = parser.parse_args()
trim_out_file = args.trim_out
trim_table_filename = args.summary_out

trim_table(trim_out_file,trim_table_filename)
