#!/bin/env python

import sys, pprint, argparse, warnings, cbapi
from cli_parser_tnc import build_cli_parser
from datetime import date, timedelta

def process_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.process_search(args.query, rows=args.rows)
    return answer

def alert_query(args):
    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.alert_search(args.query, rows=args.rows)
    return answer
     
def main():
    args = build_cli_parser()
    args.facet_enable='False'
    args.rows = 0

    if not args.url or not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    
    report_data = {}
    #Process Statistics
    #for dev purposes this is 3 days ago, the last time my demo has data
    yd = date.today() - timedelta(0)
    yd = yd.strftime('%Y-%m-%d')
    start_string = 'start:[%sT00:00:00 TO %sT23:59:59]' % (yd, yd)
    
    args.query=start_string
    answer = process_query(args)
    report_data['_report_date'] = yd
    report_data['procs_total'] = answer['total_results']

    args.query = start_string + 'block_status:"ProcessTerminated"'
    answer = process_query(args)
    report_data['procs_blocked'] = answer['total_results']
    
    args.query = start_string + 'block_status:"NotTerminatedSystemProcess"'
    answer = process_query(args)
    report_data['procs_not_terminated_system_proc'] = answer['total_results']

    args.query = start_string + 'block_status:"NotTerminatedCriticalSystemProcess"'
    answer = process_query(args)
    report_data['procs_not_terminated_critical_system_proc'] = answer['total_results']

    args.query = start_string + 'block_status:"NotTerminatedWhitelistedPath"'
    answer = process_query(args)
    report_data['procs_not_terminated_whitelisted_proc'] = answer['total_results']

    args.query = start_string + 'block_status:"NotTerminatedOpenProcessError"'
    answer = process_query(args)
    report_data['procs_not_terminated_open_proc_error'] = answer['total_results']

    args.query = start_string + 'block_status:"NotTerminatedTerminateError"'
    answer = process_query(args)
    report_data['procs_not_terminated_terminate_error'] = answer['total_results']

    args.query = start_string + 'block_status:"NotTerminatedCBProcess"'
    answer = process_query(args)
    report_data['procs_not_terminated_cb_process'] = answer['total_results']

    args.query = start_string + 'alliance_score_virustotal:[2 TO *]'
    answer = process_query(args)
    report_data['virus_total_score_ge_2'] = answer['total_results']

    # Alert Status
    # Adjust this created_string when ready for prod testing
    yd = date.today() - timedelta(0)
    yd = yd.strftime('%Y-%m-%d')
    created_string = 'created_time:[%sT00:00:00 TO %sT23:59:59]' % (yd, yd)
    
    args.query=created_string
    answer = alert_query(args)
    report_data['alerts_total_created'] = answer['total_results']

    args.query = created_string + 'status:"resolved"'
    answer = alert_query(args)
    report_data['alerts_resolved'] = answer['total_results']

    args.query = created_string + 'status:"unresolved"'
    answer = alert_query(args)
    report_data['alerts_unresolved'] = answer['total_results']

    args.query = created_string + 'status:"in progress"'
    answer = alert_query(args)
    report_data['alerts_in_progress'] = answer['total_results']

    args.query = created_string + 'status:"false positive"'
    answer = alert_query(args)
    report_data['alerts_false_positive'] = answer['total_results']


    # Alert Resolution Calculations
    # Adjust this created_string when ready for prod testing

    yd = date.today() - timedelta(0)
    yd = yd.strftime('%Y-%m-%d')
    resolved_string = 'resolved_time:[%sT00:00:00 TO %sT23:59:59]' % (yd, yd)
    
    args.query = resolved_string
    answer = alert_query(args)
    report_data['all_alerts_resolved_yesterday'] = answer['total_results']

    #pprint.pprint(report_data)
    for k in sorted(report_data.keys()):
        print k + ': ' + str(report_data[k])


if __name__ == "__main__":
    sys.exit(main())
