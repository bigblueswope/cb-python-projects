#!/bin/env python

__author__ = 'BJSwope'
import sys
import csv
from cbapi.response import CbEnterpriseResponseAPI, Sensor


outfile=open("sensors.csv","wb")
wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)

def main():
	c = CbEnterpriseResponseAPI(profile="default")
	sensor = c.select(Sensor).first()
	field_list = []
	for k in sorted(sensor._info):
		field_list.append(k)
	wr.writerow(field_list)

	sensors = c.select(Sensor)
	for sensor in sensors:
		sensor_details = []
		for i in field_list:
			sensor_details.append(getattr(sensor, i, ""))
		wr.writerow(sensor_details)

if __name__ == "__main__":
    sys.exit(main())
