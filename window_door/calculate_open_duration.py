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

def duration_for_each_minute(curr_time, next_time, curr_time_minutes, next_time_minutes, area_match_value): 
	res = []
	the_next_minute = curr_time_minutes + timedelta(minutes = 1)
	while the_next_minute <= next_time_minutes: 
		duration = round((the_next_minute - curr_time_minutes).total_seconds()/60.0, 3)
		area = round(duration*float(area_match_value), 3)
		res.append([str(curr_time_minutes), duration, area])
		curr_time_minutes = the_next_minute
		the_next_minute = curr_time_minutes + timedelta(minutes = 1)

	duration = round((next_time - next_time_minutes).total_seconds()/60.0, 3)
	area = round(duration*float(area_match_value), 3)
	res.append([str(next_time_minutes), round(duration, 3), area])
	return res

def calculate_open_duration_func(d, area_match_dict):
	area_per_minute = {}
	print("")
	print("start calculate the open area of each window/door.")
	for k, v in d.items():
		if k not in area_match_dict.keys():
			continue
		for i in range(0, len(v)-2, 2):
			curr_time = convert_string_to_datetime(v[i][0])
			next_time = convert_string_to_datetime(v[i+1][0])
			next_next_time = convert_string_to_datetime(v[i+2][0])
			curr_time_minutes = curr_time.replace(second=0, microsecond=0)
			next_time_minutes = next_time.replace(second=0, microsecond=0)
			next_next_time_minutes = next_next_time.replace(second=0, microsecond=0)

			if curr_time_minutes == next_time_minutes: 
				duration = round((next_time - curr_time).total_seconds()/60.0, 3)
				area = round(duration*float(area_match_dict[k]), 3)
				if k not in area_per_minute.keys():	
					area_per_minute[k] = [[str(curr_time_minutes), duration, area]]
				else: 
					area_per_minute[k] += [[str(curr_time_minutes), duration, area]]
			else: 
				res = duration_for_each_minute(curr_time, next_time, curr_time_minutes, next_time_minutes, area_match_dict[k])
				if k not in area_per_minute.keys():
					area_per_minute[k] = res
				else: 
					area_per_minute[k] += res
			temp_time = next_time_minutes
			while (temp_time < next_next_time_minutes - timedelta(minutes = 1)):
				next_time_close = temp_time + timedelta(minutes = 1)
				area_per_minute[k] += [[str(next_time_close), 0, 0]]
				temp_time = next_time_close

	return area_per_minute
