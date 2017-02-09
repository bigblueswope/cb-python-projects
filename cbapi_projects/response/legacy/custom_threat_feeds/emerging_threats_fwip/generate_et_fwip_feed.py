# stdlib imports
import os, sys, time, urllib, json, pprint

# third party lib imports
# google's ipaddr python library from github.com/google/ipaddr-py
sys.path.append('../../../../ipaddr-py')
import ipaddr

# our imports
sys.path.append('../../../../cbfeeds/')
import cbfeeds
from cbfeeds import CbReport
from cbfeeds import CbFeed
from cbfeeds import CbFeedInfo

#modulenames = set(sys.modules)&set(locals())
#allmodules = [sys.modules[name] for name in modulenames]
#pprint.pprint(allmodules)

def get_et_fwips():
    nodes = []
    url = "https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt"
    #######
    ###### the orignal tor example fetched a json file
    ###### we are fetching a plain text file
    ###### we will use the google ipaddr.py to validate IP addresses
    ###### we will also split any subnet lines on their / chars and for 
    ###### ranges > 1000 IPs in size we will build a query report
    ###### ranges < 1000 IPs in size will be individual IOCs
    jsonurl = urllib.urlopen(url)
    text = json.loads(jsonurl.read())
    for entry in text['relays']:
        try:
            for address in entry['or_addresses']:
                # IPv4 addresses are ip:port, IPv6 addresses are [ip]:port:
                # "or_addresses":["80.101.115.170:5061","[2001:980:3b4f:1:240:caff:fe8d:f02c]:5061"],
                # process only IPv4 addresses for now
                if address.count(':') == 1:
                    # All IPv4 addresses will end up here.
                    ipv4, port = address.split(':')
                    nodes.append({'ip': ipv4,
                                  'name': entry['nickname'],
                                  'port': port,
                                  'firstseen': entry['first_seen'],
                                  'lastseen': entry['last_seen'],
                                  'contact': entry.get("contact", "none")})
        except Exception, err:
            print "%s while parsing: %s" % (err, entry)
    return nodes


def build_reports(nodes):
    # TODO - this is one "report" per TOR node IP.  Not ideal.
    reports = []
    unique_ips = set()
    for node in nodes:
        # avoid duplicated reports
        # CBAPI-22
        if node['ip'] in unique_ips:
            continue
        else:
            unique_ips.add(node['ip'])

        fields = {'iocs': {
            'ipv4': [node['ip'], ]
        },
                  'score': 50,
                  'timestamp': int(time.mktime(time.gmtime())),
                  'link': 'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
                  'id': "Emerging-Threats-%s" % node['ip'],
                  'title': "%s is on Emerging Threats' list of IPs to block at the Firewall." % (node['ip'])}
        reports.append(CbReport(**fields))

    return reports


def create():
    nodes = get_et_fwips()
    reports = build_reports(nodes)

    feedinfo = {'name': 'Emerging_Threats',
                'display_name': "Emerging Threats IPs",
                'provider_url': 'https://www.emergingthreats.net/',
                'summary': "This feed is a list of IP addresses, from Emerging Threats public feed.",
                'tech_data': "There are no requirements to share any data to receive this feed.",
                'icon': 'et_image.jpg',
                'icon_small': 'et_image_small.jpg',
                'category': 'Open Source',
                }

    # lazy way out to get right icon path.  sorry.
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    feedinfo = CbFeedInfo(**feedinfo)
    feed = CbFeed(feedinfo, reports)
    created_feed = feed.dump()

    os.chdir(old_cwd)

    return created_feed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s [outfile]" % sys.argv[0]
        sys.exit(0)
    bytes = create()
    open(sys.argv[1], "w").write(bytes)
