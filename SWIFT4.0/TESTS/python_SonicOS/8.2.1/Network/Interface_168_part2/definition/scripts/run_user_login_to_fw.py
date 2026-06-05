#!/usr/bin/python
import os
import sys
from optparse import OptionParser
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from modules.API.users import UserLocalApi, UserLoginApi

scripts_path = os.environ["PYTHON_SONICOS_HOME"] + \
               '/Smoke_Test/Quick_Smoke_For_RTQA/definition/scripts/'
ipaddress = 'fw interface ip'
usage = '--- how to use this program -- ' \
        '\n python3 ' + scripts_path+'run_user_login_to_fw.py -i '+ipaddress+' -a limit_login -u test -p password'

parser = OptionParser(usage)
#print(usage)
parser.add_option('-i', '--ip', dest='ip', action='store', type='string', help='interface ip')
parser.add_option('-a', '--action', dest='action', action='store', type='string', help='login FW via api')
parser.add_option('-u', '--user', dest='user', action='store', type='string', help='login FW user name')
parser.add_option('-p', '--password', dest='password', action='store', type='string', help='login FW password')

(options, args) = parser.parse_args()
ip = options.ip
action = options.action
user = options.user
password = options.password
print(f'shot parameter value print: -i: {ip}, -a: {action} -u: {user} -p: {password}')

fw_cli = Firewall(
    ip=ip,
    user=user,
    password=password,
    supported_config_mode='cli-ssh')
fw_api = Firewall(
    ip=ip,
    user='test',
    password='password',
    supported_config_mode='api')

limituserlogin = UserLoginApi(headers=None,
                              ip=ip,
                              username=user,
                              password=password)

if action == 'api_login':
    print('start release the api login first...')
    fw_cli.api_logout()
    print('start login fw use admin via api...')
    output = fw_api.api_login()
    print('login fw processing done.')
elif action == 'limit_login':
    print('start release the api login first...')
    fw_cli.api_logout()
    print(f'start login fw use {user} via api...')
    res, bearer_token = limituserlogin.local_user_login()
    print(f'login fw result is {res}, bearer_token is {bearer_token}')
elif action == 'show_version':
    from modules.CLI.system import StatusCli
    print('start login fw via api...')
    rc = fw_cli.cli_login()
    print(rc)
    print('start get fw config via cli...')
    statuscli = StatusCli(fw_cli)
    output = statuscli.show_version()
    print(output)
else:
    print('-a parameter value is invalid.')
