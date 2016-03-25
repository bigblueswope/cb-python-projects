#!/bin/env python

import sys, string, re 

if len(sys.argv) != 2:
	print "useage: %s /var/log/cb/ngnix/access.log-YYYYMMDD\n" % sys.argv[0]
	sys.exit()

#search pattern
client_pattern = re.compile('/sensor/checkin/')

# dictionary to hold our counts
day_dict = {}

#create an entry in the dict for each hour and 10 minute combination
for i in range(0,24):
	#define the hours 0-23 and ensure they are 2 digits with a leading 0
	hour = str(i).zfill(2)
	for j in range (0,6):
		#define the 10 minute intervals ensure they are 2 digits with a trailing 0
		min = str(j).ljust(2, '0')
		#combine the two values with a colon
		hourmin = hour + ':' + min
		#create a key/value pair in the dictionary with the key being HH:MM and the value being an empty list
		day_dict[hourmin] = []

f=open(sys.argv[1], 'r')
for line in f:
	#sample line:
	#::ffff:192.168.230.5 - - [18/Feb/2016:19:54:09 -0500(0.015)] "POST /sensor/checkin/13 HTTP/1.1" 200 158 "-" "-" "-"
	if re.search(client_pattern,line):
		#split the line up to get the sensor_id
		sensor_id = string.split(line,' ')[6]
		sensor_id = string.split(sensor_id, '/')[3]
		
		#split the line to get the hour and minute
		line_split= string.split(line,':')
		hour = line_split[4]
		#grab the 10s digit from the minutes and append a 0 to it
		min = line_split[5][0:1].ljust(2,'0')
		
		#combine the two values with a colon 
		hourmin =  hour + ':' + min
		
		#if the hourmin list does not have the sensor_id as a value, append the sensor_id the list
		if not sensor_id in day_dict[hourmin]:
			day_dict[hourmin].append(sensor_id)
		
print "Time,Count of Unique CB Sensors"

key_list = day_dict.keys()
key_list.sort()
for k in key_list:
	#the length of each hourmin list in the dictionary is the count of unique clients that have been seen in that time interval
	print "%s,%s" % (k, len(day_dict[k]))
