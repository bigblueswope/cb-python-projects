#!/bin/env python

keepers = ['cat', 'cfp1', 'cs1', 'cs3', 'destinationDnsDomain', 'fileHash', 'fileType', 'fname', 'request', 'start']

with open('example.txt','r') as infile:
    for line in infile:
        d = {}
        fields = line.split('|')
        for field in fields:
            field = field.strip(' \t\n\r')
            try:
                k,v = field.split('=', 1)
                if k in keepers :
                    d[k] = v
                print "%s ** %s" % (k,v)
            except:
                pass
        print ''
        if d['fileType'] == 'pe':
            print d
