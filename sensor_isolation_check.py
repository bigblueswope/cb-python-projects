#!/bin/env python

__author__ = 'BJSwope'
import sys, argparse, pprint, warnings, smtplib, cbapi, json
from cli_parser import build_cli_parser
from email.mime.text import MIMEText

def send_mail(details):
    mail = {}
    msg="Network Isolation enabled!\r\nHost: %s\r\nCarbon Black Console: %s/#/host/%s\r\nLast Check-In Time: %s\r\n" % (details['computer_name'], details['url'], details['id'], details['last_checkin_time'])
    msg = MIMEText(msg)
    msg['Subject'] = 'Host Isolated By Carbon Black'
    msg['From'] = 'jswope@bigbluenetworks.com'
    msg['To'] = 'bj@carbonblack.com'
    
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

def main():
    args = build_cli_parser()
    cb = cbapi.CbApi(args.url, token=args.token, ssl_verify=args.ssl_verify, ignore_system_proxy=True)
    f = open("isolated_sensors.txt", "r+")
    fis = f.read()
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sensors = cb.sensors()
    current_iso_sensors = []
   
     try:
        former_iso_sensors = json.loads(fis)
    except ValueError:
        former_iso_sensors = []
    
    for sensor in sensors:
        if sensor['is_isolating'] == True:
            current_iso_sensors.append(sensor['id'])
            if not sensor['id'] in former_iso_sensors:
                former_iso_sensors.append(sensor['id'])
                details = {}
                details['computer_name'] = sensor['computer_name']
                details['id'] = sensor['id']
                details['last_checkin_time'] = sensor['last_checkin_time']
                details['url'] = args.url
                send_mail(details)
            else:
                next
    f.seek(0)
    f.write(json.dumps(current_iso_sensors))
    f.close()
            
            

if __name__ == "__main__":
    sys.exit(main())

