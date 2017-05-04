#!/usr/bin/env python

from cbapi.response import CbEnterpriseResponseAPI, Sensor
from cbapi.response.live_response_api import LiveResponseError
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
c = CbEnterpriseResponseAPI()
 
print("Enter Sensor ID")
sensor_id = raw_input()
sensor = c.select(Sensor, sensor_id)
 
with sensor.lr_session() as session:	# this will wait until the Live Response session is established
	try:
		session.put_file(open("test.bat", "r"), "c:\\test.bat")
	except LiveResponseError as e:
		if e.win32_error == 0x80070050:
			print "File already exists.  Running script now."
			pass
		else:
			raise
	
	output = session.create_process("cmd.exe c:\\test.bat")	# output has the stdout from running c:\test.bat
	print output
