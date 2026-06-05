import sys
import os
import re
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
    def __init__(self, ip='192.168.168.168', console_ip='', console_port='', user='admin', password='password',interface='',zone='',gw='',netmask ='255.255.255.0'):
        self.console_ip = console_ip
        self.console_port = console_port
        self.console_user = user
        self.console_password = password
        self.user = user
        self.password = password
        self.ip = ip
        self.interface = interface
        self.zone = zone
        self.gw = gw
        self.netmask = netmask
        self.fw = Firewall(self.ip, console_ip=self.console_ip, console_port=self.console_port,user=self.user, password=self.password, supported_config_mode='cli-console')
        logger.info('Console ip: ' + self.console_ip )
        logger.info('Console port: ' + str(self.console_port) )

    def cfg_if_tel(self):
        logger.info(" {} ".center(20, '-').format('Config interface by telnet'))
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/cfg_if_tel.exp '
        cmd1 = "/usr/bin/expect "+ path + self.console_ip +' '+ self.console_port +' '+ self.interface +' '+ self.zone +' '+ self.ip +' '+ self.gw
        logger.info(cmd1)
        rc = os.system(cmd1)
        if rc:
            logger.info("ERROR: Change FW {} ip through {} {} failed".format(self.interface,self.console_ip,self.console_port))

        logger.info('\nTry https management...')
        log_file = "/tmp/wget_log.txt"
        get_file = "/tmp/wget_file.txt"
        man_ip = self.ip
        man_if = self.interface
        os.system('rm -rf '+ log_file)
        os.system('rm -rf '+ get_file)

        cmd2 = "wget https://{} --no-check-certificate -o {} -O {} -T 10 -t 1".format(man_ip,log_file,get_file)
        logger.info(cmd2)
        out = subprocess.Popen(cmd2, shell = True, stdout = subprocess.PIPE).communicate()[0].decode('ASCII')

        if out:
            print("wget on this testbed doesn't have --no-check-certificate option.")
            cmd2 = "wget https://{} -o {} -O {} -T 10 -t 1".format(man_ip,log_file,get_file)
            print(cmd2)
            rc = os.popen(cmd2).read()
            if rc:
                print(rc,'Command error!')
        print('=' * 60)
        out_log = os.popen('cat ' + log_file).read()
        print(out_log)
        print('=' * 60)
        # get_log = os.popen('cat ' + get_file).read()
        # print(get_log)
        # print('*' * 60)
        print("Change FW {} ip through {} {} passed\n".format(self.interface,self.console_ip,self.console_port))

    def config_interface(self):
        commands = ['configure', 'interface '+ self.interface, 'ip-assignment '+ self.zone + ' static', 'ip ' + self.ip + ' netmask '+ self.netmask]
        if self.gw:
            commands.append('gateway' + self.gw)
        commands.extend(['end', 'exit'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        return rc
    
    def config_interface_mgmt(self, **kwargs):
        commands = ['configure', 'interface ' + kwargs['interface'], 'ip-assignment ' + kwargs['zone'] + ' static',
                    'ip ' + kwargs['ip'] + ' netmask ' + self.netmask, 'exit']
        if 'mgmt_https' in kwargs.keys():
            commands.append('management https')
        if 'mgmt_ping' in kwargs.keys():
            commands.append('management ping')
        if 'mgmt_ssh' in kwargs.keys():
            commands.append('management ssh')
        if 'mgmt_snmp' in kwargs.keys():
            commands.append('management snmp')
        commands.extend(['end', 'exit'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        print(output)
        return rc
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restore firewall via telnet.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', required=True, help='testbed ID, like: VTB518')
    parser.add_argument('-device', type=str, dest='device', required=True, help='device name, like: UTM')
    parser.add_argument('-if', type=str, dest='interface', required=True, help='interface name, like: X0')
    parser.add_argument('-zone', type=str, dest='zone', required=True, help='zone name, like: LAN')
    parser.add_argument('-ip', type=str, dest='ip', required=True, help='ip, like: 11.11.11.101')
    parser.add_argument('-cserver', '--con_server', type=str, dest='con_server', help='console server ip')
    parser.add_argument('-cport', '--con_port', type=str, dest='con_port', help='console server login user')
    parser.add_argument('-gw', type=str, dest='gateway', help='interface gateway')
    parser.add_argument('-mask', type=str, dest='mask', default='255.255.255.0', help='interface netmask')
    parser.add_argument('-os', type=str, dest='osstack', help='openstack flag')
    parser.add_argument('-exp',type=str,dest='exp',help='import exp file')
    parser.add_argument('-mgmt',type=bool, dest='mgmt', help='enable interface mgmt')
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
            logger.info('------------' + args.testbed + '-----------0-')
            ostack = Openstack(args.testbed)
            logger.info(args)
            console_info = ostack.get_console_info(args.device)
            print(console_info)

            if console_info:
                consvr = console_info[0]
                conport = console_info[1]
        else:
            out = os.popen('hostname').read()
            hostname = out.split('-')[0]
            if hostname:
                logger.info('------------ ' + hostname + '------------')
                ostack = Openstack(hostname)
                console_info = ostack.get_console_info(args.device)
                if console_info:
                    consvr = console_info[0]
                    conport = console_info[1]
    else:
        logger.info('not ready for not openstack testbed.')
        exit(1)

    conip = args.ip
    conif = args.interface   # cannot use args.if
    conzone = args.zone

    logger.info('Console server: ' + consvr)
    logger.info('Console port:   ' + conport)
    res = ConfigInterfaceTelnet(console_ip=consvr, console_port=conport,ip=conip,interface=conif,zone=conzone,gw='')
    if args.exp:
        res.cfg_if_tel()
    else:
        if args.mgmt:
            params = {
                    "interface": args.interface,
                    'ip': args.ip,
                    'zone': args.zone,
                    'mgmt_https': True,
                    'mgmt_ping': True,
                    'mgmt_snmp': True,
                    'mgmt_ssh': True
                }
            res.config_interface_mgmt(**params)
        else:
            res.config_interface()
