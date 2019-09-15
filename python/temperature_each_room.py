#!/usr/bin/python
import datetime
from datetime import datetime, timedelta
from extract_sensor_data import extract_sensor_data_func
from write_data_to_file import write_data_to_file_func
from impute_window_door_data import convert_string_to_datetime
from calculate_open_duration import datetime_range, insert_each_minute_func

def temp_for_each_minute(curr_time, curr_temperature, next_temperature, next_time, curr_time_minutes, next_time_minutes): 
	res = []
	the_next_minute = curr_time_minutes + timedelta(minutes = 1)
	res.append([str(curr_time_minutes), curr_temperature])

	while the_next_minute < next_time_minutes: 
		temperature = curr_temperature
		res.append([str(curr_time_minutes), curr_temperature])
		curr_time_minutes = the_next_minute
		the_next_minute = curr_time_minutes + timedelta(minutes = 1)

	res.append([str(next_time_minutes), next_temperature])
	return res

def temp_among_time_difference(curr_time, curr_temperature, next_time, curr_time_minutes, next_time_minutes): 
	res_list = []
	## insert the starting minute
	the_next_minute = curr_time_minutes + timedelta(minutes = 1)
	duration = round((the_next_minute - curr_time).total_seconds()/60.0, 3)
	res_list.append([str(curr_time_minutes), curr_temperature])
	## insert the difference between starting and end minutes. 
	res_list += insert_each_minute_func(the_next_minute, next_time_minutes, curr_temperature)
	return res_list

def temp_per_minute(d):
	temp_per_minute = {}
	for k, v in d.items():
		continus_minute = False
		area_flag = False
		for i in range(0, len(v)-1, 1):
			# 2015-06-10 22:28:04.784430	BathroomATemperature	23.0
			curr_time = convert_string_to_datetime(v[i][0])
			curr_time_minutes = curr_time.replace(second=0, microsecond=0)
			curr_temperature = float(v[i][2])
			next_time = convert_string_to_datetime(v[i+1][0])
			next_time_minutes = next_time.replace(second=0, microsecond=0)
			next_temperature = float(v[i+1][2])

			if curr_time_minutes == next_time_minutes: 
				continus_minute = True
				duration = round((next_time - curr_time).total_seconds()/60.0, 3)
				if k not in temp_per_minute.keys():	
					temp_per_minute[k] = [[str(curr_time_minutes), (curr_temperature + next_temperature)/2.0]]
				else: 
					temp_per_minute[k] += [[str(curr_time_minutes), curr_temperature]]
			else: 
				if continus_minute:
					curr_time = curr_time_minutes + timedelta(minutes = 1)
					curr_time_minutes = curr_time_minutes + timedelta(minutes = 1)
				res = temp_among_time_difference(curr_time, curr_temperature, next_time, curr_time_minutes, next_time_minutes)
				continus_minute = False
				if k not in temp_per_minute.keys():	
					temp_per_minute[k] = res
				else: 
					temp_per_minute[k] += res
	return temp_per_minute

def temp_func(fin_root_path, fout_root_path, house_id_list):
	for house_id in house_id_list:
		finpath = fin_root_path + house_id + "/" + "raw_no_labelled_data.al"
		sensor_type = "temperature"
		d, all_extracted_data = extract_sensor_data_func(finpath, sensor_type)
		d = temp_per_minute(d)	
		write_data_to_file_func(d, fout_root_path, house_id, sensor_type)
		

