#!/usr/bin/env python
import sys
import time
import string
import datetime
from datetime import datetime, timedelta
from impute_window_door_data import convert_string_to_datetime

def jitter_in_nine_minutes_func(input_list):
	j = 0 
	start_index = 0 
	flag = False
	end_index = len(input_list)-1
	start_time = convert_string_to_datetime(input_list[0][0])
	start_end_index = []
	while j < len(input_list)-2:
		# ('input_list[j]', ['2016-02-29 12:03:06.755074', 'OfficeAWindowBA', 'CLOSE'])
		next_time = convert_string_to_datetime(input_list[j+1][0])
		if (next_time - start_time).total_seconds() >= 540:
			end_index = j 
			if input_list[end_index][2] in ('CLOSE', 'OFF'):  	
				flag = False
				start_end_index.append([start_index, end_index, flag])
				start_index = j + 1
				j += 1
			else: 
				flag = True
				start_end_index.append([start_index, end_index, flag])
				start_index = j + 2
				j += 2
			start_time = convert_string_to_datetime(input_list[start_index][0])
		else:
			j += 1
	updated_input_list = clean_jitter(input_list, start_end_index)
	return updated_input_list

def clean_jitter(input_list, start_end_index):
	new_list = []
	for [s, e, f] in start_end_index:
		new_list.append(input_list[s])
		if f: 
			new_end_time = str(convert_string_to_datetime(input_list[s][0]) + timedelta(seconds=540))
			new_line = [new_end_time, str(input_list[s][1]), 'CLOSE']
			new_list.append(new_line)
		else:
			new_list.append(input_list[e])
	return new_list

def clean_jitter_window_door_func(d):

	for k, v in d.items():
		print("start clean jitter of sensor id %s"% k)
		if v[0][2] in ('CLOSE', 'OFF'):
			del v[0]
		else: 
			d[k] = jitter_in_nine_minutes_func(v)
	return d
