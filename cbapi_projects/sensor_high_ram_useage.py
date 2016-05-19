#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, cbapi, pprint, warnings, json
from cli_parser import build_cli_parser

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        query_parameters={}
        # Todo: Add arguments handler to collect ip, hostname or groupid from command line 
        #  to add to the query_parameters dict so we don't have to iterate over EVERY sensor 
        #  if we don't want to.
        """
        get sensors, optionally specifying search criteria

        as of this writing, supported search criteria are:
          ip - any portion of an ip address
          hostname - any portion of a hostname, case sensitive
          groupid - the sensor group id; must be numeric

        returns a list of 0 or more matching sensors
        """
        sensors = cb.sensors(query_parameters)
    for sensor in sensors:
        if sensor['uninstalled'] != 'False' and sensor['status'] == 'Online':
            r = cb.sensor_resourcestatus(sensor['id'])
            if r:
                p = json.loads(r)
                ramMB = int(p[0]['commit_charge'])/1048576
                # For testing in lab, using 10 MB as a "High" threshold.
                # For production consider changing it to 100 MB
                if ramMB  >= 10:
                    print "%s has high RAM use:  %d MB" % (sensor['computer_name'], ramMB)

if __name__ == "__main__":
    sys.exit(main())

