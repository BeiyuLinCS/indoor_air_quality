import re
import datetime
from datetime import datetime, timedelta
from impute_window_door_data import convert_string_to_datetime

def read_in_area_measure(area_finpath):
	area_match_dict = {}
	f = open(area_finpath, 'rU')
	lines = f.readlines()
	f.close()
	for l in lines:
		l_split = re.split(r'\t', l)
		area_match_dict[l_split[0]] = l_split[1].strip()
	return area_match_dict

def datetime_range(date1, date2):
    for n in range(int ((date2 - date1).total_seconds()/60)):
        yield date1 + timedelta(minutes=n)

def insert_each_minute_func(start_dt, end_dt, area):
	# start_dt = convert_string_to_date("2015-12-20 00:00:00")
	# end_dt = convert_string_to_date("2016-1-11 10:00:00")
	res_full_minnute = []
	for dt in datetime_range(start_dt, end_dt):
		res_full_minnute.append([dt.strftime("%Y-%m-%d %H:%M:%S"), area])
	return res_full_minnute

def duration_for_each_minute(curr_time, next_time, curr_time_minutes, next_time_minutes, area_match_value, area_flag): 
	res_list = []
	## insert the starting minute
	the_next_minute = curr_time_minutes + timedelta(minutes = 1)
	duration = round((the_next_minute - curr_time).total_seconds()/60.0, 3)
	if area_flag: 
		area = round(duration*float(area_match_value), 3)
	else: 
		area = 0 
	res_list.append([str(curr_time_minutes), area])
	## insert the difference between starting and end minutes. 
	if area_flag: 
		area = round(1*float(area_match_value), 3)
	else:
		area = 0 
	res_list += insert_each_minute_func(the_next_minute, next_time_minutes, area)
	return res_list

def calculate_open_duration_func(d, area_match_dict):
	area_per_minute = {}
	print("")
	print("start calculate the open area of each window/door.")
	for k, v in d.items():
		if k not in area_match_dict.keys():
			continue
		# print("v", v)
		# [['2015-06-10 18:54:21.390994', 'DiningRoomAWindowAB', 'OPEN'],...]
		continus_minute = False
		area_flag = False
		for i in range(0, len(v)-1, 1):
			curr_time = convert_string_to_datetime(v[i][0])
			next_time = convert_string_to_datetime(v[i+1][0])
			curr_time_minutes = curr_time.replace(second=0, microsecond=0)
			next_time_minutes = next_time.replace(second=0, microsecond=0)
			if v[i][2] == "OPEN": 
				area_flag = True
			else: 
				area_flag = False

			if curr_time_minutes == next_time_minutes: 
				continus_minute = True
				duration = round((next_time - curr_time).total_seconds()/60.0, 3)
				if area_flag: 
					area = round(duration*float(area_match_dict[k]), 3)
				else: 
					area = 0
				if k not in area_per_minute.keys():	
					area_per_minute[k] = [[str(curr_time_minutes), area]]
				else: 
					area_per_minute[k] += [[str(curr_time_minutes), area]]
				continue
			else: 
				if continus_minute:
					curr_time = curr_time_minutes + timedelta(minutes = 1)
					curr_time_minutes = curr_time_minutes + timedelta(minutes = 1)
				res = duration_for_each_minute(curr_time, next_time, curr_time_minutes, next_time_minutes, area_match_dict[k], area_flag)
				continus_minute = False
				if k not in area_per_minute.keys():
					area_per_minute[k] = res
				else: 
					area_per_minute[k] += res
	return area_per_minute
