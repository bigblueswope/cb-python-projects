#!/bin/env python

import sys, pprint, argparse, cbapi, warnings, json
from cli_parser import build_cli_parser

cb_servers = {
    'carbonblack.bit9se.com': 'fe067f2792a5cf36e1486c4467dd2c473e0990f6',
    'tnc.my.carbonblack.io': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
}


def main():
    args = build_cli_parser()
    if not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    if not args.parse_string:
        print "Missing the url containting the Server, Feed ID and Report ID to parse."
        sys.exit(-1)

    su = args.parse_string.strip()
    su_list = su.split('/',)
    if len(su_list) != 6:
        print "Length of list from parsed url is not 6."
        print "Printing parsed url and list and exiting script."
        print args.parse_string
        print su_list
        sys.exit(-1)
    feed_host = su_list[2]
    feed_id = su_list[-2]
    report_id = su_list[-1]
    
    if not feed_host in cb_servers:
        print "%s not in list of cb_servers.  exiting" % (feed_host)
        sys.exit(1)
    args.url = 'https://%s' % (feed_host)
    args.token = cb_servers[feed_host]

    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # retrieve threat report 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        report = cb.feed_report_info(feed_id, report_id)
    
    feed_name = report['feed_name']
    #feed_id = report['feed_id']
    report_id = report['id']
    
    updated_report = {'ids': {}, 'updates': {}}
    
    if report['is_ignored'] == True:
        updated_report['updates']['is_ignored'] = False
    elif report['is_ignored'] == False:
        updated_report['updates']['is_ignored'] = True
        
    
    for server in cb_servers.keys():
        args.url = 'https://%s' % (server)
        args.token = cb_servers[server]
        cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)
        feed_id = cb.feed_get_id_by_name(feed_name)
        updated_report['ids'] = {}
        updated_report['ids'][feed_id] = [report_id]
        url = "%s/api/v1/threat_report" % (args.url)
        r = cb.cbapi_post(url, data=json.dumps(updated_report))
        if r.status_code == 200:
            print "%s (report_id: %s) is_enabled was successfully set to %s on %s" % (report['title'], report['id'], updated_report['updates']['is_ignored'], server)
        else:
            r.raise_for_status()

if __name__ == "__main__":
    sys.exit(main())