#!/usr/bin/env python
import sys
import os 
import errno
import pickle

def write_data_to_file_func(d, foutpath, house_id, data_process):
	for k in d.keys():
		fout_new_directory_path = foutpath + house_id +"/" + data_process +"/"
		fout_new_directory = os.path.dirname(fout_new_directory_path)
		try:
		    os.stat(fout_new_directory)
		except:
		    os.makedirs(fout_new_directory)
		fout = open(fout_new_directory + "/" + k + ".txt", 'wb')
		for i in range(0, len(d[k])):
			# print("d[k][i]", d[k])
			# 	print("k,v", k, v)
			# 	'BedroomBWindow', [['2015-06-19 14:43:00', 0.020105316666666664, 0.015],
			for j in range(0, len(d[k][i])):
				if j != len(d[k][i]) - 1: 
					fout.write(str(d[k][i][j]) + "\t")
				else: 
					fout.write(str(d[k][i][j]) + "\n")
		fout.close()
	print("Finish writing the %s data into files" %data_process)
