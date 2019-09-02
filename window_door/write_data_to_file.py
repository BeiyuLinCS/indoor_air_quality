#!/usr/bin/env python
import sys
import os 
import errno
import pickle

def write_data_to_file_func(d, foutpath, house_id):
	for k in d.keys():
		fout_new_directory_path = foutpath + house_id +"/"
		fout_new_directory = os.path.dirname(fout_new_directory_path)
		try:
		    os.stat(fout_new_directory)
		except:
		    os.makedirs(fout_new_directory)
		fout = open(fout_new_directory + "/" + k + ".txt", 'wb')
		for i in range(0, len(d[k])):
			fout.write(d[k][i][0] + "\t")
			fout.write(d[k][i][1] + "\t")
			fout.write(d[k][i][2] + "\n")
		fout.close()
	print("Finish writing the imputed data into files")




