This package is used to calculate the 4 features for the Indoor Air Quality Projects. 

1. run "extract_data_from_database.py" to extract raw sensor data from CASAS's database and write under ../data/testbed_name. 
Change lines 130 through 132 to set up the testbed name, starting and end time of the extracted data.

2. download the labelled data and save them to ./data/

3. in caabChange package, run the script to get the duration of each labelled activity / per minute. 
write the data under the directory "./processed_data/testbed_name/duration/"
There is a README.txt under the caabChange directory. 

4. run "main.py".
Four features will be calculated: 
feature "wd_open_area" will be calculated by function window_door_open_area_funcs
feature "temperature" will be calculated by function temp_func
feature "overall_activity_per_room" will be calculated by functions extract_impute_motion_data and overall_activity_level_each_room
feature "duration_per_minute" will be calculated by function duration_labelled_activity_func
