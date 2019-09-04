############################################################
################## Indoor Air Quality Project ##############
############ Beiyu Lin @ Washing State University ##########
#################### beiyu.lin@wsu.edu #####################
############################################################

#!/usr/bin/python
from extract_window_door_data import extract_door_window_data_func
from impute_window_door_data import find_mean_median_duration_func, impute_by_median_mean_func
from write_data_to_file import write_data_to_file_func
from clean_jitter_window_door import clean_jitter_window_door_func

if __name__ == '__main__':

	finpath = "/Volumes/Seagate Backup Plus Drive/atmo/newAtmo1Atmo2Data/atmo1.dat"
	foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ_Minute_Data/all_houses/"
	house_id = "atmo1"

	## The default is imputing by median value due to the noises in the data 
	## which may cause large value of mean. 
	flag_impute_by_median = True
	d, all_window_door = extract_door_window_data_func(finpath)
	d_mean_duration, d_median_duration, d_missing_data = find_mean_median_duration_func(d)
	d = impute_by_median_mean_func(d, all_window_door, d_missing_data, d_median_duration, d_mean_duration, flag_impute_by_median)
	write_data_to_file_func(d, foutpath, house_id, "imputed")
	d = clean_jitter_window_door_func(d)
	write_data_to_file_func(d, foutpath, house_id, "clean_jitter")

	






	