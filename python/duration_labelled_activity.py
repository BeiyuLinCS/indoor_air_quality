#!/usr/bin/env python
import re
import os 
import glob
import sys
import datetime
from datetime import datetime, timedelta
from impute_window_door_data import convert_string_to_datetime

def make_dir(path):
	try:
		os.stat(path)
	except:
		os.makedirs(path)

def insert_per_minute_duration(fin_path, house_id_list):
	for house_id in house_id_list:
		finpath = fin_path + house_id + "/duration/"
		foutpath = fin_path + house_id + "/duration_per_minute/"
		make_dir(foutpath)
		for filename in glob.glob(os.path.join(finpath, "*.txt")):
			file = open(filename, 'rU')
			data_readin = file.readlines()
			file.close()
			temp_name_split = re.split(r"\/", filename)
		 	file_name = temp_name_split[-1][0: -4]
			fout = open(foutpath + str(file_name) + ".txt", 'w')
			for i in range(0, len(data_readin)-1):
				curr_line = re.split("\t", data_readin[i])
				next_line = re.split("\t", data_readin[i+1])
				# print("curr_line", curr_line)
				# ('curr_line', ['2015-06-10 18:51:00', '1\n'])
				curr_time = convert_string_to_datetime(curr_line[0])
				curr_time_minutes = curr_time.replace(second=0, microsecond=0)
				end_time_minutes = curr_time_minutes + timedelta(minutes = 1)
				fout.write(data_readin[i])
				next_time = convert_string_to_datetime(next_line[0])
				next_time_minutes = next_time.replace(second=0, microsecond=0)
				diff = int(((next_time_minutes - curr_time_minutes).total_seconds())/60)
				if diff == 1: 
					continue
				else:
					for i in range(0, diff-1):
						time = end_time_minutes + timedelta(minutes = i)
						fout.write(str(time) + "\t" + str(0) + "\n")
			fout.close()


def duration_labelled_activity_func(fin_duration_path, fout_root_path, house_id_list):
	names = []
	temptname = " "
	count = 0
	print"clean and calculate durations of each labelled activity per minute."
	for house_id in house_id_list:
		finpath = fin_duration_path + house_id + "/"
		for filename in glob.glob(os.path.join(finpath, "*")):
		 	data_readin = []
		 	a1 = 0
		 	temp_name_split = re.split(r"\/", filename)
		 	file_name = temp_name_split[-1].split('.')
		 	count = count + 1
		 	file = open(filename, 'rU')
			data_readin = file.readlines()
			data_length = len(data_readin)
			first_line = data_readin[0]
			last_line = data_readin[data_length-1]
			file.close()
			fout_dir = fout_root_path + "/" +  house_id + "/duration/"
			make_dir(fout_dir)
			fout = open(fout_dir + str(file_name[1]) + ".txt", 'w')
			for lines in data_readin[1:]:
				templine = re.split(r"\t", lines)
				line = re.split(r",",templine[0])
				if (line[4].strip() == "NA"):
					continue
				fout.write(str(line[0])+'\t')
				fout.write(str(line[1] + '\n'))
			fout.close()
	


