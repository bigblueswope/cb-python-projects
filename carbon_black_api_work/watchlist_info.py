import sys, struct, socket, pprint, argparse, warnings

# in the github repo, cbapi is not in the example directory
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')

import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(usage="%prog [options]", description="Dump Binary Info")

    # for each supported output type, add an option
    #
    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_argument("-n", "--no-ssl-verify", action="store_false", default=False, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_argument("-i", "--id", action="store", default=None, dest="id")
    return parser

def print_details(p):
    print '%-20s | %s' % ('field', 'value')
    print '%-20s + %s' % ('-' * 20, '-' * 60)
    print '%-20s | %s' % ('id', p['id'])
    print '%-20s | %s' % ('name', p['name'])
    print '%-20s | %s' % ('date_added', p['date_added'])
    print '%-20s | %s' % ('last_hit', p['last_hit'])
    print '%-20s | %s' % ('last_hit_count', p['last_hit_count'])
    print '%-20s | %s' % ('search_query', p['search_query'])
    print '%-20s | %s' % ('readonly', p['readonly'])
    print "\n"

def main():
    parser = build_cli_parser()
    opts = parser.parse_args()
    if not opts.url or not opts.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=opts.ssl_verify)

    # get record describing this watchlist  
    # if no watchlist id is specified, return all watchlists
	#
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        watchlist = cb.watchlist(opts.id) 
    
    if type(watchlist) is list:
        for p in watchlist:
            print_details(p)
    elif type(watchlist) is dict:
        print_details(watchlist)

if __name__ == "__main__":
    sys.exit(main())
