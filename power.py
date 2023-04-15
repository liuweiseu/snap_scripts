#! /usr/bin/env python3

"""
usage: power.py [-h] [--url URL] [--socket SOCKET] [--status STATUS]

Control the ethernet power strip.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             The url of wps, such as: http://admin:1234@192.168.0.100.
  --socket SOCKET       The socket number.
  --status STATUS, -s STATUS
                        Turn on/off the wps.
"""

import sys, os
from argparse import ArgumentParser

wps = {
    "url": "http://admin:1234@192.168.0.100",
    "socket": 1
}

# turn power on or off
#
def power_set(wps, status):
    url = wps['url']
    socket = wps['socket']
    if status == 'on':
        value = 'ON'
    else:
        value = 'OFF'
    cmd = 'curl -s %s/outlet?%d=%s > /dev/null'%(url,socket,value)
    ret = os.system(cmd)
    if ret: raise Exception('%s returned %d'%(cmd, ret))


# return True if power is on
#
def power_query(wps):
    url = wps['url']
    socket = wps['socket']
    cmd = 'curl -s %s/status'%(url)
    out = os.popen(cmd).read()
    off = out.find('state">')
    off += len('state">')
    y = out[off:off+2]
    status = int(y, 16)
    if(status&(1<<(socket-1))):
        return 'true'

if __name__ == "__main__":
    parser = ArgumentParser(description="Control the ethernet power strip.")
    parser.add_argument('--url',dest='url', type=str,help='The url of wps, such as: http://admin:1234@192.168.0.100.')
    parser.add_argument('--socket',dest='socket',type=int,help='The socket number.')
    parser.add_argument('--status','-s',dest='status',type=str,help='Turn on/off the wps.')
    args = parser.parse_args()

    if args.url:
        wps['url'] = args.url
    if args.socket:
        wps['socket'] = args.socket
    if args.status:
        power_set(wps,args.status)
        print('turned power %s'%args.status)
    else:
        status = power_query(wps)
        if status:
            print('power is on')
        else:
            print('power is off')


