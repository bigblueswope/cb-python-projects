#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, warnings
from cli_parser import build_cli_parser

# in the github repo, cbapi is not in the example directory
sys.path.append('../../../cbapi/client_apis/python/src/cbapi/')

import cbapi 

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    #If this script is run without -c and -a arguments the defaults will point to BJs VM on his laptop.
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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            processes = cb.process_search(args.query, rows=args.rows, facet_enable=args.facet_enable)
        print "List of fields available to be returned by this script:"
        for process in processes['results']:
            for k in sorted(process.iterkeys()):
                print k
        sys.exit(0)
    if not args.fields:
        #Write a warning to stderr so any program that consumes stdout will not have to parse this warning
        sys.stderr.write("No fields specified, will return hostname and cmdline fields. For a list of available fields run the script with the '-l' argument.\n")
        args.fields.append('hostname')
        args.fields.append('cmdline')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        processes = cb.process_search(args.query, rows=args.rows, facet_enable=args.facet_enable)
    
    if processes['total_results'] > args.rows:
        sys.stderr.write("Warning: Query returned %s total results, but only displaying %s results.\n" % (processes['total_results'], args.rows))

    # for each result 
    for process in processes['results']:
        fields_to_print = []
        for field in args.fields:
            fields_to_print.append(process[field])
        if fields_to_print:
            print fields_to_print
        

if __name__ == "__main__":
    sys.exit(main())

