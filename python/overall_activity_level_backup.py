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

# def matchsubstring(string1, string2): 
# 	print("string1, string2", string1, string2)
# 	for s in string2: 
# 		seqMatch = SequenceMatcher(None,string1, s) 
# 		match = seqMatch.find_longest_match(0, len(string1), 0, len(s))
# 		if (match.size > 1):
# 			res = string1[match.a: match.a + match.size]
# 			print ("Common Substring ::>",string1[match.a: match.a + match.size])
# 		else: 
# 			# print ('No longest common sub-string found') 
# 			res = ""
# 			# print("string1, string2", string1, string2)
# 	return res

def matchsubstring(string1, string2): 
	res = set()
	res_str = ""
	for s in string2: 
		# print("****************** s, string1 ******************", s, string1, string2)
		for i in range(0, len(string1)):
			if string1[i] == s[i]:
				res_str += string1[i]
			else:
				if len(res_str) > 1: 
					res.add(res_str)
				res_str = ""
				break
	return res

# def combine_motions_in_same_room(string1, string2):
# 	def _iter():
# 		for s1, s2 in zip(string1, string2):
# 			if s1 == s2: 
# 				yield s1
# 			else:
# 				return 
# 	return ''.join(_iter())

def get_all_motion_file_names(finpath, house_id):
	file_name_list = []
	room_names = set()
	for filename in glob.glob(os.path.join(finpath, "*.txt")):
		file_name_split = re.split(r"\/", filename)
		file_name = file_name_split[-1][0:-4]
		file_name_list.append(file_name)
	# print("file_name_list", file_name_list)
	for i in range(0, len(file_name_list)): 
		# print("house_id, file_name_list", house_id, file_name_list)
		temp = matchsubstring(file_name_list[i], file_name_list[0:i] + file_name_list[i+1:])
		# temp = repr(temp)
		# temp = eval(temp)
		print("temp list", list(temp))

		if temp == '':	
			room_names.add(file_name_list[i])
		else:
			room_names.add(frozenset(i) for i in temp)
	return room_names, file_name_list

def merge_sort_multiple_motions_in_one_room(house_id, fout_root_path, fout_one_room_path, one_room_name, fin_multiple_motion_path, multiple_motion_names):

	with open(fout_one_room_path + one_room_name + ".txt",'wb') as wfd:
	    for motion_name in multiple_motion_names:
	    	# print("motion_name", motion_name)
	        with open(fin_multiple_motion_path + motion_name + ".txt",'rb') as fd:
	            shutil.copyfileobj(fd, wfd)
	# print("finish merge multiple motion files %s into the room %s" %(multiple_motion_names, one_room_name))

	f = open(fout_one_room_path + one_room_name + ".txt",'rb')
	data = f.readlines()
	data = sorted(data)
	f.close()

	fout_sorted_path = fout_root_path + house_id + "/motion_each_room_sorted/"
	try:
	    os.stat(fout_sorted_path)
	except:
	    os.makedirs(fout_sorted_path)

	with open(fout_sorted_path + one_room_name + ".txt", 'w') as filehandle:
	    for listitem in data:
	        filehandle.write('%s' % listitem)
	# print("finish sort the merged data in room %s from house %s" %(one_room_name, house_id))

def overall_activity_level_each_room(fout_root_path, house_id_list):
	automatically_merge_motion_in_one_room = False
	overall_activity_d = {}
	if automatically_merge_motion_in_one_room:
		for house_id in house_id_list:
			finpath = fout_root_path + house_id + "/motion_imputed/"
			room_names, file_name_list = get_all_motion_file_names(finpath, house_id)
			print("room_names", room_names)
			fout_one_room_path = fout_root_path + house_id + "/motion_each_room_merged/"
			try:
			    os.stat(fout_one_room_path)
			except:
			    os.makedirs(fout_one_room_path)

			for room_name in room_names:
				# print("room_name", room_name)
				multiple_motion_names = [s for s in file_name_list if room_name.lower() in s.lower()]
				merge_sort_multiple_motions_in_one_room(house_id, fout_root_path, fout_one_room_path, room_name, finpath, multiple_motion_names)

		finpath_sort = fout_root_path + house_id + "/motion_each_room_sorted/"
		for house_id in house_id_list:
			for filename in glob.glob(os.path.join(finpath_sort, "*.txt")):
				# print("****************** sorted file name ******************", filename)
				file = open(filename, 'rU')
				data = file.readlines()
				file.close()
				file_name_split = re.split(r"\/", filename)
				file_room_name = file_name_split[-1][0:-4]
				# print("****************** file room name ******************", file_room_name)
				for each_line in data:
					line_split = re.split(r'\t', each_line)
					if file_room_name not in overall_activity_d.keys():
						overall_activity_d[file_room_name] = [[line_split[0], line_split[1], line_split[2].strip()]]
					else: 
						overall_activity_d[file_room_name] += [[line_split[0], line_split[1], line_split[2].strip()]]
	else:
		for house_id in house_id_list:
			finpath = fout_root_path + house_id + "/motion_imputed/"
			for filename in glob.glob(os.path.join(finpath, "*.txt")):
				print("****************** sorted file name ******************", filename)
				file = open(filename, 'rU')
				data = file.readlines()
				file.close()
				file_name_split = re.split(r"\/", filename)
				file_room_name = file_name_split[-1][0:-4]
				print("****************** file room name ******************", file_room_name)
				for each_line in data:
					line_split = re.split(r'\t', each_line)
					if file_room_name not in overall_activity_d.keys():
						overall_activity_d[file_room_name] = [[line_split[0], line_split[1], line_split[2].strip()]]
					else: 
						overall_activity_d[file_room_name] += [[line_split[0], line_split[1], line_split[2].strip()]]					
						
			overall_activity_per_minute = calculate_overall_activity_level(overall_activity_d)
			write_data_to_file_func(overall_activity_per_minute, fout_root_path, house_id, "overall_activity_per_room")



			