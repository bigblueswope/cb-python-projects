#!/bin/env python
# A script to send an email for any Carbon Black sensors that have changed 
#  the state of their network isolation since the last running of this script.
# Run this script via a job scheduler, such as cron, to be notified 
#  when a sensor's network isolation state has changed.
# The script will track isolated sensors between runs via isolated_sensors.txt

__author__ = 'BJSwope'
import sys, argparse, pprint, warnings, smtplib, cbapi, json, collections

# cli_parser.py is the file I use to define my cb server and token 
# so I don't have to provide that info on every execution nor do 
# I have to include the info in every script.

from cli_parser import build_cli_parser
from email.mime.text import MIMEText


def send_mail(sensor):
    mail = {}
    if sensor['network_isolation_enabled'] == True: 
        if sensor['is_isolating'] == True:
            print "Sending enabled and active email."
            msg="Network Isolation enabled and active!\r\n Host: %s\r\nCarbon Black Console: %s\r\n Last Check-In Time: %s\r\n" \
            % (sensor['computer_name'], sensor['url'], sensor['last_checkin_time'])
            msg = MIMEText(msg)
            msg['Subject'] = 'Host Isolation Activated By Carbon Black'
        else:
            print "Sending enabled but not active email."
            msg="Network Isolation enabled and will activate at next sensor check in.\r\n Host: %s\r\nCarbon Black Console: %s\r\n Last Check-In Time: %s\r\nNext Check-In Time: %s" \
            % (sensor['computer_name'], sensor['url'], sensor['last_checkin_time'], sensor['next_checkin_time'])
            msg = MIMEText(msg)
            msg['Subject'] = 'Host Isolation Enabled By Carbon Black'
    elif sensor['network_isolation_enabled'] == False:
        print "Sending disabled email."
        msg="Network Isolation disabled and will deactivate at next sensor check in.\r\n Host: %s\r\nCarbon Black Console: %s\r\n Last Check-In Time: %s\r\nNext Check-In Time: %s" \
            % (sensor['computer_name'], sensor['url'], sensor['last_checkin_time'], sensor['next_checkin_time'])
        msg = MIMEText(msg)
        msg['Subject'] = 'Host Isolation Disabled By Carbon Black'
    else:
        print "Isolation status not defined.  No mail sent."
        return
    
    msg['From'] = 'jswope@bigbluenetworks.com'
    msg['To'] = 'bj@carbonblack.com'
    
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    f = open("isolated_sensors.txt", "r")
    fis = f.read()
    f.close()

    try:
        former_iso_sensors = json.loads(fis)
    except ValueError:
        former_iso_sensors = collections.defaultdict(dict)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sensors = cb.sensors()
   
    current_iso_sensors = collections.defaultdict(dict)

    for sensor in sensors:
        if sensor['network_isolation_enabled'] == True:
            #sensor should be isolating, add sensor to list of currently iso enabled sensors
            sid = str(sensor['id'])
            sensor['url'] = args.url + "/#/host/" + str(sensor['id'])
            current_iso_sensors[sid]['network_isolation_enabled'] = sensor['network_isolation_enabled']
            current_iso_sensors[sid]['is_isolating'] =  sensor['is_isolating']
            try:
                if not sensor['is_isolating'] == former_iso_sensors[sid]['is_isolating']:
                    #state change, send email
                    send_mail(sensor)
            except KeyError  as e:
                #sid is not present in former_iso_sensors, new sensor isolation, send email
                send_mail(sensor)

    f = open("isolated_sensors.txt", "w")
    f.write(json.dumps(current_iso_sensors))
    f.close()
    
    #remove current isolations from from former isolations leaving the list of sensors removed from
    # isolation since the last running of this script
    iso_removed = [item for item in former_iso_sensors if item not in current_iso_sensors]
    for fixed in iso_removed:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sensor = cb.sensor(fixed)
        sensor['url'] = args.url + "/#/host/" + str(sensor['id'])
        #send notification of isolation removal
        send_mail(sensor)

            

if __name__ == "__main__":
    sys.exit(main())

""" List of fields that can be included in the emails:
boot_id
build_id
build_version_string
clock_delta
computer_dns_name
computer_name
computer_sid
cookie
display
emet_dump_flags
emet_exploit_action
emet_is_gpo
emet_process_count
emet_report_setting
emet_telemetry_path
emet_version
event_log_flush_time
group_id
id
is_isolating
last_checkin_time
last_update
license_expiration
network_adapters
network_isolation_enabled
next_checkin_time
node_id
notes
num_eventlog_bytes
num_storefiles_bytes
os_environment_display_string
os_environment_id
os_type
parity_host_id
physical_memory_size
power_state
registration_time
restart_queued
sensor_health_message
sensor_health_status
sensor_uptime
shard_id
status
supports_2nd_gen_modloads
supports_cblr
supports_isolation
systemvolume_free_size
systemvolume_total_size
uninstall
uninstalled
uptime
"""
