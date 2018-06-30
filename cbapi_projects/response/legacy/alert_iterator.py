#!/bin/env python

import sys, argparse, pprint, json, cbapi, warnings
from cli_parser_tnc import build_cli_parser
 
def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    #The default values are specified in cli_parser.py
    if not args.url or not args.token or (args.query is None and not args.list_fields):
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print args.query
        processes = cb.alert_search(args.query)
        #processes = cb.alert_search_iter(args.query)
        print "@@@@@@@@@@@"
        print processes
    for proc in processes:
        #for m in proc[0]:
        #    p0.append(m)
        print "########################"
        pprint.pprint(proc)
        #for m in proc[1]:
        #    p1.append(m)
        #print sorted(list(set(proc[0])-set(proc[1])))
        #print sorted(list(set(proc[1])-set(proc[0])))
        #for m in proc[1]['alliance_hits']['38']['hits']:
 
if __name__ == "__main__":
    sys.exit(main())
