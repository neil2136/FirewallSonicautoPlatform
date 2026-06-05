import os
import sys
from optparse import OptionParser
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall

scripts_path = os.environ["PYTHON_SONICOS_HOME"] + \
               '/CLI/SSH_With_ECLI/definition/scripts/'
ipaddress = 'fw interface ip'
usage = '--- how to use this program -- ' \
        '\n python3 ' + scripts_path+'LoginDUTFromInterface.py -i '+ipaddress+' -a login'

parser = OptionParser(usage)
parser.add_option('-i', '--ip', dest='ip', action='store', type='string', help='interface ip')
parser.add_option('-a', '--action', dest='action', action='store', type='string', help='login FW via api')
parser.add_option('-u', '--username', dest='username', action='store', type='string', help='Username to login')
parser.add_option('-p', '--password', dest='password', action='store', type='string', help='Password to login')
parser.add_option('-n', '--number', dest='number', action='store', type='int', help='SSH connection number')

(options, args) = parser.parse_args()
ip = options.ip
action = options.action
username = options.username
password = options.password
print(f'shot parameter value print: -i: {ip}, -a: {action}, -u: {username}, -p: {password}')

fw_cli_script = Firewall(
    ip=ip,
    user=username,
    password=password,
    supported_config_mode='cli-ssh')

if action == 'login':
    print('start login fw via cli...')
    output = fw_cli_script.ssh_connect(errcode=1)
    print(output)
    print('login fw processing done.')
elif action == 'addao':
    print('start login fw via cli...')
    fw_cli_script.cli_login()
    print('start add an address object via cli...')
    add_ao_cli = [
        'configure',
        'address-object ipv4 test host 192.168.168.11 zone LAN',
        'commit',
        'end',
        'show address-object ipv4 test']
    output = fw_cli_script.do_cli_commands(add_ao_cli, tag=1)
else:
    print('-a parameter value is invalid.')
