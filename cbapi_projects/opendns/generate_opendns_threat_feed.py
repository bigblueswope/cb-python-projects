#!/bin/env python

import os,zipfile, csv, collections, time, requests, json, pprint, hashlib, datetime

requests.packages.urllib3.disable_warnings()

# The URL on the next line should point to the location where you host the customized threat feed
#  For the first run, drop the 'default' opendns_threat_feed.json that came with this script into 
#    the location.
r = requests.get('http://192.168.230.202/custom_feeds/opendns_threat_feed.json')
s = json.loads(r.text)

#build a nested dictionary
#  outer dict keyed upon the Destination Domain reported from OpenDNS
#  inner dict keys are the various components of a Threat Report
new_domains = collections.defaultdict(lambda: collections.defaultdict(int))

#expiration dates: if a threat report is older than m90, we will set the IOCs to empty
#   if the threat report is older than m120, we will delete the entire report
m90 = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%s')
m120 = (datetime.datetime.now() - datetime.timedelta(days=120)).strftime('%s')

# To pull additional domains from the OpenDNS csv file add the category to this list
interesting_categories = ['Botnet', 'ShoeLaces', 'AnotherDummyCategory']

# securityActivity.zip is the zip file OpenDNS will send every day with the csv in it
a = zipfile.ZipFile('securityActivity.zip')
# securityActivity.csv is the report listing all the domains that were blocked.
b = a.open('securityActivity.csv', 'r') 
for row in csv.DictReader(b):
    if row['Categories'] in interesting_categories:
        # Based upon the Date/Time in the OpenDNS csv, calculate the seconds since the Unix epoch
        #   This will be used as the timestamp in the Threat Report for this domain.
        c = row['Date'] + " " + row['Time']
        epoch = int(time.mktime(time.strptime(c, '%Y-%m-%d %H:%M:%S')))
        
        new_domains[row['Destination']]['title'] = row['Categories']
        #the report id will be the md5 of the domain name
        new_domains[row['Destination']]['id'] = hashlib.md5(row['Destination']).hexdigest()
        new_domains[row['Destination']]['score'] = 100
        new_domains[row['Destination']]['link'] = 'https://investigate.opendns.com/domain-view/name/%s/view' % (row['Destination'])
        new_domains[row['Destination']]['iocs'] = {}
        new_domains[row['Destination']]['iocs']['dns'] = []
        new_domains[row['Destination']]['iocs']['dns'].append(row['Destination'])
        
        #if the because the OpenDNS csv will have multiple occurences of the same domain, use the most recent timestamp
        if new_domains[row['Destination']]['timestamp'] >= epoch:
            pass
        else:
            new_domains[row['Destination']]['timestamp'] = epoch
       
a.close()

# Move zipfile to zipfile_todays_date
now = datetime.datetime.now()
now = now.strftime("%Y%m%d_%H%M%S")
new_name = "securityActivity_%s.zip" % now
os.rename("securityActivity.zip", new_name)


#create a list index so we can track which item from the threat reports we are working on and updating
l_index = 0

#iterate over the existing threat reports 
for i in s['reports']:
    #iterate over the domains we picked up from the latest OpenDNS report
    for j in new_domains.keys():
        # if the threat feed already has this a report for this domain, update the timestamp
        if i['id'] == new_domains[j]['id']:
            i['timestamp'] = new_domains[j]['timestamp']
            # the domain already exists in the threat feed so we will delete it from the new domains dict
            new_domains.pop(j,None)
    
    #Commenting out the below section because it may not actually have an effect. From what I'm told we don't delete threat reports, ever.
    '''
    #delete reports that havent updated in 90 days
    # according to https://github.com/carbonblack/cbfeeds increment the timestamp and remove IOCs to have the report deleted
    if i['timestamp'] <= m90:
        # increment timestamp so the threat feed will recognize the report is updated
        s['reports'][l_index]['timestamp'] = i['timestamp'] + 1
        # delete the IOC
        s['reports'][l_index]['iocs'] = {}
    
    # If the report is over 120 days old, in theory it has been marked for deletion for 30 days and should be out of the feed on the CB server
    #  So we are just going to completely whack the entry from the opendns_threat_feed.json
    if i['timestamp'] <= m120:
        s['reports'][l_index].pop()
    '''
    #increment the list index
    l_index += 1

# any domains remaining in the new domains dict did not match an existing threat report so lets append its data to the threat feed
for j in new_domains.keys():
    s['reports'].append(new_domains[j])
    
# This is the out file to which we will write the threat feed
# Change this path to match your web server's directory where the file will be hosted
with open('/var/www/html/custom_feeds/opendns_threat_feed.json', 'w') as outfile:
    json.dump(s, outfile)

#this is a random comment to test git with
