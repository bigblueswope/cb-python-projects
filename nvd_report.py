import sys, struct, socket, pprint, argparse, warnings, csv, time, datetime

# in the github repo, cbapi is not in the example directory
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')

import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Performs a process search. Returns desired fields as a list.", fromfile_prefix_chars='@')

    # for each supported configuration option, add an option
    #
    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="Carbon Black API Authentication Token")
    parser.add_argument("-n", "--no-ssl-verify", action="store_false", default=False, dest="ssl_verify",
                      help="SSL Verification. Default = Do not verify")
    parser.add_argument("-o", "--outfile", action="store", default=None, dest="outfile",
                      help="Optional output file to save results")
    parser.add_argument("-i", "--interval", action="store", default=None, dest="interval",
                      help="Optional oldest process age (in days) to query", type=int)

    return parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        processes = cb.process_search(args.query, rows=args.rows)
    return processes

def get_events(args, arg1, arg2):
    
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)
    
    # use the cbapi object to pull all the events related to a process' id and segment_id
    events = cb.process_events(arg1, arg2)
    return events

def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.outfile:
	    cwriter = csv.writer(sys.stdout)
    else:
        outfile = open(args.outfile, 'w')
        cwriter = csv.writer(outfile)
    if args.interval:
        lastupdate_time = (datetime.datetime.now() - datetime.timedelta(days=args.interval)).strftime("%Y-%m-%d")
        args.query = 'alliance_score_nvd:* last_update:[%s TO *]' % lastupdate_time
    else:
        args.query = 'alliance_score_nvd:*'
    #request the process' id and segment id
    args.fields = ['id','segment_id']
    ##########
    #######Need to write logic to handle large numbers of results to the processes query
    ##########
    args.rows = 30
    if not args.url or not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    #run the query using the details we built above
    processes = run_query(args)
    
    cwriter.writerow(['process_md5', 'process_path', 'hostname'])
    # for each process in the results dict
    for process in processes['results']:
        #get the process events so we can pull the NVD feed hits for the process
        events = get_events(args, process['id'], process['segment_id'])
        monkey = [events['process']['process_md5'], events['process']['path'], events['process']['hostname']]
        cwriter.writerow(monkey)


if __name__ == "__main__":
    sys.exit(main())

