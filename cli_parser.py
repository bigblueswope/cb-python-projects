__author__ = 'BJSwope'
import argparse

def build_cli_parser():
    parser = argparse.ArgumentParser(description="This script does something with the CB API.")

    # for each supported configuration option, add an option
    
    # cb url defaults to my demo vm on my laptop
    parser.add_argument("-c", "--cburl", action="store", default="https://192.168.230.201", dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    
    # the default api token is only valid on my demo vm on my laptop
    parser.add_argument("-a", "--apitoken", action="store", default="fe067f2792a5cf36e1486c4467dd2c473e0990f6", dest="token",
                      help="Carbon Black API Authentication Token")
    
    # defaults ssl verification to false
    parser.add_argument("-s", "--ssl-verify", action="store_true", default=False, dest="ssl_verify",
                      help="SSL Verification. Default = Do not verify. To verify the server's certificate use this argument by itself")
    
    # disables facets by default
    parser.add_argument("-t", "--facets_enable", action="store_true", default=False, dest="facet_enable",
                      help="By default results facets are disabled to return faster results. Use this argument, by itself, to turn facets on")
   
    # some scripts can be run with -l to print a list of all available fields
    parser.add_argument("-l", "--listfields", action="store_true", default=None, dest="list_fields",
                      help="To get a list of available fields to that may be use with the \"-f\" argument, use this flag.")
    
    # how many rows to return with the query
    parser.add_argument("-r", "--rows", action="store", default=20, dest="rows", type=int,
                      help="Number of rows to be returned.  Default = 20")
    
    # list of fields that will be printed when the results are returned
    parser.add_argument("-f", "--fields", action="append", default=[], dest="fields", type=str,
                      help="Field(s) to be returned.  For multiple fields, use this option multiple times.")
    
    # for scripts that require a query use this flag to specify the query
    parser.add_argument("-q", "--query", action="store", default=None, dest="query",
                      help="process query ex. hostname:foo and netconn:45.21.30.115")
    
    # for scripts that require an MD5 use this flag to specify the MD5
    parser.add_argument("-m", "--md5", action="store", default=None, dest="md5",
                      help="MD5 of the binary we are interested in.")
    
    # for scripts that require a sensor id use this flag to specify the sensor id
    parser.add_argument("-e", "--sensor", action="store", default=None, dest="sensor",
                      help="ID of sensor for which we search.")
    
    # for scripts that need a feed id use this flag to specify the feed id
    parser.add_argument("-i", "--id", action="store", default=None, dest="feedid",
                      help="Id of feed of which the specified report is a part of")
    
    # for scripts that need a report id use this flag to specify the report id
    parser.add_argument("-R", "--reportid", action="store", default=None, dest="reportid",
                      help="Id of report to query; this may be alphanumeric")
    
    # for scripts that will parse a URL to use components of the URL use this flag to specify that string to parse
    parser.add_argument("-p", "--parse_string", action="store", default=None, dest="parse_string"
                        help="A string to be parsed by the script")
    
    # Used Flags:
    # a c e f i l m q p r R s t 

    args = parser.parse_args()
    
    return args
