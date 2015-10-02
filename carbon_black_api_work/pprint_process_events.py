import sys, struct, socket, pprint, argparse, warnings
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')
import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Performs a process search. Returns desired fields as a list.", fromfile_prefix_chars='@')

    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="Carbon Black API Authentication Token")
    parser.add_argument("-n", "--no-ssl-verify", action="store_false", default=False, dest="ssl_verify",
                      help="SSL Verification. Default = Do not verify")
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
    #query for cmd.exe
    args.query = 'process_name:cmd.exe'
    #request the process' id and segment id, these two fields are the data needed to request the events associated with a specific process
    args.fields = ['id','segment_id']
    #return a single process because we just want some sample data to print out
    args.rows = 1
    if not args.url or not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    #run the query using the details we built above
    processes = run_query(args)
    
    # for each process in the results dict
    for process in processes['results']:
        events = get_events(args, process['id'], process['segment_id'])
        pprint.pprint(events)

if __name__ == "__main__":
    sys.exit(main())

