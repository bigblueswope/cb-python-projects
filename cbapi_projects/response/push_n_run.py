#!/usr/bin/env python

import sys
import time
from cbapi.response import CbEnterpriseResponseAPI, Sensor
from cbapi.response.live_response_api import LiveResponseError
import datetime
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
c = CbEnterpriseResponseAPI()
 
print("Enter Sensor ID")
sensor_id = raw_input()
print "Setting Sensor"
sensor = c.select(Sensor, sensor_id)

print "Establishing LR session to sensor %s (%s)" % (sensor.computer_dns_name, sensor.computer_name)

with sensor.lr_session() as session:	# this will wait until the Live Response session is established
	try:
		print "Pushing file to sensor."
		# read collect_system_info.bat and write it to the destination host
		# if no paths are provided
		#  the source file must be in the same directory as this script
		#  and the destination file will land in CB's default directory
		#  on Windows that is C:\Windows\CarbonBlack\
		session.put_file(open("collect_system_info.bat", "r"), "collect_system_info.bat")
	except LiveResponseError as e: 
		if e.win32_error == 0x80070050: # Win32 Error Code meaning the file already exists
			file_info = session.list_directory("collect_system_info.bat")
			lmod = datetime.datetime.fromtimestamp(int(file_info[0]['last_write_time'])).strftime('%Y-%m-%d %H:%M:%S')
			print "File exists. Last Modified: %s" % (lmod)
			print "Keep existing or Replace with new version: (k/r)"
			kflag = raw_input()
			try:
				if kflag[0] in ['K','k']:
					print "Keeeping existing file."
				elif kflag[0] in ['R', 'r']:
					print "Deleting existing and re-pushing new version."
					session.delete_file("collect_system_info.bat")
					session.put_file(open("collect_system_info.bat", "r"), "collect_system_info.bat")
				else:
					print "Response did not begin with either K or R.  Exiting program."
					sys.exit(1)
			except IndexError as e:
				print "No response received.  Exiting program."
				sys.exit(1)
		else:
			raise
	print "Running command"
	session.create_process("cmd.exe /c collect_system_info.bat")	# output has the stdout from running collect_system_info.bat
	print "Sleeping 15 seconds before retrieving the output."
	time.sleep(15)
	results = session.get_file("system_info.txt")
	print results

