#!/usr/bin/env python
import sys
import string
import re
import os 
import errno
import glob
import datetime
from datetime import datetime, timedelta
from duration_labelled_activity import make_dir
from insert_each_minute import convert_string_to_date


def calculate_length_fucs(f_project_path, summer_or_winter, house_id_list, time_periods):
	for house_id in house_id_list: 
		# print("processing house_id %s" % house_id)
		fin_path = f_project_path + summer_or_winter + "_final_clean/" + "/" + house_id + "/"
		length_house = {}

		for filename in glob.glob(os.path.join(fin_path, "*")):
			tempNameSplit = re.split(r"\/", filename)
			file_name = tempNameSplit[-1][0:-4]

			file = open(filename, 'rU')
			data_readin = file.readlines()
			data_length = len(data_readin)
			file.close()
			if data_readin == []:
				continue
			if data_length not in length_house.keys():
				length_house[data_length] = [[file_name]]
			else: 
				length_house[data_length] += [[file_name]]
				
		if len(length_house.keys()) > 1: 
			print("######################")
			print("house_id", house_id)
			for k, v in length_house.items():
				print("key is ", k)
				print("value is ", v)
				print("")
