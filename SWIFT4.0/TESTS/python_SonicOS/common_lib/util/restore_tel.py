import argparse
import os
import re
import sys
import pexpect

from config.openstack import get_console_info
from runner.settings import Params, LOGGING
logger = LOGGING.getLogger(__name__)

temp_args = sys.argv[1:]
parser = argparse.ArgumentParser(description="Restore firewall use telnet.")
parser.add_argument('-t', '--testbed', action="store", dest="testbed", required=False)
parser.add_argument('-p', '--product', action="store", dest="product")
parser.add_argument('--con_user', action="store", dest="con_user", default='admin')
parser.add_argument('--con_passwd', action="store", dest="con_passwd", default='password')
parser.add_argument('--fw_user', action="store", dest="fw_user", default='admin')
parser.add_argument('--fw_passwd', action="store", dest="fw_passwd", default='password')
parser.add_argument('--fw_wrong_passwd', action="store", dest="fw_wrong_passwd", default='Admin@123456789')

args = parser.parse_args()
if re.match(r'[vtb3|vtb5|vtb7|vtb8|vtb9]', args.testbed, re.I)：
    os = Openstack(args.testbed)
    console = os.get_console_info(dut=args.product)
    if console:
        console_ip, console_port = console

try:
    ssh = pexpect.spawn('telnet ' +  console_ip + ' ' + str(console_port) )
except:
    logger.error('Could not start telnet to ' + console_ip + ' ' + str(console_port) )
    return False
port_prefix = re.match(r'(\d)', str(console_port))
if not port_prefix:
    return False
elif port_prefix.group(1) == '2':
    if not ssh.expect([pexpect.TIMEOUT, 'login:']): 
        logger.error('Unable to Telnet to: ' + console_ip  + ' ' + str(console_port))
        return False          
    ssh.sendline(args.con_user)
    if not ssh.expect([pexpect.TIMEOUT, 'Password:']): 
        return False
    ssh.sendline(args.con_passwd)
elif port_prefix.group(1) == '6':
    pass
    
for i in range(0,2):
    ssh.sendline('')
flushbuffer()
ssh.sendline('')
time.sleep(1)
fail_num = 0
passwd_flag = 0
while True:
    index = ssh.expect([
        pexpect.TIMEOUT, 
#                '(yes\/no)', 
        'User:',
        'Password:',
        '>',
        'config\(.*\)\# ',
        '\(.*\)?\# ',
        '->',
        'Au revior',
        'changes found',
        'Connection closed by foreign host',
        'Access denied',
        '\(Y\/N\)|\(yes\/no\)|\(yes\/cancel\)',
        'Restarting now',
    ])        
    
    if index == 0: # Timeout
        fail_num += 1
        if fail_num ==5:
            logger.error('Firewall has no response.')
        ssh.close()
        return False
    elif index == 1:               
        ssh.sendline(fw_user)
        passwd_flag += 1
        continue
    elif index == 2: # password
        if passwd_flag == 2:
            ssh.sendline(fw_wrong_passwd)
        else:
            ssh.sendline(fw_passwd)
        continue
    elif index == 3: 
        logger.info('Console to dut via telnet {} {} sucessfully.'.format(self.console_ip,self.console_port))
        ssh.sendline('firmware boot current factory')
        passwd_flag += 1
        continue
    elif index == 4 or index ==5:
        ssh.sendline("exit")
        continue
    elif index == 6:
        ssh.sendline('exit')
        continue
    elif index == 7:
        self.ssh.sendline('')
        continue
    elif index == 8:
        ssh.sendline('no')
        continue  
    elif index == 9:
        result = False
        logger.error('Please check server password.')
    elif index == 10:
        ssh.sendline(fw_user)
        passwd_flag = 2
        continue   
    elif index == 11:
        ssh.sendline('yes')
        continue                  
    elif index == 12:
        result == True
        break
if result:
    logger.info('Fail to restore firewall.')
    ssh.send('\c]')
    ssh.close()

ssh.expect([pexpect.TIMEOUT, 'Serial Number\W+:\W+(\w{12})'], timeout=300)

def enable_all_management():

def disable_fips():
