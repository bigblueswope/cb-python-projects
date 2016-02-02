# This script requires 3 arguments
#    1. CB Server URL
#    2. API Token for an account with permissions to create watchlists
#    3. A file containing python dictionariess, one dict per line, which contain at least one key/value pair
#        list_name: (required) the watchlist name as displayed in the UI
#        Additional key/value pairs will be ignored, this script can use the
#           same input file used by whitelist_add.py

import sys,struct,socket,pprint,argparse,warnings
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')
import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Add a watchlist")

    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_argument("-w", "--watchlistsource", action="store", default=None, dest="wls",
                      help="File containing watchlists to import.")
    return parser

def main():
    parser = build_cli_parser()
    opts = parser.parse_args()
    if not opts.url or not opts.token or not opts.wls:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)
    
    # build a cbapi object
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=False)
    
    #get existing whatchlists
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        current_watchlist = cb.watchlist()
    
    wl_dict = {}
    #iterate over current watchlists, add names of existing watchlists to a list
    if type(current_watchlist) is list:
        for p in current_watchlist:
            wl_dict[p['name']] = p['id']
    elif type(current_watchlist) is dict:
        wl_dict[current_watchlist['name']] = current_watchlist['id']
    
    f = open(opts.wls, 'r')
    for line in f:
        lt = eval(line)
        opts.name = lt['list_name']

        #compare name of the new watchlist to the list of current watchlists
        if opts.name in wl_dict.keys():
            #if new name exists delete the watchlist
            print "Deleting watchlist |||| ", opts.name
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                watchlist = cb.watchlist_del(wl_dict[opts.name])
        else:
            # the watchlist name does not exist, print below message
            print "Watchlist with name does not exist, skipping deleting of watchlist |||| ", opts.name

if __name__ == "__main__":
    sys.exit(main())
