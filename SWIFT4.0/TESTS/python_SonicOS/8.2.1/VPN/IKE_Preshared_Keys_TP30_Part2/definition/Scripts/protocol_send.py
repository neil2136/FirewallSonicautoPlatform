#!/usr/bin/python
import os
import sys
import requests
from optparse import OptionParser
import urllib.request as ftp_request
from scapy.all import conf, IP, TCP, srloop

usage = '--- how to use this program -- \n' \
        f'python3 .../protocol_send.py -t ftp -u url'

parser = OptionParser(usage)
parser.add_option('-t', '--type', dest='type', action='store', type='string', help='protocol type')
parser.add_option('-u', '--url', dest='url', action='store', type='string', help='access url')

(options, args) = parser.parse_args()
typename = options.type
url = options.url
print(f'shot parameter value print: -t: {typename}, -u: {url}')

if typename == 'ftp':
    print('start send ftp request...')
    response = ftp_request.urlopen(url)
    print(response)
    print('end send ftp request...')
elif typename == 'http':
    print('start send http request...')
    # timeout=(connect time, read time)
    response = requests.get(url, timeout=(3.05, 3))
    print(response.status_code)
    print('end send http request...')
elif typename == 'terminal':
    print('start send terminal request...')
    terminal_packet = IP(dst=url) / TCP(dport=3389, flags="S")
    resp = srloop(terminal_packet, count=3)
    print(resp)
elif typename == 'ping':
    print('start send ping request...')
    os.system(f'ping {url}')
    print('end send ping request...')

else:
    print('-t parameter value is invalid.')
