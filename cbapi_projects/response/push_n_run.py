#!/usr/bin/env python

import sys
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
 
print "Establishing LR session to sensor"
with sensor.lr_session() as session:	# this will wait until the Live Response session is established
	try:
		print "Pushing file to sensor."
		session.put_file(open("test.bat", "r"), "test.bat")
	except LiveResponseError as e:
		if e.win32_error == 0x80070050:
			file_info = session.list_directory("test.bat")
			lmod = datetime.datetime.fromtimestamp(int(file_info[0]['last_write_time'])).strftime('%Y-%m-%d %H:%M:%S')
			print "File exists. Last Modified: %s" % (lmod)
			print "Keep existing or Replace with new version: (k/r)"
			kflag = raw_input()
			try:
				if kflag[0] in ['K','k']:
					print "Keeeping existing file."
				elif kflag[0] in ['R', 'r']:
					print "Deleting existing and re-pushing new version."
					session.delete_file("test.bat")
					session.put_file(open("test.bat", "r"), "test.bat")
				else:
					print "Response did not begin with either K or R.  Exiting program."
					sys.exit(1)
			except IndexError as e:
				print "No response received.  Exiting program."
				sys.exit(1)
		else:
			raise
	print "Running command"
	print session.create_process("cmd.exe /c test.bat")	# output has the stdout from running c:\test.bat

