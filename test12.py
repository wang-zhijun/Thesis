#!/usr/bin/env python

import zipfile

z = zipfile.ZipFile("/home/wzj/Downloads/7za920.zip", "r")
for filename in z.namelist():
	print 'File: ', filename
	bytes = z.read(filename)
	print 'has', len(bytes), 'bytes'
