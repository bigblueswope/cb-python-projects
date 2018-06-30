#!/bin/env python
import sys, pprint, warnings, cbapi
from cli_parser import build_cli_parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a binary based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.binary_search(args.query, rows=args.rows,facet_enable=args.facet_enable)
    return answer

def main():
    args = build_cli_parser()
    if not args.url or not args.token or not args.query:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    answer = run_query(args)

    for binary in answer['results']:
        pprint.pprint(binary)
    
if __name__ == "__main__":
    sys.exit(main())
