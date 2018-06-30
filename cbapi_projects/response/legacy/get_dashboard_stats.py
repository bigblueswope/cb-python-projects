#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, pprint, warnings
from cli_parser import build_cli_parser
import cbapi 

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    if not args.url or not args.token :
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
   
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        stats = cb.get_dashboard_stats()
        pprint.pprint(stats)
    '''# for each result 
    for process in processes['results']:
        fields_to_print = []
        for field in args.fields:
            fields_to_print.append(process[field])
        if fields_to_print:
            print fields_to_print
    '''

if __name__ == "__main__":
    sys.exit(main())

