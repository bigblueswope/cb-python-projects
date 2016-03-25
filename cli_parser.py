__author__ = 'BJSwope'
import argparse

def build_cli_parser():
    parser = argparse.ArgumentParser(description="Performs a process search. Returns desired fields as a list.")

    # for each supported configuration option, add an option
    #
    parser.add_argument("-c", "--cburl", action="store", default="https://192.168.230.201", dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    # cb url defaults to my demo vm on my laptop
    parser.add_argument("-a", "--apitoken", action="store", default="fe067f2792a5cf36e1486c4467dd2c473e0990f6", dest="token",
                      help="Carbon Black API Authentication Token")
    # the default api token is only valid on my demo vm on my laptop
    parser.add_argument("-s", "--ssl-verify", action="store_true", default=False, dest="ssl_verify",
                      help="SSL Verification. Default = Do not verify. To verify the server's certificate use this argument by itself")
    parser.add_argument("-t", "--facets_enable", action="store_true", default=False, dest="facet_enable",
                      help="By default results facets are disabled to return faster results. Use this argument, by itself, to turn facets on")
    parser.add_argument("-l", "--listfields", action="store_true", default=None, dest="list_fields",
                      help="To get a list of available fields to that may be use with the \"-f\" argument, use this flag.")
    parser.add_argument("-r", "--rows", action="store", default=20, dest="rows", type=int,
                      help="Number of rows to be returned.  Default = 20")
    parser.add_argument("-f", "--fields", action="append", default=[], dest="fields", type=str,
                      help="Field(s) to be returned.  For multiple fields, use this option multiple times.")
    parser.add_argument("-q", "--query", action="store", default=None, dest="query",
                      help="process query ex. hostname:foo and netconn:45.21.30.115")
    parser.add_argument("-m", "--md5", action="store", default=None, dest="md5",
                      help="MD5 of the binary we are interested in.")
    args = parser.parse_args()
    return args
