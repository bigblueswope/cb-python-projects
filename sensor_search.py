#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, cbapi, pprint, warnings
from cli_parser import build_cli_parser

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sensor = cb.sensor(args.sensor)
    
    pprint.pprint(sensor)
    #for k in sorted(sensor):
    #    print k

if __name__ == "__main__":
    sys.exit(main())

