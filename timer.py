#!/usr/bin/env python
import os
import time

s = 0
m = 0
h = 0

while s <= 60:
	os.system('clear')
	print h, 'Hours', m, 'Minutes', s, 'Seconds'
	time.sleep(1)
	s += 1
	if s == 60:
		m += 1
		s = 0
	elif m == 60:
		h += 1
		m = 0

