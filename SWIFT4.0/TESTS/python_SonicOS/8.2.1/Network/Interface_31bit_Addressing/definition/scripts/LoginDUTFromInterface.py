#!/usr/bin/python
import os
import sys
from optparse import OptionParser
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall

scripts_path = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Network/Interface_31bit_Addressing/definition/scripts/'
ipaddress = 'fw interface ip'
usage = '--- how to use this program -- ' \
        '\n python3 ' + scripts_path+'LoginDUTFromInterface.py -i '+ipaddress+' -a login'

parser = OptionParser(usage)
parser.add_option('-i', '--ip', dest='ip', action='store', type='string', help='interface ip')
parser.add_option('-a', '--action', dest='action', action='store', type='string', help='login FW via api')
# parser.add_option('-d', '--doing', dest='doing', action='store', type='string', help='delete linux task')

(options, args) = parser.parse_args()
ip = options.ip
action = options.action
print(f'shot parameter value print: -i: {ip}, -a: {action}')

fw_cli = Firewall(
    ip=ip,
    user="admin",
    password="password",
    supported_config_mode='cli-ssh')

if action == 'login':
    print('start release the api login first...')
    fw_cli.api_logout()
    print('start login fw via api...')
    output = fw_cli.api_login()
    print(output)
    print('login fw processing done.')
elif action == 'showversion':
    from modules.CLI.system import StatusCli
    print('start login fw via api...')
    fw_cli.cli_login()
    print('start get fw config via cli...')
    statuscli = StatusCli(fw_cli)
    output = statuscli.show_version()
    print(output)
else:
    print('-a parameter value is invalid.')
