############################################################
################## Impute the sensor data ##################
############################################################
#!/usr/bin/env python
import sys
import time
import string
import calendar
from decimal import *
import csv
import pylab
import pytz
import re
import os 
import glob
import errno
from dateutil import tz
import numpy as np
import datetime
from pytz import timezone
from datetime import datetime, timedelta
import extract_window_door_data as wd

def convert_string_to_datetime(input_string):
	try:
		res = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
	except: 
		res = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S.%f")
	return res

def find_mean_median_duration_func(d):
	d_missing_data = {}
	durations_of_start_end = [] ## on_off or open_close
	durations_of_end_start = [] ## off_on or close_open
	d_mean_duration = {}
	d_median_duration = {}
	for k in d.keys():
		print("Start imputing the data with sensor id %s" %k)
		for i in range(0, len(d[k])-1):
			curr_datetime = convert_string_to_datetime(d[k][i][0]) 
			next_datetime = convert_string_to_datetime(d[k][i+1][0])
			curr_status = d[k][i][2]
			next_status = d[k][i+1][2]
			duration = (next_datetime - curr_datetime).total_seconds()
			if curr_status == next_status:
				curr_date_missing_data = d[k][i]
				if k not in d_missing_data.keys():
					d_missing_data[k] = [[i, i+1, duration]]
				else:
					d_missing_data[k] += [[i, i+1, duration]]
			else: 
				if curr_status in ('ON', 'OPEN') and next_status in ('OFF', 'CLOSE'): 
					durations_of_start_end.append(duration)
				else:
					durations_of_end_start.append(duration)
		d_mean_duration[k] = [np.mean(durations_of_start_end), np.mean(durations_of_end_start)]
		d_median_duration[k] = [np.median(durations_of_start_end), np.median(durations_of_end_start)]
	return d_mean_duration, d_median_duration, d_missing_data

def look_for_next_event_time(all_window_door, curr_event): 
	## all_window_door = [[local_time, sensor_id, motion_status], ...]
	res = ""
	event_split = curr_event
	for i in range(0, len(all_window_door)-1): 
		if str(all_window_door[i][0]) == str(event_split[0]):
			res =  all_window_door[i+1][0]
			break			
	return res

def impute_by_median_mean_func(d, all_window_door, d_missing_data, d_median_duration, d_mean_duration, flag_impute_by_median): 
	if flag_impute_by_median:
		impute_duration = d_median_duration
	else: 
		impute_duration = d_mean_duration
	for k, v in d_missing_data.items():
		i = 0 
		l = [0,0, 0]
		for i in range(0, len(v)):
			curr_local_time = convert_string_to_datetime(cd[k][v[i][0]])
			next_local_time = convert_string_to_datetime(d[k][v[i][1]])
			temp_list = d[k][v[i][0]]
			if temp_list[2] == "OPEN":
				new_motion_status = "CLOSE"
				if float(v[i][2]) >= impute_duration[k][0]:
					new_local_time = str(curr_local_time + timedelta(seconds=impute_duration[k][0]))
				else: 
					new_local_time = look_for_next_event_time(all_window_door, d[k][v[i][0]])
			elif temp_list[2] == "CLOSE":
				new_motion_status = "OPEN" 
				if float(v[i][2]) >= impute_duration[k][1]:
					new_local_time = str(curr_local_time + timedelta(seconds=impute_duration[k][1]))
				else: 
					new_local_time = look_for_next_event_time(all_window_door, d[k][v[i][0]])
			insert_new_data = [str(new_local_time), k, new_motion_status]
			d[k].append(insert_new_data)
	for k, v in d.items():
		d[k] = sorted(d[k], key = lambda x: x[0])
	print("Finish imputing data")
	return d


