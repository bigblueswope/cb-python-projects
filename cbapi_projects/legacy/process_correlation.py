#!/bin/env python

# First attempt at a script to correlate processes across time
# 

__author__ = 'BJSwope'
import sys, argparse, warnings, pprint, requests
from collections import defaultdict
from cli_parser import build_cli_parser

requests.packages.urllib3.disable_warnings()

import cbapi 

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    # Sample query looks for notepad on one of my lab machines.  Because this is not constrained to a single day
    #   it will pull every instance of notepad for the life of my data (which means a notepad run 2 months ago
    #   at 1:05 PM and a notepad run yesterday at 1:10 PM would be correlated, albeit incorrectly, but we want
    #   this behavior for testing purposes.
    args.query='process_name:notepad.exe hostname:W7-low'
    
    #pull data back in chunks of 100 instead of the default chunks of 10
    args.rows = 100
    
    processes = cb.process_search_iter(args.query, rows=args.rows, facet_enable=args.facet_enable)

    # build a nested dictionary
    # outer dict will key on the hostname
    # inner dictionary will key upon the start time, converted to seconds since midnight, with a resolution of 1 minute
    d = defaultdict(lambda: defaultdict(int))

    # for each result 
    for p in processes:
        h = p['hostname']
        #convert hour to seconds
        a = int(p['start'][11:13]) * 3600
        #covert minutes to seconds
        b = int(p['start'][14:16]) * 60
        # not parsing for seconds because per-second resolution would increase our workload 60 fold without any measurable benefit
        #sum them and declare it a string so we can use it as a dictionary key
        s=str(a+b)
        #dictonary of hosts whose value is a dictionary of start times, in seconds, whose value is the count of processes started in that minute
        d[h][s] +=1
    
    #for each host who has run notepad.exe
    for host in d.keys():
        # time_list will contain the integer values of the process start times
        time_list = []
        #k is the string representing the process' start time which we convert to in integer so we can compare it to a range of integers
        for k in sorted(d[host].keys()):
            # time_list contains the start time for every notepad that has run
            time_list.append(int(k))
        
        # This list will be used to track start times that have already been used to trigger an alert so that they are not used again.
        already_used_to_trigger = []
        
        # for every start time in the list of start times
        for t in sorted(time_list):
            # if the start time has already been used to tigger an alert, no need to re-trigger on it.
            if t in already_used_to_trigger:
                continue
            
            range_min = t - 900  # 15 minutes before the start time of the process we are analyzing
            range_max = t + 901  # 15 minutes after the start time of the process we are analyzing
            
            # r is a list containing the integers representing the 30 minutes surrounding the start time of the process
            r = range(range_min, range_max, 60)
           
            #count of processes inside the 30 minute window
            proc_count = 0
            
            # processes from the time_list that fall within the 30 minute range surrounding the process we are analyzing
            in_both = set(time_list).intersection(r)
            
            for i in sorted(in_both):
                hour = (i/3600)
                minute = ((i % 3600)/60)
                
                # d[host][str(i)] will be an integer representing how many times the process was started within the minute
                proc_count += d[host][str(i)]
            
            # for our testing purposes, if we see more than 3 notepad processes launched in 30 minutes, take action.
            if proc_count >= 3:
                # take all the start times that just triggered an alert, and put them in the list to prevent further alerts
                for x in in_both:
                    already_used_to_trigger.append(x)
                
                print host + ' had %s instances of the notepad.exe within 30 minutes of %02d:%02d' % (proc_count, hour, minute)
                
        

if __name__ == "__main__":
    sys.exit(main())

