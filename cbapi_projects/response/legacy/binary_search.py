#!/bin/env python
import sys, cbapi
from cli_parser import build_cli_parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a binary based search
    answer = cb.binary_search(args.query, rows=args.rows,facet_enable=args.facet_enable)
    return answer

def main():
    args = build_cli_parser()
    if not args.url or not args.token or (args.query is None and not args.list_fields):
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    if not args.fields:
        if args.list_fields:
            #If -l flag was used, ignore the query from the command line and instead look for a binary added in the last 7 days
            #(because newer binaries may have additional fields that were added with a newer version of Carbon Black)
            args.query='server_added_timestamp:-10080m'
            #Ignore the -r argument from the command line and return a single row instead.
            args.rows=1
            answer = run_query(args)
            
            print "List of fields available to be returned by this script:"
            for binary in answer['results']:
                for k in sorted(binary.iterkeys()):
                    print k
            sys.exit(0)
        else:
            #Write a warning to stderr so any program that consumes stdout will not have to parse this warning
            sys.stderr.write("No fields specified, will return endpoint and observered_filename fields. For a list of available fields run the script with the '-l' argument.\n")
            args.fields = []
            args.fields.append('endpoint')
            args.fields.append('observed_filename')

    answer = run_query(args)

    if answer['total_results'] > args.rows:
        sys.stderr.write( "Warning: Query returned %s total result(s), but only displaying %s result(s).\n" % (answer['total_results'], args.rows))
    
    for binary in answer['results']:
        fields_to_print = []
        for field in args.fields:
            try:
                fields_to_print.append(binary[field])
            except KeyError:
                fields_to_print.append("")
        if fields_to_print:
            print fields_to_print

    
if __name__ == "__main__":
    sys.exit(main())
