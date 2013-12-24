#!/usr/bin/env python

def is_prime(n):
	tmp = n
	i = 2
	while tmp:
		if tmp % i == 0 & i != tmp:
			return False
		i += 1
		tmp = tmp / i
	return True

if __name__ == '__main__':
	val = 1
	count = 0	
	while True:
		if is_prime(val):
			count += 1	
			if count == 10001:
				print val
				break
		else:
			val += 1
