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
    parser.add_argument("-q", "--query", action="store", default=None, dest="query",
                      help="binary query")
    parser.add_argument("-f", "--fields", action="append", default=[], dest="fields", type=str,
                      help="Field(s) to be returned.  For multiple fields, use this option multiple times.")
    parser.add_argument("-l", "--listfields", action="store_true", default=None, dest="list_fields",
                      help="To get a list of available fields to return, use this flag and do not provide an '-f' argument.")
    return parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    print args
    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.binary_summary(args.query)
    return answer

def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.url or not args.token or args.query is None:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    if not args.fields:
        if args.list_fields:
            args.query='18bd0948d254894441dd6f818d9b3811 '
            print args
            print
            answer = run_query(args)
            print answer
            print
            for i in sorted(answer):
                print i
                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(answer[i])
                print 
            sys.exit(0)
        else:
            sys.stderr.write("No fields specified, will return endpoint and observered_filename fields. For a list of available fields run the script with the '-l' argument.\n\n")
            args.fields = []
    answer = run_query(args)
    print answer

if __name__ == "__main__":
    sys.exit(main())
