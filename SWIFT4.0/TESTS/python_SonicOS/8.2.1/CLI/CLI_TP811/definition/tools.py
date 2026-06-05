from definition.init_param import *
import re
import ipaddress
import os
import sys
import time
from collections import OrderedDict
import json
from pprint import pprint
from telnetlib import Telnet
import pexpect
import struct
import hashlib
from tcpping import tcpping
import requests
import urllib3
import subprocess
from requests.auth import HTTPDigestAuth

def login(user="admin", ip= "192.168.168.168",cli_port= '22',password='password',prompt='>'):
    os.system('sed -i ' + '\'' + '/' + ip + '/' + ' d' + '\'' + ' /root/.ssh/known_hosts')
    newSsh = "Are you sure you want to continue connecting"
    cmd = 'ssh -l ' + user + ' ' + ip
    if cli_port != '' and cli_port != '22':
        cmd = cmd + ' -p ' + str(cli_port)
    logger.info(cmd)
    ssh = pexpect.spawn(cmd)
    while True:
        try:
            index = ssh.expect([
                pexpect.TIMEOUT, 
                '(yes\/no)', 
                '[pP]assword:\s?$',
                'REMOTE HOST IDEN',
                '--MORE--*',
                '\[redisplay\]*|yes\/no\/redisplay*',
                newSsh,
                'Maximum login attempts exceeded',
                prompt,
                'Please enter old password',
                'Please enter a new password',
                'Please re-enter new password',
            ])
        except:
            logger.info('Could not start ssh to {}'.format(ip))
            return False
        if index == 0: # Timeout
            logger.error('Send command timeout')
            return False
        elif index == 1: # SSH does not have the public key. Just accept it.
            time.sleep(3)
            ssh.sendline ('yes')
            time.sleep(3)
            continue
        elif index == 2: # password
            logger.info('Send routine password...')
            ssh.sendline(password)
            ssh.buffer = b''
            continue
        elif index == 3: 
            logger.info('FIX: .ssh/know_hosts')
            continue
        elif index == 4:
            ssh.send("q")
            continue
        elif index == 5 or index == 6:
            ssh.sendline('yes')
            continue
        elif index == 7:
            logger.info('Maximum login attempts exceeded: ' + 'ssh -l ' + user + ' ' + ip)
            return False                
        elif index == 8:
            logger.info('Successfully login in ' + ip)
            return True,ssh
        elif index == 9:
            ssh.sendline(password)
            continue
        elif index == 10:
            ssh.sendline(new_password)
            continue
        elif index == 11:
            ssh.sendline(new_password)
            continue

def cli_logout(ssh):
    ssh.sendline('exit')
    index = ssh.expect([
                pexpect.TIMEOUT, 
                'User',
            ])
    if index == 1:
        ssh.close()
        return True
    else:
        return False

def config_interface(fw_cli,start,end,zone):
    flage = False
    for i in range(start,end):
        command = ["configure", "interface x{0}".format(i),"ip-assignment {0} static".format(zone),"commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flage = True
        else:
            flage = False
            return flage
    return flage

def show_interface(fw_cli,flage,start,end):
    flage = flage
    for i in range(start,end):
        command = ["show interface x{0}".format(i)]
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "interface X{0}".format(i) in rc[1]:
            flage = True
        else:
            flage = False
            break
    return flage

def show_interface_ip(fw_cli,flage,start,end):
    flage = flage
    for i in range(start,end):
        command = ["show interface x{0}".format(i)]
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "192.168.16{0}.168".format(i) in rc[1]:
            flage = True
        else:
            flage = False
            break
    return flage

def show_interface_zone(fw_cli,flage,start,end,zone):
    flage = flage
    for i in range(start,end):
        sleep(1)
        command = ["show interface x{0}".format(i)]
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "ip-assignment {0} static".format(zone) in rc[1]:
            flage = True
        else:
            flage = False
            break
    return flage