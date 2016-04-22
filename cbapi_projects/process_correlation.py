#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, warnings, pprint, requests
from collections import defaultdict
from cli_parser import build_cli_parser

requests.packages.urllib3.disable_warnings()

import cbapi 

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    args.query='process_name:notepad.exe hostname:W7-low'
    args.rows = 100
    
    processes = cb.process_search_iter(args.query, rows=args.rows, facet_enable=args.facet_enable)

    d = defaultdict(lambda: defaultdict(int))

    # for each result 
    for p in processes:
        h = p['hostname']
        #convert hour to seconds
        a = int(p['start'][11:13]) * 3600
        #covert minutes to seconds
        b = int(p['start'][14:16]) * 60
        #sum them and declare it a string so we can use it as a dictionary key
        s=str(a+b)
        #dictonary of hosts whose value is a dictionary of start times, in seconds, whose value is the count of processes started in that minute
        d[h][s] +=1
    
    for host in d.keys():
        print host, d[host]
        print ""
        time_list = []
        #k is the string representing the process' start time which we convert to in integer so we can compare it to a range of integers
        for k in sorted(d[host].keys()):
            time_list.append(int(k))
        
        already_used_to_trigger = []
        
        for t in sorted(time_list):
            if t in already_used_to_trigger:
                continue
            range_min = t - 900
            range_max = t + 901
            # r is a list containing the integers representing the 30 minutes surrounding the start time of the process
            r = range(range_min, range_max, 60)
           
            proc_count = 0
            
            in_both = set(time_list).intersection(r)
            
            for i in sorted(in_both):
                hour = (i/3600)
                minute = ((i % 3600)/60)
                #print "%02d:%02d = %d" % (hour, minute, d[host][str(i)])
                proc_count += d[host][str(i)]
            
            if proc_count >= 3:
                for x in in_both:
                    already_used_to_trigger.append(x)
                
                print host + ' had %s instances of the notepad.exe within 30 minutes of %02d:%02d' % (proc_count, hour, minute)
                
        

if __name__ == "__main__":
    sys.exit(main())

