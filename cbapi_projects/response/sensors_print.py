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
        print "Next Check In: %s" % (sensor.next_checkin_time)
        print sensor.computer_name, sensor.id, sensor.status, sensor.physical_memory_size, sensor.computer_dns_name

if __name__ == "__main__":
    sys.exit(main())
