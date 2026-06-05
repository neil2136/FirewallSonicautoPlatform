#!/usr/bin/python
import os
import sys
import requests
from optparse import OptionParser
import urllib.request as ftp_request

usage = '--- how to use this program -- \n' \
        f'python3 .../protocolsend.py -t ftp -u url'

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
    response = requests.get(url)
    print(response.status_code)
    print('end send http request...')
else:
    print('-t parameter value is invalid.')
