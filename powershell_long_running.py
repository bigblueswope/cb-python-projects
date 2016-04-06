#!/bin/env python
import datetime, sys, pprint, cbapi
from cli_parser import build_cli_parser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings() 
    
def run_query(args):
    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to iterate over all matching process documents
    r = cb.process_search_iter(args.query)
    return r

def main():
    args = build_cli_parser()
    args.query = 'process_name:powershell.exe'
    answer = run_query(args)
    count = 0 
    lrcount = 0
    # iterate over each process document in the results set
    for pdoc in answer:
        count += 1
        # Start time
        start = datetime.datetime.strptime(pdoc['start'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Last Update time
        ludate = datetime.datetime.strptime(pdoc['last_update'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Difference betweeen the two
        runtime = int((ludate - start).seconds)
        # Change the compared value if 60 seconds is not considered a long run of powershell
        if runtime > 60:
            lrcount += 1
            print "#########################"
            print "Proc Doc: %s/#/analyze/%s/%d" % (args.url, pdoc['id'], pdoc['segment_id'])
            print "Hostname: ", pdoc['hostname']
            print "Username: ", pdoc['username']
            print "Process Name: ", pdoc['process_name']
            print "Command Line: ", pdoc['cmdline']
            print "Runtime: %d seconds" % runtime
            print "$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "Matching Process Count: ", count
    print "Matching Long Running Process Count: ", lrcount
    
if __name__ == "__main__":
    sys.exit(main())
