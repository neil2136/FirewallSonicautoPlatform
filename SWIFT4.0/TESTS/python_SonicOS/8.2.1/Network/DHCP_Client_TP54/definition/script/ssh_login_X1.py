#!/usr/bin/python
import os
import sys
import getopt
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import FirewallCLI

(opts, args) = getopt.getopt(sys.argv[1:], '-i:', ['ip='])
ip_address = ''

for opt_name, opt_value in opts:
    if opt_name in ('-i', '--ip'):
        ip_address = opt_value
        print("ip address is {}".format(ip_address))    

fw_ssh = FirewallCLI(ip=ip_address, user="admin", password="password", supported_config_mode='cli-ssh')
ret = fw_ssh.cli_login()
print(ret)
