#!/usr/bin/env python

import pprint
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

url = 'https://api5.conferdeploy.net/integrationServices/v3/event?applicationName=powershell.exe&rows=1000&searchWindow=2w'
headers = {'X-Auth-Token': 'thelongone/theshortone'}
r = requests.get(url, headers=headers)
foo = r.json()

hashes = {}
appNames = {}

'''
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(foo['results'][0])
'''

for bar in foo['results']:
	sha256Hash = bar['selectedApp']['sha256Hash']
	if sha256Hash in hashes.keys():
		hashes[sha256Hash] += 1
	else:
		hashes[sha256Hash] = 1
	#print bar['selectedApp']['applicationName'], bar['selectedApp']['sha256Hash']

print "Powershell Hashes and Count of Occurences"
for k in hashes.keys():
	print k + " = " + str(hashes[k])

for j in hashes.keys():
	url = 'https://api5.conferdeploy.net/integrationServices/v3/event?sha256hash=%s&rows=1000&searchWindow=2w' % (j)
	r = requests.get(url, headers=headers)
	foo = r.json()
	for bar in foo['results']:
		if bar['selectedApp']['sha256Hash'] in hashes.keys():
			appName = bar['selectedApp']['applicationName']
			if appName in appNames.keys():
				appNames[appName] +=1
			else:
				appNames[appName] = 1

print ""
print "Application Names and Count of Occurrences"
for k in appNames.keys():
	print k + " = " + str(appNames[k])
