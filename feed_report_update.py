#!/bin/env python

import sys, time, pprint, argparse, cbapi, warnings, json
from cli_parser import build_cli_parser


def main():
    args = build_cli_parser()
    if not args.url or not args.token or not args.feedid or not args.reportid:
      print "Missing required param; run with --help for usage"
      sys.exit(-1)

    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # retrieve threat report 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        report = cb.feed_report_info(args.feedid, args.reportid)
    pprint.pprint(report)
    url = "%s/api/v1/feed/threat_report" % (args.url)
    
    updated_report = {'ids': {}, 'updates': {}}
    updated_report['ids'][report['feed_id']] = [report['id']]
    updated_report['updates']['is_ignored'] = 'True'
  
    print "#########"
    print 'args.url = ', args.url
    print 'complete_url = ', url
    
    t = cb.cbapi_post('https://192.168.230.201/api/v1/threat_report', data=json.dumps(updated_report))
    print "works: ", t
    r = cb.cbapi_post(url, data=json.dumps(updated_report))
    print "borks: ", r
    #r = cb.cbapi_post(url, data=(updated_report))
    r.raise_for_status()
    pprint.pprint(r)


if __name__ == "__main__":
    sys.exit(main())
