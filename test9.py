#!/usr/bin/env python

def multiples_of_3_and_5():
	sum = 0
	for x in xrange(1,334):
		tmp = x * 3
		if tmp % 5 != 0:
			sum += tmp
	for x in xrange(1,200):
		sum += x*5

	return sum

print  multiples_of_3_and_5()
			
