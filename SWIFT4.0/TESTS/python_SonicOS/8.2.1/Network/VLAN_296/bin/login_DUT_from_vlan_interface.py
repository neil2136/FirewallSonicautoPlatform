#!/usr/bin/python
import os
import sys
import getopt
sys.path.append("/SWIFT4.0/TESTS/python_SonicOS/common_lib")
from utm import Firewall
(opts, args) = getopt.getopt(sys.argv[1:], '-i:-a:', ['ip=', 'action='])
ip_address = ''
action = ''

for opt_name, opt_value in opts:
    if opt_name in ('-i', '--ip'):
        ip_address = opt_value
        print("ip address is {}".format(ip_address))    
    elif opt_name in ('-a', '--action'):
        action = opt_value
        print("action is {}".format(action))    
     

fw1 = Firewall(ip=ip_address, user="admin", password="password", supported_config_mode='cli-ssh')

if action == 'login':
    ret = fw1.api_login()
    print(ret)
else:
    ret = fw1.api_logout()
    print(ret)

