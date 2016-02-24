import sys, struct, socket, pprint, argparse, time, datetime, warnings
# in the github repo, cbapi is not in the example directory
# if cbapi.py is local then comment out the sys.path.append statement
sys.path.append('../../cbapi/client_apis/python/src/cbapi/')
import cbapi


def build_cli_parser():
    parser = argparse.ArgumentParser(description="Lists the fields available when querying sensor data.")
    # for each supported output type, add an option
    #
    parser.add_argument("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., https://127.0.0.1 ")
    parser.add_argument("-a", "--apitoken", action="store", default=None, dest="token",
                      help="Carbon Black API Authentication Token")
    parser.add_argument("-s", "--ssl-verify", action="store_true", default=False, dest="ssl_verify",
                      help="SSL Verification. Default = Do not verify")
    return parser


def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if not args.url or not args.token:
        print "Missing either server URL or Authentication Token; run with --help for usage"
        sys.exit(-1)

    # build a cbapi object
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # enumerate sensors
        sensors = cb.sensors()

    print "List of fields available to be returned by a sensor search:"
    unique_field_names = []
    for k in sensors[1]:
        if k not in unique_field_names:
            unique_field_names.append(k)
    for l in sorted(unique_field_names):
        print l
    sys.exit(0)
   
    
if __name__ == "__main__":
    sys.exit(main())

