#!/bin/bash

import os
import argparse


def get_sample_dictionary(trim_out_file):
    sample_dictionary={}
    with open(trim_out_file) as outfile:
		for line in outfile:
			line_split=line.split()
			if len(line_split) >= 1:
				if line_split[0].startswith("TrimmomaticPE:") and line_split[1].startswith("Started"):
					next_line = outfile.next()
					line_data=next_line.split()
					sample="_".join(line_data[0].split("_")[0:2])
					print sample
					for i in range(0,4):
						next_line=outfile.next()
						line_data=next_line.split()
						if line_data[0].startswith("Input"):
							num_reads_input=line_data[3]
							print num_reads_input
							num_reads_surviving=line_data[6]
							print num_reads_surviving
							perc_reads_surviving=line_data[7][1:-2]
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
