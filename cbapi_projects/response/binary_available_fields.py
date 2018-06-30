#!/usr/bin/env python

import sys
import datetime
from cbapi.response.models import Binary
from cbapi.example_helpers import build_cli_parser, get_cb_response_object
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


def main():
    parser = build_cli_parser()
    parser.add_argument("--query", help="binary query", default='')
    args = parser.parse_args()

    cb = get_cb_response_object(args)
    binary_query = cb.select(Binary).where(args.query)
    
    for binary in binary_query:
		#print binary
		for k in sorted(binary._info):
			print k
		break

if __name__ == "__main__":
    sys.exit(main())
