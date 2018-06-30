import sys, struct, socket, pprint, argparse, warnings

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
    return parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        processes = cb.process_search(args.query, rows=args.rows)
    return processes

def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.url or not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    args.query=''
    args.rows=1
    processes = run_query(args)
    print ""
    for process in processes['results']:
        pprint.pprint(process)
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())

