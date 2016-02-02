import sys, struct, socket, pprint, argparse, warnings

# in the github repo, cbapi is not in the example directory
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')

import cbapi 

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Pull md5, ip and domain information")

    # for each supported output type, add an option
    #
    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_argument("-n", "--no-ssl-verify", action="store_false", default=False, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    return parser

def main():
    
    # parse command line arguments
    #
    parser = build_cli_parser()
    opts = parser.parse_args()
    if not opts.url or not opts.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=opts.ssl_verify)

    # retrieving large result sets requires paging
    # the 'rows' variable controls the page size
    #
    start = 0
    rows = 250 

    md5s = set()
    ips = set()
    domains = set()

    # extract all md5s from the binary index (cbmodules)
    # this is equivalent to the "Search Binaries" capability
    # in the web ui
    #
    while True:

        # perform an unqualified search of the binary index,
        # paging as necessary
        #
        # an empty query string (first parameter) maps to a
        # raw SOLR query of *:*
        #
        binaries = cb.binary_search('', start=start, rows=rows)

        # if no results were found, the search is complete
        #
        if len(binaries['results']) < 1:
            break

        # iterate over the result set, extracting just the md5
        #
        for binary in binaries['results']:
            md5s.add(binary['md5'])
            pass
       
        # update the start row requested for the next iteration
        # 
        start = start + rows

    start = 0
    rows = 250 

    # iterate over all process documents that have at least one netconn
    # event.  this search returns documents from the 'cbevents' index,
    # and is equivalent to the "search processes" functionality in the
    # web ui
    #
    # the process search returns various properties of the process described
    # by each process document, such as the process name, the command line,
    # and the count of various event types.  it does not return the raw event
    # data itself
    #
    # as written, this logic provides an inefficient mechanism of identifying
    # all of the unique IPs and domains.  this could be more performantly
    # accomplished via targeted use of SOLR's term component.  CB API exposure
    # of this component is on the way...
    #
    while True:

        # perform the process search, restricting results to only those that 
        # include at least one netconn event
        #
        processes = cb.process_search('netconn_count:[1 to *]', start=start, rows=rows)

        # if no results were found, the search is complete
        #
        if len(processes['results']) < 1:
            break

        # iterate over the process document result set
        # for each process document, we can query for the netconn events
        # and extract the corresponding IP and domain names
        #
        for process in processes['results']:

            # query the server for the full event set for the process
            # identified via search. 
            #
            # this event set includes netconn events
            #
            events = cb.process_events(process['id'], process['segment_id'])

            # iterate over each netconn event in the process document
            #
            for netconn in events['process']['netconn_complete']:
           
                # the netconn event format is a single string with six fields, with a | delimiter
                # the fields are as follows:
                # 
                # <!-- NETCONNS - expected to be "(TIME) | (IP) | (PORT) | (PROTOCOL) | (domain) | (direction)" -->
                # <!--                            2013-02-08 14:44:06.000000|460258477|20480|1|facebook.com|1 -->
                #
                # split the netconn event into individual fields, validating that
                # six and only six fields are present
                #
                netconn_fields = netconn.split('|')
                if len(netconn_fields) != 6:
                    continue

                # extract the ip field (32bit unsigned int representation of the IPv4
                # address) and convert to a string represenation of the IP
                # 
                # the IP may be missing in certain cases, most notably a web proxy scenario
                # 
                ip = netconn_fields[1]
                if len(ip) > 0:
                    try:
                        ip = socket.inet_ntoa(struct.pack("!i", int(ip)))
                        ips.add(ip)
                    except Exception, e:
                        pass 

                # extract the domain field
                #
                # the domain name field may be missing in certain cases, most notably
                # when the connection was made directly to an IP
                #
                domain = netconn_fields[4]
                if len(domain) > 0:
                    domains.add(domain)
                
        start = start + rows

        print start 

    print "# %-10s | %s" % ('IOC', 'Count')
    print "# %-10s + %s" % ('-' * 10, '-' * 10)
    print "# %-10s | %s" % ('md5', len(md5s))
    print "# %-10s | %s" % ('ipv4', len(ips))
    print "# %-10s | %s" % ('domain', len(domains))
    print "# %-10s + %s" % ('-' * 10, '-' * 10)

    for md5 in md5s:
        print md5
    for ip in ips:
        print ip
    for domain in domains:
        print domain

if __name__ == "__main__":
    sys.exit(main())
