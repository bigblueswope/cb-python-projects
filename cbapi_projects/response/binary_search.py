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

    # for each result 
    for binary in binary_query:
        try: 
            s = datetime.datetime.strptime(binary.server_added_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            now = datetime.datetime.utcnow()
            dwell_time = now-s
        except ValueError:
            try:
                s = datetime.datetime.strptime(binary.server_added_timestamp, "%Y-%m-%dT%H:%M:%SZ")
                now = datetime.datetime.utcnow()
                dwell_time = now-s
            except ValueError:
                dwell_time = "Indeterminate"
        print binary
        print ("=" * 80)
        print(binary.md5sum)
        print("-" * 80)
        print("%-20s : %s" % ('Dwell Time', dwell_time))
        print("%-20s : %s" % ('First Seen', binary.server_added_timestamp))
        print("%-20s : %s" % ('Size (bytes)', binary.size))
        print("%-20s : %s" % ('Signature Status', binary.signed))
        print("%-20s : %s" % ('Publisher', binary.digsig_publisher) if binary.signed == True else "%-20s : %s" % ('Publisher', 'n/a'))
        print("%-20s : %s" % ('Product Version', binary.product_version))
        print("%-20s : %s" % ('File Version', binary.file_version))
        print("%-20s : %s" % ('64-bit (x64)', binary.is_64bit))
        print("%-20s : %s" % ('EXE', binary.is_executable_image))

        for fn in binary.observed_filenames:
            print("%-20s : %s" % ('On-Disk Filename', fn.split('\\')[-1]))

        print('\n')

if __name__ == "__main__":
    sys.exit(main())
