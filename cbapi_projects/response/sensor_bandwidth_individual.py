#!/bin/env python

__author__ = 'BJSwope'
import sys
import requests.packages.urllib3
from cbapi.response import CbEnterpriseResponseAPI, Sensor

requests.packages.urllib3.disable_warnings()

def main():
    band_dict = {}
    try:
        with open('max_id.txt', 'r') as target:
            id_max_old = target.readline()
            id_max_old = id_max_old.strip()
    except:
        id_max_old = 0
    id_max_new = id_max_old
    c = CbEnterpriseResponseAPI(profile="default")
    sensor_list = c.select(Sensor)
    for sensor in sensor_list:
        if sensor.queued_stats:
            try:
                for i in sensor.queued_stats:
                    if i['id'] > id_max_old:
                        if i['id'] > id_max_new:
                            id_max_new = i['id']
                        dt = i['timestamp'][0:19]
                        sn = sensor.computer_name
                        event_bytes = int(i['num_eventlog_bytes'])
                        binary_bytes = int(i['num_storefile_bytes'])
                        print "%s,%s,%d,%d" % (dt, sn, event_bytes, binary_bytes)
            except AttributeError:
                pass
    
    with open('max_id.txt', 'w') as target:
        target.write(id_max_new)

if __name__ == "__main__":
    sys.exit(main())

