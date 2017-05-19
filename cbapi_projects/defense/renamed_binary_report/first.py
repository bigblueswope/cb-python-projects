#!/usr/bin/env python

import pprint
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

hashes = {}
appNames = {}

pp = pprint.PrettyPrinter(indent=4)
'''
pp.pprint(foo['results'][0])
'''

def parse_return(r):
	if r.status_code == 200:
		foo = r.json()
		return foo
	elif r.status_code == 400:
		foo = r.json()
		if foo['message']:
			print foo['message']
		elif foo['messages']:
			print foo['messages']
		sys.exit(0)
	elif r.status_code == 401:
		print "Authentication failed.  Check the contents of X-Auth-Token"
		sys.exit(0)
	elif r.status_code == 429:
		print "Rate limit hit.  Try again later."
		sys.exit(0)
	elif r.status_code == 500:
		print "Server error by Cb Defense."
		foo= r.json()
		if foo['message']:
			print foo['message']
		elif foo['messages']:
			print foo['messages']
		sys.exit(0)
	else:
		foo=r.json()
		print "Unexpected HTTP response."
		pp.pprint(foo)
		sys.exit(0)

url = 'https://api5.conferdeploy.net/integrationServices/v3/event?applicationName=powershell.exe&rows=1000'
headers = {'X-Auth-Token': 'thelongone/theshortone'}
r = requests.get(url, headers=headers)

foo = parse_return(r)

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
	print j
	url = 'https://api5.conferdeploy.net/integrationServices/v3/event?sha256hash=%s&searchWindow=2w' % (j)
	print url
	r = requests.get(url, headers=headers)
	foo = parse_return(r)
	for bar in foo['results']:
		pp.pprint(bar['selectedApp'])
		if bar['selectedApp']['sha256Hash'] in hashes.keys():
			print "==" * 80
			pp.pprint(bar)
			#print "<<<< Process Details >>>>"
			#pp.pprint(bar['processDetails'])
			#print ">>>> Selected App <<<<"
			#pp.pprint(bar['selectedApp'])
			appName = bar['selectedApp']['applicationName']
			if appName in appNames.keys():
				appNames[appName] +=1
			else:
				appNames[appName] = 1

print ""
print "Application Names and Count of Occurrences"
for k in appNames.keys():
	print k + " = " + str(appNames[k])
