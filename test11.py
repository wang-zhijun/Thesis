#!/usr/bin/env python

import datetime, calendar

def find_last_friday():
	last_friday = datetime.date.today()

	one_day = datetime.timedelta(days = 1)

	while last_friday.weekday() != calendar.FRIDAY:
		last_friday -= on_day

	return last_friday.strftime('%Y-%m-%d %A')

if __name__ == '__main__':
	print find_last_friday()
