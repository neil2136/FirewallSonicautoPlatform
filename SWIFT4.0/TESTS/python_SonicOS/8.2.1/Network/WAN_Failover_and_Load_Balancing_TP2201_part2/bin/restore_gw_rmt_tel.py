__author__ = 'CHU'
import sys
import os
import re
import time
import argparse
import subprocess

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from utm import is_Firewall_up
from util.openstack import Openstack
from runner.settings import logger
from pprint import pprint
from modules.API.system import AdminApi

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
admin = AdminApi(fw)


class ConfigInterfaceTelnet():
    def __init__(self, ip='192.168.168.168', console_ip='', console_port='', user='admin', password='password', new_password='password',
                 interface='', zone='', gw='', netmask='255.255.255.0'):
        self.console_ip = console_ip
        self.console_port = console_port
        self.console_user = user
        self.console_password = password
        self.user = user
        self.password = password
        self.new_password = new_password
        self.ip = ip
        self.interface = interface
        self.zone = zone
        self.gw = gw
        self.netmask = netmask
        self.fw = Firewall(self.ip, console_ip=self.console_ip, console_port=self.console_port, user=self.user,
                           password=self.password, new_password='password', supported_config_mode='cli-console')
        print('Console ip: ' + self.console_ip)
        print('Console port: ' + str(self.console_port))

    def restore(self):
        logger.info('Maybe need to wait 120 seconds...')
        commands = ['configure', 'restore-defaults']
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        if not rc:
            print(output)
        time.sleep(120)
        cmd = ['show status']
        for i in range(10):
            (rc, out) = self.fw.do_cli_commands(cmd, 1)
            if 'System Information:' in out:
                logger.info('Firewall boots up')
                return True
            logger.info('Sleep 30s for firewall up...')
            time.sleep(30)
            if i == 9:
                logger.error('Firewall boots up failed.')
                return False

    def config_interface(self, **kwargs):
        logger.info(" {} ".center(30, '*').format(' Config interface '))
        print(kwargs)
        if 'acc_rule' in kwargs.keys():
            commands = ['configure', 'access-rule from WAN to LAN action deny', 'action allow']
        elif 'nat_policy' in kwargs.keys():
            commands = ['configure', 'nat-policy inbound X0 outbound X1 translated-source name "X1 IP"', 'no enable', \
'exit', 'nat-policy inbound X2 outbound X1 translated-source name "X2 IP"', 'no enable']
        else:
            commands = ['configure', 'interface ' + kwargs['interface'], 'ip-assignment ' + kwargs['zone'] + ' static',
                        'ip ' + kwargs['ip'] + ' netmask ' + self.netmask]
            if 'gw' in kwargs.keys():
                commands.append('gateway ' + kwargs['gw'])
            if 'mgmt_https' or 'mgmt_ping' or 'mgmt_ssh' in kwargs.keys():
                commands.append('exit')
                if 'mgmt_https' in kwargs.keys():
                    commands.append('management https')
                if 'mgmt_ping' in kwargs.keys():
                    commands.append('management ping')
                if 'mgmt_ssh' in kwargs.keys():
                    commands.append('management ssh')

        commands.extend(['end', 'exit'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        print(output)
        return rc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restore firewall via telnet.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', required=True,
                        help='testbed ID, like: VTB518')
    parser.add_argument('-device', type=str, dest='device', required=True, help='device name, like: UTM')
    parser.add_argument('-if', type=str, dest='interface', required=True, help='interface name, like: X0')
    parser.add_argument('-zone', type=str, dest='zone', required=True, help='zone name, like: LAN')
    parser.add_argument('-ip', type=str, dest='ip', required=True, help='ip, like: 11.11.11.101')
    parser.add_argument('-cserver', '--con_server', type=str, dest='con_server', help='console server ip')
    parser.add_argument('-cport', '--con_port', type=str, dest='con_port', help='console server login user')
    parser.add_argument('-gw', type=str, dest='gateway', help='interface gateway')
    parser.add_argument('-mask', type=str, dest='mask', default='255.255.255.0', help='interface netmask')
    parser.add_argument('-os', type=str, dest='osstack', help='openstack flag')
    parser.add_argument('-restore', type=str, dest='restore', help='restore the DUT')
    args = parser.parse_args()

    print("Enable admin preempt logout!\n")
    out = admin.show_admin_setting()
    # pprint(out)

    admin_info = {
        "administration": {
            'admin': {
                'preempt_action': 'logout'
            },
            'gms_management': {}
        }
    }
    out = admin.edit_admin(**admin_info)
    # pprint(out)

    consvr = ''
    conport = ''
    if args.osstack == '1':
        if args.con_server and args.con_port:
            consvr = args.con_server
            conport = args.con_port
        elif args.testbed:
            print('------------' + args.testbed + '-----------0-')
            ostack = Openstack(args.testbed)
            print(args)
            console_info = ostack.get_console_info(args.device)
            print(console_info)

            if console_info:
                consvr = console_info[0]
                conport = console_info[1]
        else:
            out = os.popen('hostname').read()
            hostname = out.split('-')[0]
            if hostname:
                print('------------ ' + hostname + '------------')
                ostack = Openstack(hostname)
                console_info = ostack.get_console_info(args.device)
                if console_info:
                    consvr = console_info[0]
                    conport = console_info[1]
    else:
        print('not ready for not openstack testbed.')
        exit(1)

    conip = args.ip
    conif = args.interface  # cannot use args.if
    conzone = args.zone

    print('Console server: ' + consvr)
    print('Console port:   ' + conport)
    res = ConfigInterfaceTelnet(console_ip=consvr, console_port=conport, ip=conip, interface=conif, zone=conzone, gw='')

    if_opt = []
    if args.device == 'VPNGW':
        if_opt = [{
            'interface': conif,
            'ip': conip,
            'zone': conzone,
            'mgmt_ping': True,
            'mgmt_ssh': True
        },
            {
                "interface": 'x1',
                'ip': '12.12.1.101',
                'zone': 'WAN',
                'gw': '12.12.1.1',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            },
            {
                "interface": 'x2',
                'ip': '12.12.2.101',
                'zone': 'LAN',
                'gw': '12.12.2.1',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            },
            {
                'acc_rule': True
            },
            {
                'nat_policy' : True
            }]
    if 'RemoteGEN' in args.device:
        if_opt = [
            {
                "interface": 'x0',
                'ip': '172.16.1.101',
                'zone': 'LAN',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            },
            {
                'interface': 'x1',
                'ip': '12.12.1.201',
                'zone': 'WAN',
                'gw': '12.12.1.101',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            },
            {
                'interface': 'x2',
                'ip': '12.12.2.201',
                'zone': 'WAN',
                'gw': '12.12.2.101',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            },
            {
                'interface': 'x3',
                'ip': '12.12.3.201',
                'zone': 'LAN',
                'gw': '12.12.3.101',
                'mgmt_https': True,
                'mgmt_ping': True,
                'mgmt_ssh': True
            }
        ]

    if args.restore:
        rc = res.restore()
        if rc:
            for item in if_opt:
                res.config_interface(**item)
        else:
            logger.error('Something wrong in restore fw..')
