## Sensor monitor
#  Author: Jon Ross, jross@bit9.com
#  Version 0.1
#
#  Purpose: Alert on Carbon Black sensors that are offline more than a 
#  certain period of time (default: 1 day).  Alerts are sent to syslog
#  in /var/log/cb/notifications/cb-notifications-sensormonitor.log
#
#  Variables that MUST be modified to match your environment
#  SERVER_IP : Set this to the IP address of your Carbon Black server
#  API_TOKEN : Used for authentication, set this to the API token of the user
#              in Carbon Black that will make the request.
#
#  Variables that you MAY change if you prefer
#  DELTATIME : The amount of time (IN SECONDS) that is too long for a sensor
#              to remain offline.  Default is 86400 seconds (1 day).
##

################### EDIT THESE VALUES TO MATCH YOUR SERVER ###################

SERVER_IP = '192.168.230.40'
API_TOKEN = '11f8e14d1d98469468b962f494885fbef9e16cc5'
DELTATIME = 86400

################### DO NOT MODIFY BELOW THIS LINE ############################


import cbapi
import datetime
import syslog

syslog.openlog('cb-notifications-sensormonitor')
CarbonBlackUrl = "https://" + SERVER_IP

c = cbapi.CbApi(CarbonBlackUrl, ssl_verify=False, token=API_TOKEN)

query = "%s/api/v1/sensor" % c.server

results = c.session.get(query, headers=c.token_header, verify=c.ssl_verify)
results = results.json()

for host in results:
	# verify that a sensor is both offline and not marked for uninstall
	if host['status'] == 'Offline' and host['uninstall'] != True:
		#chopping 6 characters off to remove tz because my python doesn't like utc offset tz format
		lct = host['last_checkin_time'][:len(host['last_checkin_time'])-6]
		lct = datetime.datetime.strptime(lct,"%Y-%m-%d %H:%M:%S.%f")
		deltaTime = datetime.datetime.now() - lct
		# report if offline for a day or more
		maxDrift = datetime.timedelta(seconds=DELTATIME)
		if deltaTime > maxDrift:
			syslog.syslog(syslog.LOG_WARNING,'Carbon Black sensor %s has not checked in for %s' % (host['computer_dns_name'],deltaTime))

syslog.closelog()
