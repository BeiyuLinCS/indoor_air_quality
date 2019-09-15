#!/usr/bin/python

import re
import os
import glob
import datetime
from datetime import datetime, timedelta
from duration_labelled_activity import make_dir
from impute_window_door_data import convert_string_to_datetime

def convert_string_to_date(input_string):
	# '2015/8/25''%Y/%m/%d'
	res = datetime.strptime(input_string, "%Y/%m/%d")
	return res

def write_summer_winter_data(data, start_time_s, end_time_s, start_time_w, end_time_w, fout_s, fout_w):
	for l in data: 
		l_split = re.split(r'\t', l)
		curr_time = convert_string_to_datetime(l_split[0])
		if curr_time < start_time_s: 
			continue
		elif start_time_s <= curr_time <= end_time_s: 
			fout_s.write(l)
		elif  end_time_s < curr_time < start_time_w:
			continue
		elif start_time_w <= curr_time <= end_time_w:
			fout_w.write(l)
		else: 
			continue

def write_only_summer_data(data, start_time_s, end_time_s, fout_s): 
	for l in data: 
		l_split = re.split(r'\t', l)
		curr_time = convert_string_to_datetime(l_split[0])
		if curr_time < start_time_s: 
			continue
		elif start_time_s <= curr_time <= end_time_s: 
			fout_s.write(l)
		else: 
			continue

def data_within_time_period(fout_root_path, f_project_path, house_id_list, time_periods, four_features_dirs):
	acronyms = {"duration_per_minute": "duration_", 
			"wd_open_area": "wd_", 
			"overall_activity_per_room": "activity_level_", 
			"temperature": "temp_"}
	for house_id in house_id_list:
		print("finish extracting data for %s in the given time periods." %house_id)
		for dirs in four_features_dirs: 
			finpath = fout_root_path + house_id + "/" + dirs + "/"
			foutpath_s = f_project_path + "/four_features_summer/" + house_id + "/"
			foutpath_w = f_project_path + "/four_features_winter/" + house_id + "/"
			make_dir(foutpath_s)
			make_dir(foutpath_w)
			curr_acronym = acronyms[dirs]
			for filename in glob.glob(os.path.join(finpath, "*")):
				f = open(filename, 'rU')
				data = f.readlines()
				f.close()
				file_name = list(re.split(r'\/', filename))
				## remove empty strings
				file_name = ' '.join(file_name).split()
				file = file_name[-1]
				time_period = time_periods[house_id]
				if len(time_period) == 1:
					fout_s = open(foutpath_s + curr_acronym + file, 'w')
					start_time_s = convert_string_to_date(time_period[0][0])
					end_time_s = convert_string_to_date(time_period[0][1])
					write_only_summer_data(data, start_time_s, end_time_s, fout_s)
					fout_s.close()
				else: 
					fout_s = open(foutpath_s + curr_acronym + file, 'w')
					fout_w = open(foutpath_w + curr_acronym + file, 'w')
					start_time_s = convert_string_to_date(time_period[0][0])
					end_time_s = convert_string_to_date(time_period[0][1])
					start_time_w = convert_string_to_date(time_period[1][0])
					end_time_w = convert_string_to_date(time_period[1][1])
					write_summer_winter_data(data, start_time_s, end_time_s, start_time_w, end_time_w, fout_s, fout_w)
					fout_s.close()
					fout_w.close()
	print("finish extracting data for all houses in the given time periods.")




