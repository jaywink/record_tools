#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import os

target_dir = sys.argv[2]

source_file = csv.reader(open(sys.argv[1], 'rb'), delimiter=',', quotechar='"')


for row in source_file:
	try:
		os.rename(target_dir+'/AUDIO'+row[0]+'.MP3', target_dir+'/'+row[1]+'.mp3')
	except:
		print "Unable to process ",row[0],row[1]

print "done"

