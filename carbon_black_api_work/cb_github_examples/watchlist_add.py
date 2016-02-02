# This script requires 3 arguments
#    1. CB Server URL
#    2. API Token for an account with permissions to create watchlists
#    3. A file containing python dictionariess, one dict per line, which contain 3 key/value pairs
#        list_type: 2 possible values 'events' or 'modules'
#        list_name: the watchlist name to be displayed in the UI
#        list_query:  the watchlist's query

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
    
    wl_names = []
    #iterate over current watchlists, add names of existing watchlists to a list
    if type(current_watchlist) is list:
        for p in current_watchlist:
            wl_names.append(p['name'])
    elif type(current_watchlist) is dict:
        wl_names.append(current_watchlist['name'])
    
    f = open(opts.wls, 'r')
    for line in f:
        lt = eval(line)
        opts.type = lt['list_type']
        opts.name = lt['list_name']
        opts.query = lt['list_query']
        
        if not opts.query.startswith("q="):
            opts.query = "q=" + opts.query

        #compare name of the new watchlist to the list of current watchlists
        if not opts.name in wl_names:
            #if new name is does not exist add new watchlist
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                watchlist = cb.watchlist_add(opts.type, opts.name, opts.query)
            
            # print details of just added watchlist
            print "Watchlist created |||| " , opts.name
        else:
            # the new watchlist name already exists, print below message
            print "Watchlist with same name already exists, skipping adding of watchlist |||| ", opts.name

if __name__ == "__main__":
    sys.exit(main())
