import sys, struct, socket, pprint, argparse, warnings
##
#
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
    parser.add_argument("-r", "--rows", action="store", default=20, dest="rows", type=int,
                      help="Number of rows to be returned.  Default = 20")
    parser.add_argument("-f", "--fields", action="append", default=[], dest="fields", type=str,
                      help="Field(s) to be returned.  For multiple fields, use this option multiple times.")
    parser.add_argument("-l", "--listfields", action="store_true", default=None, dest="list_fields",
                      help="To get a list of available fields to return, use this flag and do not provide an '-f' argument.")
    return parser

def run_query(args):

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)

    # use the cbapi object to perform a process based search
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        answer = cb.binary_search(args.query, rows=args.rows)
    return answer

def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.url or not args.token or args.query is None:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    if not args.fields:
        if args.list_fields:
            args.query='observed_filename:cmd.exe'
            args.rows=1
            answer = run_query(args)
            
            print "List of fields available to be returned by this script:"
            for result in answer['results']:
                for k in sorted(result.iterkeys()):
                    print k
            sys.exit(0)
        else:
            sys.stderr.write("No fields specified, will return endpoint and observered_filename fields. For a list of available fields run the script with the '-l' argument.\n\n")
            args.fields = []
            args.fields.append('endpoint')
            args.fields.append('observed_filename')

    answer = run_query(args)

    #Write a warning to stderr so any program that consumes stdout will not have to parse this warning
    if answer['total_results'] > args.rows:
        sys.stderr.write( "Warning: Query returned %s total result(s), but only displaying %s result(s).\n" % (answer['total_results'], args.rows))

    print "%-17s : %s" % ('Displayed Results', len(answer['results']))
    print "%-17s : %s" % ('Total Results', answer['total_results'])
    print "%-17s : %sms\n" % ('Query Time', int(1000*answer['elapsed']))

    for result in answer['results']:
        fields_to_print = []
        
        for field in args.fields:
            try:
                print field, " : ", result[field]
            except KeyError:
                print "None"
            try:
                fields_to_print.append(result[field])
            except KeyError:
                fields_to_print.append(None)
        
        if 'observed_filename' in result:
            print "%-20s :" % ('On-Disk Filename(s)'), 
            # result['observed_filename'][0].split('\\')[-1])
            for observed_filename in result['observed_filename']:
                print " %s" % (observed_filename.split('\\')[-1]),

    
if __name__ == "__main__":
    sys.exit(main())
