#!/usr/bin/env python

import sys
import datetime
import operator
from cbapi.response.models import Binary, Process
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
        s = datetime.datetime.strptime(binary.server_added_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.datetime.utcnow()
        dwell_time = now-s
        print(binary.md5sum)
        
        print("%-20s : %s" % ('Endpoint(s)', binary.endpoint))
        print("%-20s : %s" % ('Dwell Time', dwell_time))
        print("%-20s : %s" % ('First Seen', binary.server_added_timestamp))
        print("%-20s : %s" % ('Size (bytes)', binary.size))
        print "*"*80
        proc_query = cb.select(Process).where('filewrite_md5:%s' % (binary.md5sum))
        pd = {}
        for proc in proc_query:
            pd[proc.unique_id] = {}
            pd[proc.unique_id]['hostname'] = proc.hostname
            pd[proc.unique_id]['username'] = proc.username
            
            for fm in proc.filemods:
                if fm.type == "LastWrote" and fm.md5 == binary.md5sum.lower():
                    idt = now - fm.timestamp
                    pd[proc.unique_id]['dwell_time'] = idt
                    pd[proc.unique_id]['path'] = fm.path
        for entry in pd.keys():
            print pd[entry]['hostname'], pd[entry]['username'], pd[entry]['dwell_time'], pd[entry]['path']

if __name__ == "__main__":
    sys.exit(main())
