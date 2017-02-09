#!/bin/env python

__author__ = 'BJSwope'
import sys
from cbapi.response import CbEnterpriseResponseAPI, Sensor

def main():
    c = CbEnterpriseResponseAPI(profile="default")
    sensors = c.select(Sensor)
    for sensor in sensors:
        print sensor.computer_name, sensor.id, sensor.status, sensor.physical_memory_size, sensor.computer_dns_name

if __name__ == "__main__":
    sys.exit(main())
