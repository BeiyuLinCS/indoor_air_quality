################################################################################
####################### Extract the Window/Door Sensors' Data ##################
######## To calcuat the opening area of each window/door 		########
######## write data (local_time, sensor_id, motion_status) into a file #########
################################################################################
#!/usr/bin/env python
import sys
import string
import re
import os 

def process_extracted_data(line, d, all_extracted_data):
	str_split = re.split(r'\|', line)
	### Skip some special notation: ---------+------
	if len(str_split) >= 2:
		local_time = str_split[5].strip() ## local time 
		motion_status = str_split[6].rstrip() ## OPEN/CLOSE;
		sensor_id = str_split[9].rstrip() ## sensor id/name
		motion_status = motion_status.replace(" ","")
		sensor_id = sensor_id.replace(" ","")
		temp = [local_time, sensor_id, motion_status]
		all_extracted_data.append(temp)
		if sensor_id in d.keys():
			d[sensor_id] += [temp]
		else: 
			d[sensor_id] = [temp]	
	return d, all_extracted_data

def extract_sensor_data_func(finpath, sensor_type):
	house_name = re.split(r'/', finpath)
	print("")
	print("#####################")
	print("Start extracting %s sensor data from house: %s"%(sensor_type, house_name[-2]))
	fin = open(finpath, 'rU')
	raw_data = fin.readlines()
	fin.close()
	d = {}
	all_extracted_data = []
	for line in raw_data:
		if (sensor_type == "window_door" and ("OPEN" in line or "CLOSE" in line)): 
			d, all_extracted_data = process_extracted_data(line, d, all_extracted_data)
		if (sensor_type == "temperature" and "Control4-Temperature" in line):
			d, all_extracted_data = process_extracted_data(line, d, all_extracted_data)
		if (sensor_type == "motion" and "Control4-Motion" in line):
			d, all_extracted_data = process_extracted_data(line, d, all_extracted_data)
	print("Finish extracting %s sensor data from house: %s"%(sensor_type, house_name[-2]))
	return d, all_extracted_data
