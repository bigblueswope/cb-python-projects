#!/usr/bin/python
import sys
import time
import re
import json
import requests
import getpass
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def prettyPrint(entry):
	print json.dumps(entry, indent=4, sort_keys=True)

def check_request_version():
	req_ver = requests.__version__
	if req_ver != '2.14.2':
		print "WARNING: Your version of the Python module 'requests' is not the most up-to-date.\n\
If you have errors related to 'requests' upgrade to the latest version using:\n\t\
sudo pip install requests --upgrade"
		raw_input("Press 'Enter' to continue")

def get_cbd_instance(src_or_dst):
	host = raw_input("Please enter the ****%s*** CbD console URL\n(default is https://defense-prod05.conferdeploy.net): " % (src_or_dst))
	if len(host) == 0:
		host = "https://defense-prod05.conferdeploy.net"

	if host.startswith('http://'):
		host = re.sub('http://', 'https://', host)

	if not host.startswith('https://'):
		host = 'https://' + host
	return host

def get_username_password(src_or_dst):
	uname = raw_input("%s Username: " % (src_or_dst))
	if not uname:
		print "Error: Username cannot be blank. Rerun the script."
		sys.exit(1)
	pword = getpass.getpass("%s Password: " % (src_or_dst))
	if not pword:
		print "Error: Password cannot be blank. Rerun the script."
		sys.exit(1)
	return uname, pword

def get_policy_name(infile):
	if type(infile) == 'string':
		ppn = infile.split('.',1)[0]
		print "DESTINATION Policy Name: %s" % (ppn)
		pol_name = raw_input("Type you New Policy Name or just press 'Enter' to use '%s': " % (ppn))
		if not pol_name:
			pol_name = ppn
	else:
		pol_name = raw_input("DESTINATION Policy Name: ")
		if not pol_name:
			print "ERROR:  DESTINATION policy name cannot be blank.  Rerun the script and provide a name."
			sys.exit(1)
	
	return pol_name

def get_policy_description():
	pol_desc = raw_input("DESTINATION Policy Description: ")
	return pol_desc

def get_policy_priority():
	valid_pol_pris = ['LOW', 'MEDIUM', 'HIGH', 'MISSION_CRITICAL']
	pol_pri = raw_input("DESTINATION Policy Target Value: LOW MEDIUM HIGH MISSION_CRITICAL: [MEDIUM]")
	if len(pol_pri) == 0:
		pol_pri = "MEDIUM"
	if pol_pri in valid_pol_pris:
		return pol_pri
	else:
		print "Error:  %s is an invalid Policy Priority.  Valid Policy Priorities are:"
		for i in valid_pol_pris:
			print i
		sys.exit(1)

def get_policy_priority_level():
	#Nobody seems to know what this variable maps to
	#  Until we figure it out, I'm just hard setting it to 3
	#  If anybody ever says anything, just uncomment the next 3 lines
	#  And delete the on just below them.
	#ppl = raw_input("Policy Priority Level: [3] ")
	#if len(ppl) == 0:
	#	ppl = 3
	ppl = 3
	return ppl
	
def get_request_headers(host):
	referer = host + '/ui'
	request_headers = {
		'Host': host,
		'Origin': host,
		'Referer': referer
	}
	return request_headers

def login(session, user, password, host):
	request_headers = get_request_headers(host)
	formdata = {'forward': '', 'email': user, 'password': password}
	
	url = host + '/checkAuthStrategy'
	response = session.post(url, data=formdata, headers=request_headers, timeout=30)
	
	url = host + '/userInfo'
	response = session.get(url, data=formdata, headers=request_headers, timeout=30)
	
	if 'csrf' in response.json() and response.json()['csrf'] is not None:
		csrf = json.dumps(response.json()['csrf']).replace('"', '')
		return csrf
	else:
		print 'Error: No csrf record. Authentication failed'
		sys.exit(1)

def web_get(session, host, uri, request_headers):
	try:
		url = host + uri
		response = session.get(url, headers=request_headers, timeout=30)
	except Exception as e:
		print "GET request failed for the following URI: %s" % (uri)
		print "Exception: %s" % (e)
		sys.exit(1)
	try:
		return response.json()
	except Exception as e:
		pass
		
def web_post(session, host, uri, request_headers, formdata):
	try:
		url = host + uri
		response = session.post(url, json=formdata, headers=request_headers, timeout=30)
	except Exception as e:
		print "POST request failed for the following URI: %s" % (uri)
		print "Exception: %s" % (e)
		sys.exit(1)
	print "URL = " + url + "\nStatus = " + str(response.status_code)
	
	try:
		return response.json()
	except Exception as e:
		print "Exception: %s" % (e)
		
def does_policy_exist(jsonResponse):
	if jsonResponse['groupAlreadyExists'] is True:
		print "ERROR: A policy with this name already exists."
		print "Re-run the import and create a policy with a new name."
		sys.exit(1)

