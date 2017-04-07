#!/bin/env python

__author__ = 'BJSwope'
import sys
import csv
from cbapi.response import CbEnterpriseResponseAPI, Sensor
import pprint

pp = pprint.PrettyPrinter(indent=4)


outfile=open("sensors.csv","wb")
wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)

def main():
	c = CbEnterpriseResponseAPI(profile="default")
	sensors = c.select(Sensor)
	field_list = []
	for sensor in sensors:
		for k in sorted(sensor._info):
			field_list.append(k)
		break
	wr.writerow(field_list)

	for sensor in sensors:
		sensor_details = []
		for i in field_list:
			try:
				sensor_details.append(sensor._info[i])
			except AttributeError:
				sensor_details.append("")
		wr.writerow(sensor_details)

if __name__ == "__main__":
    sys.exit(main())
