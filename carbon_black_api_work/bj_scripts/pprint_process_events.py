import sys, pprint, argparse
sys.path.append('../../../cbapi/client_apis/python/src/cbapi/')
import cbapi 
from cli_parser import build_cli_parser

def run_query(args):
    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    processes = cb.process_search(args.query, rows=args.rows, facet_enable=False)
    return processes

def get_events(args, arg1, arg2):
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)
    # use the cbapi object to pull all the events related to a process' id and segment_id
    events = cb.process_events(arg1, arg2)
    return events

def main():
    args = build_cli_parser()
    #query for cmd.exe
    args.query = 'filemod_count:5 process_name:notepad.exe'
    #args.query = 'process_name:cmd.exe'
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

