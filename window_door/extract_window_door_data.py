################################################################################
####################### Extract the Window/Door Sensors' Data ##################
######## To calcuat the opening area of each window/door 				########
######## write data (local_time, sensor_id, motion_status) into a file #########
################################################################################
#!/usr/bin/env python
import sys
import string
import re
import os 

def extract_door_window_data_func(finpath):
	house_name = re.split(r'/', finpath)
	print("Start extracting window and door sensor data from house: %s"%house_name[-1])
	fin = open(finpath, 'rU')
	raw_data = fin.readlines()
	fin.close()
	d = {}
	all_window_door = []
	for line in raw_data:
		if (("OPEN" in line) or ("CLOSE" in line)):  ## extract the WINDOW/DOOR data 
		#if ("Control4-Temperature" in line):  ## extract the temp data 
			str_split = re.split(r'\|', line)
			### Skip some special notation: ---------+------
			if len(str_split) < 2:
				continue
			local_time = str_split[5].strip() ## local time 
			motion_status = str_split[6].rstrip() ## OPEN/CLOSE;
			sensor_id = str_split[9].rstrip() ## sensor name
			motion_status = motion_status.replace(" ","")
			sensor_id = sensor_id.replace(" ","")
			temp = [local_time, sensor_id, motion_status]
			all_window_door.append(temp)
			# temp = ",".join(temp)
			if sensor_id in d.keys():
				d[sensor_id] += [temp]
			else: 
				d[sensor_id] = [temp]

	print("Finish extracting window and door sensor data for this house.")
	return d, all_window_door
