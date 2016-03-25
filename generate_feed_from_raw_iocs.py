#!/bin/env python

# stdlib imports
import re, sys, time, urllib, json, socket, base64, hashlib, ConfigParser, os
  
# cb imports
from cbfeeds import CbReport
from cbfeeds import CbFeed
from cbfeeds import CbFeedInfo

def gen_report_id(iocs):
    """
    a report id should be unique
    because generate_feed_from_raw may be run repeatedly on the same data, it should
    also be deterministic.
    this routine sorts all the indicators, then hashes in order to meet these criteria
    """
    md5 = hashlib.md5()

    # sort the iocs so that a re-order of the same set of iocs results in the same report id
    iocs.sort()

    for ioc in iocs:
        md5.update(ioc.strip())

    return md5.hexdigest()

def build_reports(options):
    reports = []
    ips = []
    domains = []
    md5s = []
  
    # read all of the lines (of text) from the provided input file (of IOCs)
    raw_iocs = open(options['ioc_filename']).readlines()
    
    # iterate over each of the lines attempt to determine if each line is a suitable ipv4 address, dns name, or md5
    for raw_ioc in raw_iocs:
        
        # strip off any leading or trailing whitespace skip any empty lines 
        raw_ioc = raw_ioc.strip()
        if len(raw_ioc) == 0:
            continue
        
        try:
            # attempt to parse the line as an ipv4 address 
            socket.inet_aton(raw_ioc)
            # parsed as an ipv4 address!
            ips.append(raw_ioc)
        except Exception, e:
            # attept to parse the line as a md5 and, if that fails, as a domain.  use trivial parsing
            if 32 == len(raw_ioc) and re.findall(r"([a-fA-F\d]{32})", raw_ioc):
                md5s.append(raw_ioc)
            elif -1 != raw_ioc.find("."):
                domains.append(raw_ioc) 

    fields = {'iocs': {
                      },
              'timestamp': int(time.mktime(time.gmtime())),
              'link': options['feed_provider_url'],
              'title': options['report_name'],
              'id': gen_report_id(ips + domains + md5s),
              'score': 100}
   
    if options['report_tags'] : 
        fields['tags'] = options['report_tags'].split(',')
    
    if len(ips) > 0:
        fields['iocs']['ipv4'] = ips
    if len(domains) > 0:
        fields['iocs']['dns'] = domains
    if len(md5s) > 0:
        fields['iocs']['md5'] = md5s

    reports.append(CbReport(**fields))

    return reports

def create_feed(options):
   
    # generate the required feed information fields based on command-line arguments
    feedinfo = {'name': options['feed_name'],
                'display_name': options['feed_display_name'],
                'provider_url': options['feed_provider_url'],
                'summary': options['feed_summary'],
                'tech_data': options['feed_tech_data']}
   
    # if an icon was provided, encode as base64 and include in the feed information 
    if options['feed_icon']:
        bytes = base64.b64encode(open(options['feed_icon']).read())
        feedinfo['icon'] = bytes 
    
    # if a small icon was provided, encode as base64 and include in the feed information
    if options['feed_small_icon'] :
        bytes = base64.b64encode(open(options['feed_small_icon']).read())
        feedinfo['icon_small'] = bytes
  
    # if a feed category was provided, include it in the feed information
    if options['feed_category']:
        feedinfo['category'] = options['feed_category']
 
    # build a CbFeedInfo instance this does field validation    
    feedinfo = CbFeedInfo(**feedinfo)
   
    # build a list of reports (always one report in this case).  the single report will include all the IOCs  
    reports = build_reports(options)
   
    # build a CbFeed instance this does field validation (including on the report data) 
    feed = CbFeed(feedinfo, reports)

    return feed.dump()

def get_options(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s <config_file_defining_threat_feed>\n' % sys.argv[0])
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        sys.stderr.write('ERROR: Configuration file %s was not found!\n' % sys.argv[1])
        sys.exit(1)

    config = ConfigParser.SafeConfigParser()
    config.read(sys.argv[1])
    options = {}
    for section in config.sections():
        if section == 'Required':
            for name,value in config.items(section):
                if value == '':
                    print "Config file missing a value for the required options.  Edit config file and retry."
                    print "Required Options:"
                    for name,value in config.items(section):
                        print name
                    sys.exit(1)
        options.update(get_options(section))
    
    custom_threat_feed = create_feed(options)
    if options['output_file']:
        with open(options['output_file'], 'w') as outfile:
            outfile.write(custom_threat_feed)
    else:
        print custom_threat_feed
