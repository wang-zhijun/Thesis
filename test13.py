#!/usr/bin/env python

def line_number(filepath):

	count = -1 
	for count, line in enumerate(open(filepath, "rU")):
		pass
	return count + 1

if __name__ == '__main__':
	print line_number('/home/wzj/Programming/Thesis/test.py')
