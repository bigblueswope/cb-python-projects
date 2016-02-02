import sys, struct, socket, pprint, argparse, warnings

# in the github repo, cbapi is not in the example directory
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')

import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Perform a binary search")

    # for each supported output type, add an argument
    #
    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_argument("-n", "--no-ssl-verify", action="store_false", default=False, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_argument("-l", "--listfields", action="store_true", default=None, dest="list_fields",
                      help="To get a list of available fields to return, use this flag and do not provide an '-f' argument.")
    return parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.process_search(args.query, rows=args.rows)
    return answer

def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.url or not args.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    args.query = ''
    args.rows = 1
    answer = run_query(args)
    print "List of fields available to be returned by a process search:"
    unique_field_names = []
    for result in answer['results']:
        for k in result.iterkeys():
            if k not in unique_field_names:
                unique_field_names.append(k)
    for l in sorted(unique_field_names):
        print l
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
