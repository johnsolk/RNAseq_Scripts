# combines files from multiple lanes, same sample
# R1 and R2 separately

import os
import os.path
import subprocess
from subprocess import Popen,PIPE
import clusterfunc

def combine_files(merge_dictionary,basedir,combine_dir):
	for sample in merge_dictionary:
		R1 = []
		R2 = []
		for i in merge_dictionary[sample]: 
			file_fields = i.split("/")
			fields = file_fields[5].split("_")
			if fields[3] == "R1":
				R1.append(i)
			elif fields[3] == "R2":
				R2.append(i)
			else:
				print "Wrong field.",fields		 
		print sample,"R1 files:",R1
		print sample,"R2 files:",R2
		fields_read = R1[0].split("/")[5].split("_")
		sample = fields_read[0]
		extension = fields_read[4][3:]
		newfilename_R1=combine_dir+sample+"_R1"+extension
		newfilename_R2=combine_dir+sample+"_R2"+extension
		files_string_R1=" ".join(R1)
		files_string_R2=" ".join(R2)
		combine_string_R1="zcat "+files_string_R1+" > "+newfilename_R1
		combine_string_R2="zcat "+files_string_R2+" > "+newfilename_R2
		print combine_string_R1
		print combine_string_R2
		#s=subprocess.Popen(combine_string,shell=True)
		#s.wait()
		combine_command=[combine_string_R1,combine_string_R2]
		module_load_list=[""]
		process_name="combine"
		clusterfunc.sbatch_file(basedir,process_name,module_load_list,sample,combine_command)


def find_files_to_merge(fileslist,basedir):
	filestomergelist={}
        for filename in fileslist:
		if filename != "sbatch_files":
			fields = filename.split("_")
			sample = fields[0]
			if sample in filestomergelist:
				filestomergelist[sample].append(basedir+filename)
			else:
				filestomergelist[sample] = [basedir+filename]
	return filestomergelist

basedir="/home/ywdong/Data/Project_AWYD_alllanes/"
#lanes = [basedir+"Project_AWYD_L1_MKS001/",basedir+"Project_AWYD_L2_MKS001/",basedir+"Project_AWYD_L3_MKS001/",basedir+"Project_AWYD_L4_MKS001/"]
listoffiles=os.listdir(basedir)
#print listoffiles
merge_dictionary=find_files_to_merge(listoffiles,basedir)

for sample in merge_dictionary:
	print sample 
	for i in merge_dictionary[sample]:
		print i

combine_dir="/home/ywdong/Data/combined/"
combine_files(merge_dictionary,basedir,combine_dir)
