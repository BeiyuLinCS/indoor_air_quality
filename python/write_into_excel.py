#!/usr/bin/env python
import sys
import os
import time
import string
import calendar
from decimal import *
import numpy
import numpy as np
import csv
import pylab
import calendar
import datetime
from datetime import datetime
from pytz import timezone
import pytz
import re
import os 
import errno
import glob
import math
from dateutil import tz
from duration_labelled_activity import make_dir

# finpath = "/Volumes/Seagate Backup Plus Drive/IAQ_Minute_Data/Atmo9S_Minute/ForCategoryIAQPeriod_Minute_PST/"
# foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ_Minute_Data/Atmo9S_Minute/"
#freadNames1 = "/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/Atmo1.txt"
#freadNames2 = "/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/Atmo2.txt"

#freadNames = freadNames1
#dicName = {}

def write_four_features_into_excel(f_project_path, summer_or_winter, house_id_list):
	for house_id in house_id_list: 
		fin_path = f_project_path + summer_or_winter + "/" + house_id + "/"
		summer_or_winter_string = re.split(r'_', summer_or_winter)
		fout_path_dir = f_project_path + "/summarized_excels/"
		make_dir(fout_path_dir)
		fout_path = fout_path_dir + str(house_id) + "_" + str(summer_or_winter_string[-1]) + ".csv"
		f_out = open(fout_path, 'wa')

		filenames = glob.glob(os.path.join(fin_path, "*.txt"))
		writer = csv.writer(f_out, delimiter=',')
		row = ['Time']
		files = {}

		## Make the header ####
		for filename in filenames:
			# Open all the files for use later
			files[filename] = open(filename, 'rU')
			# Get the actual filename
			tempNameSplit = re.split(r"\/", filename)
			#print tempNameSplit
			#print tempNameSplit[-1]
			##'IMedBathroomAArea.txt'
			# Remove the first 4 characters ('Imed') and last 4 characters ('.txt')
			row.append(tempNameSplit[-1][0:-4])

		# Write the header
		writer.writerow(row)

		while (1):
			row = []
			for filename in filenames:
				# Read the next line from the file
				if os.stat(filename).st_size == 0:
					continue

				line = files[filename].readline().rstrip('\n')
				# If the end of file was reached, break
				if not line or line == '\n': break
				# Split the line by the tab character
				tempLineSplit = re.split(r'\t', line)
				# If row is empty, set the first element to be the time
				if not row: row = [tempLineSplit[0]]
				#print tempLineSplit, tempLineSplit[0], tempLineSplit[1]
				# Append the data from each file into row
				row.append(tempLineSplit[1])
			# If the end of file was reached, break
			if not row: break
			else: writer.writerow(row)

		# Close all the files
		f_out.close()
		for filename in filenames:
			files[filename].close()
