#!/usr/bin/env python

def sum_of_even_fibonacci(max):
	a, b, sum = 0, 2, 0
	while b < 4000000:
		sum = sum + b
		a, b = b, 4*b+a
	return sum

if __name__ == '__main__':
	sum = sum_of_even_fibonacci(4000000)
	print sum
