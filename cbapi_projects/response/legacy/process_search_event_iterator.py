#!/bin/env python
__author__ = 'BJSwope'
import sys, argparse, pprint, json
from cli_parser import build_cli_parser
import cbapi
 
def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    #The default values are specified in cli_parser.py
    if not args.url or not args.token or (args.query is None and not args.list_fields):
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    processes,events = cb.process_search_and_events_iter(args.query)
    pd = {}
    for i in processes:
        print "money"
        if i['netconn_count'] >= 1:
            print i['netconn_count']
            print i['netconn_complete']
            if pd.has_key(i['unique_id']):
                print i['unique_id']
                if pd[i['unique_id']].has_key(i['segment_id']):
                    print 'here'
                    for l in i['netconn_complete']:
                        pd[i['unique_id'][i['segment_id']]].append(l)
                else:
                    print 'there'
                    pd[i['unique_id']] = {}
                    pd[i['unique_id'][i['segment_id']]] = {}
                    for l in i['netconn_complete']:
                        pd[i['unique_id'][i['segment_id']]].append(l)
            else:
                print 'elsewhere'
                pd[i['unique_id']] = {}
                pd[i['unique_id'][i['segment_id']]] = []
                for l in i['netconn_complete']:
                    #print l
                    pd[i['unique_id'][i['segment_id']]].append(l)
            #pprint.pprint(pd)
 
if __name__ == "__main__":
    sys.exit(main())
