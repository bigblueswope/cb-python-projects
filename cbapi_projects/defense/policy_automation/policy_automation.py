#!/usr/bin/env python

import sys
import csv
import re
import argparse
import json
import pprint
import collections
try:
	import requests
except ImportError as e:
	print "It appears that you do not have the required Python module 'requests' installed."
	print "Try running the following command to install 'requests'"
	print "	sudo pip install requests --upgrade"
	sys.exit(0)

import policy_components
import policy_framework as policy

pp = pprint.PrettyPrinter(indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="Action to be taken.  Valid values: export_json,import_csv,import_json,transfer", required=True)
parser.add_argument("-i", "--input", help="File containing rules or policy to import.")
parser.add_argument("-o", "--output", help="File to which to write policy JSON. Just in case you wish to verify the JSON.")
args = parser.parse_args()

apps = policy_components.applications
ops = policy_components.operations
actions = policy_components.actions

def data_validation_error(input_string, field_numb):
	print "CSV contains invalid data in field %i (printed below).  Fix data and try again." % (field_numb)
	print input_string
	sys.exit(1)

def app_match(input_string):
	for k in apps.keys():
		if input_string.startswith(k):
			return (apps[k]['type'], apps[k]['value'])
	#if we get to here, the 1st field on a line does not match our rule types.
	data_validation_error(input_string, 1)

def op_match(input_string):
	for k in ops.keys():
		if input_string.startswith(k):
			return (ops[k])
	#if we got to here, the 2nd field on a line does not match our rule operations.
	data_validation_error(input_string, 2)

def action_match(input_string):
	for k in actions.keys():
		if input_string.startswith(k):
			return (actions[k])
	#if we got to here, the 3rd field on a line does not match our rule actions.
	data_validation_error(input_string, 3)

