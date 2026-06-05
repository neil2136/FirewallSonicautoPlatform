import sys
import os
import re
import argparse
import time
import pexpect
## Add test
## Add test
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from utm import is_Firewall_up
from util.openstack import Openstack
from runner.settings import logger

class RestoreFwTelnet():
    def __init__(self, ip='192.168.168.168', console_ip='', console_port='', console_user='qa',\
                 console_password='qa', user='admin', password='password',new_password='password', boot_check=True):
        self.console_ip = console_ip
        self.console_port = console_port
        self.console_user = console_user
        self.console_password = console_password
        self.user = user
        self.password = password
        self.new_password = new_password
        self.wrongpass = 'Admin@123456789'
        self.ip = ip
        self.boot_check = boot_check
        self.fw = Firewall(self.ip, console_ip=self.console_ip, console_port=self.console_port,\
                           user=self.user, password=self.password, new_password=self.new_password, supported_config_mode='cli-console')
        self.fw_wrongpass = Firewall(self.ip, console_ip=self.console_ip, console_port=self.console_port,\
                                     user=self.user, password=self.wrongpass, supported_config_mode='cli-console')
        logger.info('Console ip: ' + self.console_ip )
        logger.info('Console port: ' + str(self.console_port) )

    def update_password_in_default_state(self):
        (rc, output) = self.fw.cli_login(errcode=1)
        return rc
    
    def restore(self):
        commands = ['configure', 'restore-defaults']
        try:
            (rc, output) = self.fw.do_cli_commands(commands, 1)
        except pexpect.exceptions.EOF:
            # Device is rebooting after restore-defaults, this is expected
            logger.info('Connection closed by device (EOF), device is rebooting after restore-defaults.')
            rc = True
            output = 'Restoring to factory defaults - device rebooting'
        
        if not rc and 'Maximum login attempts exceeded' in output:
            logger.info('Maybe wrong password.')
            try:
                (rc, output) = self.fw_wrongpass.do_cli_commands(commands, 1)
            except pexpect.exceptions.EOF:
                logger.info('Connection closed by device (EOF), device is rebooting after restore-defaults.')
                rc = True
                output = 'Restoring to factory defaults - device rebooting'
        
        if not rc:
            logger.info(output)
            logger.info('telnet fail, try ssh....')
            fw_ssh = Firewall(self.ip, user=self.user, password=self.password, new_password=self.new_password, supported_config_mode='cli-ssh')
            (rc1, output1) = fw_ssh.do_cli_commands(commands, 1)
            if not rc1:
                logger.error('Firewall boots up failed.')
                return False
            rc = rc1
        
        if self.boot_check:
            # Wait for device to reboot after restore-defaults
            # logger.info('Waiting for firewall to reboot after restore-defaults...')
            # time.sleep(240)  # Sleep 240s for device to reboot
            out = os.popen(f'ping {self.ip} -c 3').read()
            rc = '100% packet loss' not in out
            logger.info('Firewall is up.')
            # if is_Firewall_up(self.ip):
            #     logger.info('Firewall boots up')
            #     return rc
            # logger.error('Firewall boots up failed.')
            # return False
        return rc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restore firewall via telnet.')
    # parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', help='testbed ID, like: VTB518')
    # parser.add_argument('-device', type=str, dest='device', required=True, help='device name, like: UTM')
    parser.add_argument('-cserver', '--con_server', type=str, dest='con_server', required=True, help='console server ip')
    parser.add_argument('-cport', '--con_port', type=str, dest='con_port', required=True, help='console server login user')
    args = parser.parse_args()

    if args.con_server and args.con_port:
        consvr = args.con_server
        conport = args.con_port
    # elif args.testbed:
    #     logger.info('------------ ' + args.testbed + '------------')
    #     ostack = Openstack(args.testbed)
    #     # console_info = ostack.get_console_info()
    #     console_info = ostack.get_console_info(args.device)
    #     if console_info:
    #         consvr = console_info[0]
    #         conport = console_info[1]
    # else:
    #     out = os.popen('hostname').read()
    #     hostname = out.split('-')[0]
    #     if hostname:
    #         logger.info('------------ ' + hostname + '------------')
    #         ostack = Openstack(hostname)
    #         console_info = ostack.get_console_info(args.device)
    #         if console_info:
    #             consvr = console_info[0]
    #             conport = console_info[1]
    logger.info('Console server: ' + consvr)
    logger.info('Console port:   ' + conport)
    restore_telnet = RestoreFwTelnet(console_ip=consvr, console_port=conport)
    restore_telnet.restore()

