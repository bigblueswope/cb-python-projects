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
                        sn = sensor.computer_name
                        dt = i['timestamp'][0:19]
                        event_bytes = int(i['num_eventlog_bytes'])
                        binary_bytes = int(i['num_storefile_bytes'])
                        if dt in band_dict.keys():
                            band_dict[dt][0] += 1
                            band_dict[dt][1] += event_bytes
                            band_dict[dt][2] += binary_bytes
                            band_dict[dt][3].append(sn)
                        else:
                            band_dict[dt] = [1,event_bytes, binary_bytes, [sn]]
            except AttributeError:
                pass
    
    with open('max_id.txt', 'w') as target:
        target.write(id_max_new)

    for k in sorted(band_dict):
        #band_dict key is a date-time stamp (YYYY-MM-DD hh:mm:ss)
        #band_dict value is list consisting of # of sensors that checked-in, sum of eventlog bytes, sum of binary upload bytes
        print "%s,%s,%d,%d,%s" % (k, band_dict[k][0], band_dict[k][1], band_dict[k][2], band_dict[k][3])

if __name__ == "__main__":
    sys.exit(main())

