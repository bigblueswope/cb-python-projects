#!/usr/bin/env python
import sys
import datetime
from cbapi.response.models import Binary, Process

from cbapi.example_helpers import build_cli_parser, get_cb_response_object
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

#list containing names of binaries we wish to find if being run after being renamed
watched_names = ['powershell.exe', 'notepad.exe', 'cmd.exe']

# a list of process names that can be used to exclude that process from the results
#  (Originally in script because I was querying for md5:<hash> instead of process_md5:<hash>
#	and that would return processes that had the hash in the mod_loads.)
#	Strictly speaking it probably is not needed, but I put it in so we can leave it just 
#	in case somebody might need the functionality.
ignored_names = []

def main():
	parser = build_cli_parser()
	parser.add_argument("--query", help="binary query", default='')
	args = parser.parse_args()

	cb = get_cb_response_object(args)
	for wn in watched_names:
		bq = "observed_filename:%s" % (wn)
		binaries = cb.select(Binary).where(bq)
		
		for binary in binaries:
			print("-" * 80)
			print "Filename: %s  Filehash: %s" % (wn, binary.md5sum)
			print("-" * 80)
			
			pq = "process_md5:%s" % (binary.md5)
			# to limit the search to the previous 24 hours
			# comment out the above query and uncomment out the below query
			#pq = "process_md5:%s start:-1440m" % (binary.md5)
			procs = cb.select(Process).where(pq)
			
			proc_names = {}
			for proc in procs:
				if proc.process_name in ignored_names :
					pass
				else:
					try:
						proc_names[proc.process_name] +=1
					except KeyError:
						proc_names[proc.process_name] = 1
			
			for k in sorted(proc_names.keys()):
				print k + " = " + str(proc_names[k])
		
			print('\n')

if __name__ == "__main__":
	sys.exit(main())
