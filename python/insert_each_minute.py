import datetime
from datetime import datetime, timedelta

def convert_string_to_date(input_string):
	# '2015/8/25''%Y-%m-%d'
	res = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
	return res

def daterange(date1, date2):
	# (next_datetime - curr_datetime).total_seconds()
    for n in range(int ((date2 - date1).total_seconds()/60 +1)):
        yield date1 + timedelta(minutes=n)

# def insert_each_minute_func(start_dt, end_dt):
# start_dt = convert_string_to_date("2015-12-20 00:10:20")
# end_dt = convert_string_to_date("2016-1-11 10:59:30")
# for dt in daterange(start_dt, end_dt):
#     print(dt.strftime("%Y-%m-%d %H:%M:%S"))