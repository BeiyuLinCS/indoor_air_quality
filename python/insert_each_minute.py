import datetime
from datetime import datetime, timedelta

def convert_string_to_date(input_string):
	res = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
	return res

def daterange(date1, date2):
    for n in range(int ((date2 - date1).total_seconds()/60 +1)):
        yield date1 + timedelta(minutes=n)
