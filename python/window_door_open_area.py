############################################################
############## Window Door Open Area Calculation ###########
############ Beiyu Lin @ Washing State University ##########
#################### beiyu.lin@wsu.edu #####################
############################################################

#!/usr/bin/python
from extract_sensor_data import extract_sensor_data_func
from impute_window_door_data import find_mean_median_duration_func, impute_by_median_mean_func
from write_data_to_file import write_data_to_file_func
from clean_jitter_window_door import clean_jitter_window_door_func
from calculate_open_duration import read_in_area_measure, calculate_open_duration_func

def window_door_open_area_funcs(fin_root_path, fout_root_path, house_id_list):
	for house_id in house_id_list:
		finpath = fin_root_path + house_id + "/" + "raw_no_labelled_data.al"
		area_finpath = fin_root_path + house_id + "/" + "AreaMatch.txt"
		## The default is imputing by median value due to the noises in the data 
		## which may cause large value of mean. 
		flag_impute_by_median = True
		sensor_type = "window_door"
		window_door_d, all_window_door = extract_sensor_data_func(finpath, sensor_type)
		d_mean_duration, d_median_duration, d_missing_data = find_mean_median_duration_func(window_door_d)
		window_door_d = impute_by_median_mean_func(window_door_d, all_window_door, d_missing_data, d_median_duration, d_mean_duration, flag_impute_by_median)
		write_data_to_file_func(window_door_d, fout_root_path, house_id, "wd_imputed")
		window_door_d = clean_jitter_window_door_func(window_door_d)
		write_data_to_file_func(window_door_d, fout_root_path, house_id, "wd_clean_jitter")
		area_match_dict = read_in_area_measure(area_finpath)
		area_per_minute = calculate_open_duration_func(window_door_d, area_match_dict)
		write_data_to_file_func(area_per_minute, fout_root_path, house_id, "wd_open_area")
		