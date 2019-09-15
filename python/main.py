############################################################
################## Indoor Air Quality Project ##############
############ Beiyu Lin @ Washing State University ##########
#################### beiyu.lin@wsu.edu #####################
############################################################
#!/usr/bin/python
from window_door_open_area import window_door_open_area_funcs
from temperature_each_room import temp_func
from overall_activity_level import extract_impute_motion_data, overall_activity_level_each_room
from duration_labelled_activity import duration_labelled_activity_func, insert_per_minute_duration
from extract_data_in_time_period import data_within_time_period
from final_clean import final_clean_func
from use_pandas_to_csv import pandas_to_csv

if __name__ == '__main__':

	time_periods = { "atmo1": [["2015/8/25","2015/9/2"], ["2016/2/27", "2016/3/4"]], 
				"atmo2": [["2015/7/23", "2015/8/20"], ["2016/3/12", "2016/3/28"]],
				"atmo4": [["2016/3/31", "2016/4/11"]],
				"atmo5": [["2016/8/19", "2016/8/26"]],
				"atmo6": [["2016/9/13", "2016/9/19"], ["2017/1/31", "2017/2/7"]],
				"atmo7": [["2016/9/20", "2016/10/3"], ["2017/2/7", "2017/2/14"]],
				"atmo8": [["2018/2/5", "2018/2/19"], ["2018/7/31", "2018/8/9"]],
				"atmo9": [["2017/9/8", "2017/9/15"], ["2018/1/19", "2018/1/26"]],
				"atmo10": [["2017/9/19", "2017/9/27"], ["2018/1/27", "2018/2/5"]]}

	four_features_dirs = ["duration_per_minute", 
				"wd_open_area", 
				"overall_activity_per_room", 
				"temperature"]
	
	house_id_list = ["atmo1", 
				"atmo2", 
				"atmo4", 
				"atmo5", 
				"atmo6", 
				"atmo7", 
				"atmo8", 
				"atmo9", 
				"atmo10"]

	f_project_path = "/Users/BeiyuLin/Desktop/indoor_air_quality/" 
	fin_root_path = "/Users/BeiyuLin/Desktop/indoor_air_quality/data/"
	fout_root_path = "/Users/BeiyuLin/Desktop/indoor_air_quality/processed_data/"	
	fin_duration_path = "/Users/BeiyuLin/Desktop/indoor_air_quality/duration/iaq_data_sep_19/duration_minute/"

	window_door_open_area_funcs(fin_root_path, fout_root_path, house_id_list)
	temp_func(fin_root_path, fout_root_path, house_id_list)
	extract_impute_motion_data(fin_root_path, fout_root_path, house_id_list)
	overall_activity_level_each_room(fout_root_path, house_id_list)

	## first run the caabChange package to get durations of each activity and write the results to fin_duration_path
	## then run the below functions.
	duration_labelled_activity_func(fin_duration_path, fout_root_path, house_id_list)
	insert_per_minute_duration(fout_root_path, house_id_list)

	data_within_time_period(fout_root_path, f_project_path, house_id_list, time_periods, four_features_dirs)
	final_clean_func(f_project_path, "four_features_summer", house_id_list, time_periods)
	final_clean_func(f_project_path, "four_features_winter", house_id_list, time_periods)

	pandas_to_csv(f_project_path, "four_features_summer", house_id_list, time_periods)
	pandas_to_csv(f_project_path, "four_features_winter", house_id_list, time_periods)
	


