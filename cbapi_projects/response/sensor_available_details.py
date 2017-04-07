#!/bin/env python

__author__ = 'BJSwope'
import sys
from cbapi.response import CbEnterpriseResponseAPI, Sensor
import pprint

pp = pprint.PrettyPrinter(indent=4)


def main():
    c = CbEnterpriseResponseAPI(profile="default")
    sensors = c.select(Sensor)
    for sensor in sensors:
		for k in sorted(sensor._info):
			print k
		sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
