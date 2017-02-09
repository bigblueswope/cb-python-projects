#!/bin/env python

import sys, argparse, cbapi, pprint, json
from cli_parser import build_cli_parser
 
def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    #The default values are specified in cli_parser.py
    if not args.url or not args.token or (args.query is None and not args.list_fields):
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    if args.list_fields:
        #ignore any query on the command line and set the query to look for processes that started in the last 7 days
        #(because newer versions of CB may have different fields than what was available on older data)
        args.query='start:-10080m'
        #ignore the number of rows from the command line and set the row count to 1
        args.rows=1
        processes = cb.process_search(args.query, rows=args.rows, facet_enable=args.facet_enable)
        print "List of fields available to be returned by this script:"
        for process in processes['results']:
            for k in sorted(process.iterkeys()):
                print k
        sys.exit(0)
 
    processes = cb.process_search_and_events_iter(args.query)
    print args.query
    
    for proc in processes:
        #for m in proc[0]:
        #    p0.append(m)
        print "########################"
        #for m in proc[1]:
        #    p1.append(m)
        print sorted(list(set(proc[0])-set(proc[1])))
        print sorted(list(set(proc[1])-set(proc[0])))
        #for m in proc[1]['alliance_hits']['38']['hits']:
 
if __name__ == "__main__":
    sys.exit(main())
