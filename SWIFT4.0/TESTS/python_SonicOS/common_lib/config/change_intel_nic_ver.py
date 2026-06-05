import sys
import os
import re
import time
import pexpect
import argparse
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall,G_PASSWORD_NEW
from utm import is_Firewall_up
from util.openstack import Openstack
from runner.settings import logger

class ChangeNICVer():
    def __init__(self, version, ip='192.168.168.168',
                 console_ip='', console_port='', console_user='admin', console_password='password',
                 user='admin', password='password',new_password=G_PASSWORD_NEW, boot_check=False):
        self.console_ip = console_ip
        self.console_port = console_port
        self.console_user = user
        self.console_password = password
        self.user = user
        self.password = password
        self.new_password = new_password
        self.ip = ip
        self.boot_check = boot_check
        self.version = re.sub(r"(^7\.\d+\.\d+)\.\d+", r"\1", version)
        self.fw = Firewall(self.ip, console_ip=self.console_ip, console_port=self.console_port,
                           user=self.user, password=self.password, new_password=self.new_password,
                           supported_config_mode='cli-console')
        logger.info('Console ip: ' + self.console_ip )
        logger.info('Console port: ' + str(self.console_port) )

    def check_ver(self):
        update_nic_ver = ''
        (rc, output) = self.fw.do_cli_commands(['show status'], 1)
        pattern = re.search(r'Model:\D+(\d+)700', output, re.I)
        if pattern and int(pattern.group(1)) > 3:
            pattern = re.search(r'Firmware Version\W+SonicOS\s+(\d+\.\d+\.\d+\S+)', output, re.I)
            ver = ''
            if pattern:
                ver = pattern.group(1)
            if ver.startswith('7.') and self.version.startswith('8.'):
                update_nic_ver = 'new' # current GEN7, 1. upgrade 2. update NIC ver
            elif ver.startswith('8.') and self.version.startswith('7.'):
                update_nic_ver = 'old' # current GEN8, 1. update NIC ver 2. upgrade
        return update_nic_ver

    def update_nic_ver(self, ver):
        if ver.lower() not in ['old', 'new']:
            return False, "Please input a legal version sting: old/new"

        fw_obj = self.fw
        safemode = False
        
        timeout = 5
        for i in range(0,2):
            rc, output = fw_obj.cli_login(1)
            if rc:
                break
            logger.info('Fail to login. try again')
            if (i == 1):
                # self.ssh.sendline('exit')
                try:
                    fw_obj.ssh.close()
                except:
                    logger.error('Maximum try, Login fail.')
                finally:
                    if tag == 1:
                        logger.error('Login failed log: {}'.format(output))
                        return False, output
                    return False

        fw_obj.flushbuffer()
        output = ''
        pass_tag = False
        fw_obj.ssh.sendline('safemode')
        time.sleep(0.1)
        wrong_time = 0
        while True:
            index = fw_obj.ssh.expect([
                pexpect.TIMEOUT,
                r'\[cancel\]:',
                r'Enter into the safemode now',
                r'Enter an option:',
                r'\(y/N\):',
                r'\(old/new\):',
                r'Serial Number.*:',
                r'Are you sure you wish to enter into safemode'],
                timeout=timeout)
            try:
                output += bytes.decode(fw_obj.ssh.before) + bytes.decode(fw_obj.ssh.after)
            except:
                logger.debug('output {} {} not meet the expected match.'.format(fw_obj.ssh.before, fw_obj.ssh.after))
            if index == 0:
                logger.info('Wrong command: ' + bytes.decode(fw_obj.ssh.before) + str(fw_obj.ssh.after))
                wrong_time += 1
                if wrong_time > 2:
                    break
            if index == 1 or index == 7:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                timeout = 5
                time.sleep(1)
                fw_obj.ssh.sendline('yes')
                safemode = True
                continue
            if index == 2:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                timeout = 180
                time.sleep(60)
                logger.info('======>' + 'Have finished 1 minute sleep.')
                continue
            if index == 3:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                safemode = True
                timeout = 5
                fw_obj.ssh.sendline('intel-mac-firmware-update')
                continue
            if index == 4:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                timeout = 5
                fw_obj.ssh.sendline('y')
                continue
            if index == 5:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                timeout = 300
                logger.info('======>' + f'Send version {ver}')
                fw_obj.ssh.sendline(ver)
                time.sleep(300)
                logger.info('======>' + 'Have finished 300s sleep.')
                continue
            if index == 6:
                fw_obj.flushbuffer()
                logger.info('======>' + output)
                logger.info('======>' + 'Firewall boots up from safemode.')
                safemode = False
                pass_tag = True
                break

        fw_obj.ssh.sendcontrol(']')
        fw_obj.ssh.close()
        if wrong_time > 2:
            return False
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Intel NIC ver via telnet.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', help='testbed ID, like: VTB518')
    parser.add_argument('-device', type=str, dest='device', required=True, help='device name, like: UTM')
    parser.add_argument('-cserver', '--con_server', type=str, dest='con_server', help='console server ip')
    parser.add_argument('-cport', '--con_port', type=str, dest='con_port', help='console server login user')
    args = parser.parse_args()

    if args.con_server and args.con_port:
        consvr = args.con_server
        conport = args.con_port
    elif args.testbed:
        logger.info('------------ ' + args.testbed + '------------')
        ostack = Openstack(args.testbed)
        console_info = ostack.get_console_info(args.device)
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
    logger.info('Console server: ' + consvr)
    logger.info('Console port:   ' + conport)
    res = ChangeNICVer(console_ip=consvr, console_port=conport, version='7.0.0-8013')
#    out = res.check_ver()
    out = res.update_nic_ver('old')
    print(f'====== {out} ======')


