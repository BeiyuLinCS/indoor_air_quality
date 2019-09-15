#!/usr/bin/env python
import sys
import string
import re
import os 
import errno
import glob
import datetime
from datetime import datetime, timedelta
from duration_labelled_activity import make_dir
from insert_each_minute import convert_string_to_date

def convert_string_to_only_date(input_string):
	res = datetime.strptime(input_string, "%Y/%m/%d")
	return res

def write_missing_start_end_time(f_out, minute_start, minute_end, value, start_flag): 
	if start_flag: 
		minute_start = minute_start + timedelta(minutes = 1)
	while minute_start <= minute_end: 
		f_out.write(str(minute_start) + "\t" + value + "\n") 
		minute_start = minute_start + timedelta(minutes = 1)
	# if start_flag: 
	# 	f_out.write(str(minute_start) + "\t" + value + "\n") 

def find_time_period(winter_or_summer_name, time_period): 
	if winter_or_summer_name == "summer":
		## time_period[0]
		time_period_start = time_period[0][0]
		time_period_end = time_period[0][1]
	else: 
		## time_period[1]
		time_period_start = time_period[1][0]
		time_period_end = time_period[1][1]
	return convert_string_to_only_date(time_period_start), convert_string_to_only_date(time_period_end)

def process_readin_data(f_out, file_name, data_readin, data_length, time_periods, house_id, winter_or_summer_name):
	time_period = time_periods[house_id]
	time_period_start, time_period_end = find_time_period(winter_or_summer_name, time_period)
	start_line = re.split(r'\t', data_readin[0])
	start_time = convert_string_to_date(start_line[0])
	end_line = re.split(r'\t', data_readin[-1])
	end_time = convert_string_to_date(end_line[0])

	start_flag = False
	if start_time > time_period_start: 
		value = 'na'
		start_flag = True
		write_missing_start_end_time(f_out, time_period_start, start_time, value, start_flag)

	for i in range(1, data_length-1): 
		curr_line = re.split(r'\t', data_readin[i])
		next_line = re.split(r'\t', data_readin[i+1])
		curr_time = convert_string_to_date(curr_line[0])
		next_time = convert_string_to_date(next_line[0])
		if (next_time - curr_time).total_seconds()/60.0 == 0: 
			continue
		f_out.write(data_readin[i])
	
	if end_time == time_period_end: 
		f_out.write(data_readin[i+1])
	if end_time < time_period_end: 
		value = 'na'
		start_flag = False
		write_missing_start_end_time(f_out, end_time, time_period_end, value, start_flag)

def final_clean_func(f_project_path, summer_or_winter, house_id_list, time_periods):
	for house_id in house_id_list: 
		print("processing house_id %s" % house_id)
		fin_path = f_project_path + summer_or_winter + "/" + house_id + "/"
		summer_or_winter_string = re.split(r'_', summer_or_winter)
		fout_path_dir = f_project_path + summer_or_winter + "_final_clean/"+ str(house_id) + "/"
		make_dir(fout_path_dir)

		for filename in glob.glob(os.path.join(fin_path, "*")):
			tempNameSplit = re.split(r"\/", filename)
			file_name = tempNameSplit[-1]
			winter_or_summer_name = re.split(r'_', summer_or_winter)
			winter_or_summer_name = winter_or_summer_name[-1]
			fout_path = fout_path_dir + file_name 
			file = open(filename, 'rU')
			data_readin = file.readlines()
			data_length = len(data_readin)
			file.close()
			if data_readin == []:
				print("the file is empty", filename)
				continue
			f_out = open(fout_path, 'w')
			process_readin_data(f_out, file_name, data_readin, data_length, time_periods, house_id, winter_or_summer_name)
