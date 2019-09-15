#!/usr/bin/env python
import csv
import sys
import string
import os 
import glob
import re
import pandas as pd

def pandas_to_csv(f_project_path, summer_or_winter, house_id_list, time_periods):
	for house_id in house_id_list: 
		fin_path = f_project_path + summer_or_winter + "_final_clean/"+ str(house_id) + "/"
		fout_path = "".join([f_project_path, "/summarized_excels/", str(house_id), "_", str(re.split(r'_', summer_or_winter)[-1]), ".csv"])
		files = glob.glob(os.path.join(fin_path, "*"))
		total_files = len(files)
		print("##################")
		print("convert the data from house %s into csv file" %house_id)
		header_list = []
		header_list.append("date_time")
		data_list = []
		first_file_flag = True
		for f in files: 
			f_name = re.split(r'\/', f)[-1][0:-4]

			header_list.append(f_name)
			data = pd.read_csv(f, delimiter="\t", usecols=[0, 1], names = ['date_time', f_name])
			date_time_list = data['date_time'].tolist()
			value_list = data[f_name].tolist()
			# [['2016-03-03 23:57:00', 0],]
	
			if first_file_flag:
				first_file_flag = False
				data_list.append(date_time_list)
				data_list.append(value_list)
			else: 
				data_list.append(value_list)
		final_list_for_each_home =[]
		final_list_for_each_home.append(header_list)
		final_list_for_each_home += list(zip(*data_list))
		my_df = pd.DataFrame(final_list_for_each_home)
		my_df.to_csv(fout_path, index=False, header=False)
