#!/usr/bin/env python

# Shameless lifted from Stackoverflow
# Specifically: https://stackoverflow.com/a/28950776/6692942

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
	print get_ip()
