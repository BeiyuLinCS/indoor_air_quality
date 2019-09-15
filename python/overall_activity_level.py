#!/usr/bin/python
import sys
import datetime
import glob
import os
import re
import shutil
from difflib import SequenceMatcher 
from datetime import datetime, timedelta
from extract_sensor_data import extract_sensor_data_func
from impute_window_door_data import convert_string_to_datetime, find_mean_median_duration_func, impute_by_median_mean_func
from write_data_to_file import write_data_to_file_func

def insert_per_minute(curr_time_minutes, end_time_minutes, overall_activity_per_minute, k): 
	diff = int(((curr_time_minutes - end_time_minutes).total_seconds())/60)
	for i in range(0, diff): 
		time = end_time_minutes + timedelta(minutes = i)
		if k not in overall_activity_per_minute.keys(): 
			overall_activity_per_minute[k] = [[str(time), 0]]
		else: 
			overall_activity_per_minute[k] += [[str(time), 0]]
	return overall_activity_per_minute

def calculate_overall_activity_level(d):
	overall_activity_per_minute = {}
	print("start calculating the overall activity level.")
	for k, v in d.items():
		# print ("v", v)
		start_time = convert_string_to_datetime(v[0][0])
		start_time_minutes = start_time.replace(second=0, microsecond=0)
		end_time_minutes = start_time_minutes + timedelta(minutes = 1)
		i = 0
		count = 0
		while ( i < len(v)):
			curr_time = convert_string_to_datetime(v[i][0])
			curr_time_minutes = curr_time.replace(second=0, microsecond=0)
			if start_time_minutes <= curr_time_minutes < end_time_minutes:
				# print("curr_time_minutes in between")
				# print("v[i]", v[i])
				if v[i][2] == 'ON': 
					count += 1
			elif curr_time >= end_time_minutes: 
				if k not in overall_activity_per_minute.keys():	
					overall_activity_per_minute[k] = [[str(start_time_minutes), count]]
				else: 
					overall_activity_per_minute[k] += [[str(start_time_minutes), count]]
				count = 0

				if curr_time_minutes == end_time_minutes:
					start_time_minutes = end_time_minutes
				elif curr_time_minutes > end_time_minutes:
					overall_activity_per_minute = insert_per_minute(curr_time_minutes, end_time_minutes, overall_activity_per_minute, k)
					start_time_minutes = curr_time_minutes
				end_time_minutes = start_time_minutes + timedelta(minutes = 1)
				if v[i][2] == 'ON': 
					count += 1
			else: 
				print("line 51 insert per minute problem")
				print("v[i][0]", v[i][0])
				print("start time", start_time_minutes)
				count = 0
			i += 1
	return overall_activity_per_minute


def extract_impute_motion_data(fin_root_path, fout_root_path, house_id_list):
	for house_id in house_id_list:
		finpath = fin_root_path + house_id + "/" + "raw_no_labelled_data.al"
		sensor_type = "motion"
		flag_impute_by_median = True
		motion_d, all_extracted_data = extract_sensor_data_func(finpath, sensor_type)

		d_mean_duration, d_median_duration, d_missing_data = find_mean_median_duration_func(motion_d)
		motion_d = impute_by_median_mean_func(motion_d, all_extracted_data, d_missing_data, d_median_duration, d_mean_duration, flag_impute_by_median)
		write_data_to_file_func(motion_d, fout_root_path, house_id, "motion_imputed")

def overall_activity_level_each_room(fout_root_path, house_id_list):
	overall_activity_d = {}
	for house_id in house_id_list:
		finpath = fout_root_path + house_id + "/motion_imputed/"
		for filename in glob.glob(os.path.join(finpath, "*.txt")):
			file = open(filename, 'rU')
			data = file.readlines()
			file.close()
			file_name_split = re.split(r"\/", filename)
			file_room_name = file_name_split[-1][0:-4]
			for each_line in data:
				line_split = re.split(r'\t', each_line)
				if file_room_name not in overall_activity_d.keys():
					overall_activity_d[file_room_name] = [[line_split[0], line_split[1], line_split[2].strip()]]
				else: 
					overall_activity_d[file_room_name] += [[line_split[0], line_split[1], line_split[2].strip()]]					

		overall_activity_per_minute = calculate_overall_activity_level(overall_activity_d)
		write_data_to_file_func(overall_activity_per_minute, fout_root_path, house_id, "overall_activity_per_room")
	print("finish calculating overall activity levels and writing them into files.")

		