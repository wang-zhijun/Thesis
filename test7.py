#!/usr/bin/env python
# -*- coding:utf-8 -*-

################################
#行の先頭に数個のスペースをつける
################################
def reindent(s, numSpace):
	leading_space = numSpace * ' '
	lines = [ leading_space + line.strip() for line in s.splitlines()]
	return '\n'.join(lines)

foo = open('/etc/hosts')
bar = open('/home/wzj/Programming/Thesis/file','w')
s = foo.read()
t = reindent(s,4)
bar.write(t)