def build_policy_from_csv(infile):
	rules_dict = {'rules': []}
	rule_id = 1

	with open (infile, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			rule = {'required': 'false', 'id': rule_id}
		
			app_dict = {}
			app_dict['type'], app_dict['value'] = app_match(row[0])
			if not app_dict['value']:
				adv = row[0].split(': ')[1]
				adv = re.sub('"', '', adv)
				app_dict['value'] = adv
				
			rule['application'] = app_dict.copy()
			rule['operation'] = op_match(row[1])
			rule['action'] = action_match(row[2])
			
			rules_dict['rules'].append(rule.copy())
			rule_id += 1

	dicts = [policy_components.av_config, policy_components.misc_config, policy_components.sensor_config, rules_dict]

	all_config = collections.defaultdict(dict)
	for d in dicts:
		for k, v in d.iteritems():
			all_config[k] = (v)

	if args.output:
		with open(args.output, 'w') as outfile:
			json.dump(all_config, outfile, indent=4, sort_keys=True)
	return all_config


def import_policy(insrc, intype):
	print "\n##### Begin Policy Import #####"
	session =requests.Session()
	host = policy.get_cbd_instance('DESTINATION')
	user, password = policy.get_username_password('DESTINATION')
	policyName = policy.get_policy_name(insrc)
	policyDescription = policy.get_policy_description()
	policyPriority = policy.get_policy_priority()
	policyPriorityLevel = policy.get_policy_priority_level()
	request_headers = policy.get_request_headers(host)
	request_headers['X-CSRF-Token'] = policy.login(session, user, password, host) 
	
	if intype == 'from_csv':
		jsonPolicy = build_policy_from_csv(insrc)
	elif intype == 'from_json_memory':
		jsonPolicy = insrc
	elif intype == 'from_json_file':
		with open(insrc, 'r') as f:
			jsonPolicy = json.load(f)
	else:
		print "Error:  Import Policy called for an unsupported format."
		sys.exit(1)
	
	formdata = {"name": policyName,
				"description": policyDescription,
				"priorityLevel": policyPriority,
				"priority": int(policyPriorityLevel),
				"sourceGroupId": None}

	print "Creating Policy: %s" % (policyName)
	uri = '/settings/groups/add'
	response = policy.web_post(session, host, uri, request_headers, formdata)

	policy.does_policy_exist(response)

	groupId = response['addedDeviceGroupId']
	print "Inserting configuration and rules into policy id:  %i" % (groupId)

	formdata = {"id": groupId,
				"origname": policyName,
				"name": policyName,
				"origdescription": policyDescription,
				"description": policyDescription,
				"priorityLevel": policyPriority,
				"origpriorityLevel": policyPriority,
				"adminVersion": False,
				"policy": jsonPolicy}

	uri = '/settings/groups/modify'
	policy.web_post(session, host, uri, request_headers, formdata)

	print "Policy Import completed. Logging out."
	uri = '/logout'
	policy.web_get(session, host, uri, request_headers)

def export_policy(exp_type):
	print "\n##### Begin Policy Export #####"
	session =requests.Session()
	host = policy.get_cbd_instance('SOURCE')
	user, password = policy.get_username_password('SOURCE')
	
	request_headers = policy.get_request_headers(host)
	request_headers['X-CSRF-Token'] = policy.login(session, user, password, host) 
	
	uri = '/settings/groups/list'
	response = policy.web_get(session, host, uri, request_headers)
	# Note: policy.web_get & policy.web_post both return a dict
	
	if response['success']:
		# creating a list of the policies from the target org
		menu_number = 0
		policies = collections.OrderedDict()
		pol_names = []

		for entry in response['entries']:
			policies[entry['name']] = {'orgId': entry['orgId'], 'id': entry['id']}
			pol_names.append(entry['name'])
		
		print "Policies Available for Export:"
		for key in policies.keys():
			print '%i) %s' % (menu_number, key)
			menu_number += 1
	
		pol_id = int(raw_input("Choose the number for your SOURCE Policy: "))
		if pol_id < menu_number:
			pol_name = pol_names[int(pol_id)]
			print "SOURCE Policy Name: %s" % (pol_name)
			groupId = policies[pol_name]['id']
			print 'SOURCE Policy ID: %i' % (groupId)
		else:
			print "Invalid SOURCE Policy choice received.  Rerun the script and retry."
			sys.exit(1)
	
	# we may want to add value to list ORG ID for CSR access and queries

	uri = '/settings/policy/%i/details' % (groupId)
	response = policy.web_get(session, host, uri, request_headers)
	# Note: policy.web_get & policy.web_post both return a dict
	if response['success']:
		jsonResponse = json.dumps(response['policy'], indent=4, sort_keys=True)
		if exp_type == 'to_json_file':
			if not args.output:
				print "No Output File Specified."
				outfile = raw_input("Specify output filename or just press 'Enter' to output to '%s.json': " % (pol_name))
				if outfile == '':
					outfile = pol_name + '.json'
			else:
				outfile = args.output
			with open(outfile, 'w') as outf:
				outf.write(jsonResponse)
		elif exp_type == 'to_json_memory':
			return response['policy']
		else:
			print "Export type not specified.  No data exported."


policy.check_request_version()
if args.action == 'export_json':
	export_policy('to_json_file')

elif args.action == 'import_csv':
	if not args.input:
		args.input = raw_input("No Input File Specified.\nWhat CSV contains the rules to import?: ")
	print "Using %s as rule source" % (args.input)
	import_policy(args.input, 'from_csv')

elif args.action == 'import_json':
	if not args.input:
		args.input = raw_input("No input file specified.\nWhat file contains the JSON policy to import?: ")
	print "Using %s as rule source" % (args.input)
	import_policy(args.input, 'from_json_file')

elif args.action == 'transfer':
	src_policy = export_policy('to_json_memory')
	import_policy(src_policy, 'from_json_memory')

else:
	print "Error: action was not one of 'export_json/import_csv/transfer'."
	print "Please rerun the script providing a correct action argument"

#Tests we should run:
#	export_json
#		with -o
#		without -o
#			accept pol name as outfile
#			not accept pol name as outfile
#	import_csv
#		with -i
#			accept filename as pol name
#			not accept filename as pol name
#		without -i
#			accept filename as pol name
#			not accept filename as pol name
#	import_json
#		with -i
#			accept filename as pol name
#			not accept filename as pol name
#		without -i
#			accept filename as pol name
#			not accept filename as pol name
#	transfer
#		same server
#			same org
#				keep dst pol name same: should fail
#				change dst pol name
#			diff org
#				keep dst pol name same
#				change dst pol name
#		diff servers
#			keep dst pol name same
#			change dst pol name
