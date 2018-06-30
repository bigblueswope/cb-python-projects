#!/usr/bin/env python
# A script to parse the Emerging Threats FW IP Block List
# bj@bit9.com
# 2015-10-03

import sys, os, re, string

# third party lib imports
# Uses David Moss' netaddr python library for manipulating subnets
# https://pythonhosted.org/netaddr/index.html
import netaddr

hash_start = re.compile('^#') 
input=open(sys.argv[1], 'r')

for line in input:
    #strip the \n from the line
    line = line.strip()
    #use regex search to determine if line starts with a #
    if re.search(hash_start, line):
        #drop the leading # and strip the any leading spaces that remain
        # the last hash line will identify which section of the ET feed we are parsing and will be used to annotate stuff in threat feed
        last_hash_line = line[1:].strip()
        print last_hash_line
    else:
        # if the line contains an IP address then it will split to 4 items
        if len(string.split(line, '.')) == 4:
            try:
                # lines with a subnet break out the IP and subnet mask
                addr,subnet = string.split(line, '/')
            except:
                # lines without a subnet mean individual IPs which implies a 32 bit subnet mask
                addr = line
                subnet = 32
            
            # production set this to 21, meaning the entry has > 1000 hosts so we will use this entry as a query based threat feed
            if int(subnet) < 25:
                net = netaddr.IPNetwork(line)
                net_bottom = net.first - 4294967296 
                net_top =  net.last - 4294967296
                ip_query = ''.join(['q=ipaddr%3A%5B', str(net_bottom), '%20TO%20', str(net_top), '%5D'])
                print ip_query
