import sys
import hashlib
import ipaddress
import json
import os
import subprocess
import re
import struct
import time
from collections import OrderedDict
from pprint import pprint

import telnetlib
from telnetlib import IAC, NOP

import pexpect
import requests
import urllib3

from networkdevice import *
from runner.settings import logger


class SWOCLI():
    def __init__(self, console_ip, console_port, console_user='console', console_password='console',
                 switch_usename="admin", switch_password="password", supported_config_mode="cli-ssh"):
        self.telnet = telnetlib.Telnet()
        self.console_ip = console_ip
        self.console_port = console_port
        self.console_user = console_user
        self.console_password = console_password
        self.switch_usename = switch_usename
        self.switch_password = switch_password
        self.supported_config_mode = supported_config_mode

        try:
            if not self.supported_config_mode:
                self.console_login()
        except:
            self.console_login()

    def telnet_console_login(self):
        try:

            self.telnet.open(self.console_ip, port=self.console_port)
            self.telnet.read_until(b'login:', timeout=2)
            self.telnet.write(self.console_user.encode('ascii') + b'\n')
            self.telnet.read_until(b'Password:', timeout=2)
            self.telnet.write(self.console_password.encode('ascii') + b'\n')
            time.sleep(1)
            self.telnet.write(" ".encode('ascii') + b'\n')
            self.telnet.expect([b'\s*Password:\s*', b'#'])
            self.telnet.write(self.switch_password.encode('ascii') + b'\n')
            time.sleep(1)
            self.telnet.expect([b'\s*login:\s*', b'#'])
            self.telnet.write(self.switch_usename.encode('ascii') + b'\n')
            self.telnet.expect([b'\s*Password:\s*', b'#'])
            self.telnet.write(self.switch_password.encode('ascii') + b'\n')

        except Exception as e:
            logger.error('server must be specified with port.')
            logger.error(e)
            self.telnet.close()
            return False

        if self.telnet.expect([b'\s*#\s*']):
            self.telnet_authenticated = True
            logger.info('login %s success' % self.console_ip)
            return True
        else:
            self.telnet_authenticated = False
            logger.warning('login %s fail, user or password incorrect' % self.console_ip)
            # self.telnet.close()
            return False

    def console_login(self, errcode=0):

        if self.supported_config_mode == 'cli-ssh':
            return self.ssh_connect(errcode)
        elif self.supported_config_mode == 'cli-telnet':
            return self.console_connect(errcode)
        else:
            logger.error('Make sure supported_config_mode is one of cli-ssh,cli-console')

    def test_change_password(self):
        login = 'ssh -l console ' + self.console_ip + ' -p ' + str(self.console_port)
        logger.info(login)
        self.ssh = pexpect.spawn(login)
        while True:
            try:
                index = self.ssh.expect([
                    pexpect.TIMEOUT,
                    '(yes\/no)',
                    '[pP]assword:\s?$',
                ])
            except:
                logger.info("could not start ssh console")
            if index == 1:
                # SSH does not have the public key. Just accept it.
                self.ssh.sendline('yes')
                self.ssh.expect('yes')
                logger.info("Accepted ssh public key")
                logger.info(self.ssh.before)
                continue
            elif index == 2:
                self.ssh.sendline('console')
                logger.info(self.ssh.before)
                self.ssh.sendline('\n')
                self.ssh.expect(":")
                self.ssh.sendline('admin')
                logger.info(self.ssh.before)
                logger.info("User name is admin")
                self.ssh.expect(":")
                self.ssh.sendline('password')
                logger.info(self.ssh.before)
                self.ssh.sendline('Password@123')
                logger.info(self.ssh.before)
                self.ssh.expect(":")
                self.ssh.sendline('Password@123')
                logger.info("Logged into the switch successfully")
                self.ssh.sendline("exit")
                break
    def ssh_connect(self, errcode=0):
        login = 'ssh -l console ' + self.console_ip + ' -p ' + str(self.console_port)

        logger.info(login)
        self.ssh = pexpect.spawn(login)
        while True:
            try:
                index = self.ssh.expect([
                    pexpect.TIMEOUT,
                    '(yes\/no)',
                    '[pP]assword:\s?$',
                    r'#',
                    r'Would you reboot the device and restore to default config? < y / n >'

                ])
            except:
                logger.info('Could not start ssh to {}'.format(self.console_ip))
                if errcode:
                    return False, 'Could not start ssh'
                return False
            if index == 1:
                # SSH does not have the public key. Just accept it.
                self.ssh.sendline('yes')
                self.ssh.expect('yes')
                logger.info(self.ssh.before)
                continue
            elif index == 2:  # password:
                self.ssh.sendline('console')
                logger.info(self.ssh.before)
                self.ssh.sendline('\n')
                self.ssh.expect(":")
                self.ssh.sendline('admin')
                logger.info(self.ssh.before)
                logger.info("User name is admin")
                self.ssh.expect(":")
                self.ssh.sendline('Password@123')
                logger.info(self.ssh.before)
                logger.info("Password is password")
                self.ssh.expect("#")
                logger.info(self.ssh.before)
                break
        if errcode:
            return False, 'Final fail, no error code got'
        return False

    def single_capture(self, command, customPrompt='#', timeout=10):

        """send single command"""
        logger.info('Send command:' + command)
        # self.flushbuffer()
        output = ""
        time.sleep(15)
        # output=self.ssh.sendline(command)
        self.ssh.sendline(command)
        time.sleep(0.1)
        while True:
            index = self.ssh.expect([b'--\s*More\s*--', b'#', b'.*<y/n>.*', b'.*login:.*'
                                     ],
                                    timeout=timeout)

            try:
                output += bytes.decode(self.ssh.before) + bytes.decode(self.ssh.after)
            except:
                logger.debug('output {} {} not meet the expected match.'.format(self.ssh.before, self.ssh.after))
            if index == 0:  # Timeout
                self.ssh.send(' ')
                continue
            elif index == 1:
                m = self.ssh.before
                break
            elif index == 2:
                logger.info(self.ssh.before)
                break
            elif index == 3:
                logger.info(self.ssh.before)
                continue
            elif index == -1:
                logger.info(self.ssh.before)
            else:
                # time.sleep(2)
                None
        output += bytes.decode(self.ssh.before) + bytes.decode(self.ssh.after)
        return output

    def capture(self, commands, tag=0, timeout=10):
        logger.info(commands)
        self.console_login()
        output = ''
        for command in commands:
            tmp = self.single_capture(command, timeout=timeout)
        self.ssh.sendline("exit")
        return tmp

    def telnet_capture(self, cmd):
        logger.debug("command executed:{0}".format(cmd))
        if self.telnet.eof:
            return None
        (index, match, text) = self.telnet.expect([b'#'], timeout=0.3)
        (index, match, text) = self.telnet.expect([b'--\s*More\s*--', b'#'], timeout=0.3)
        self.telnet.read_until(b"/n", timeout=0.3)
        self.telnet.read_until(b'.*<y/n>.*', timeout=0.3)
        self.telnet.read_until(b'--\s*More\s*--', timeout=0.3)
        self.telnet.read_until(b'#', timeout=0.3)
        self.telnet.write(cmd.encode('ascii') + b'\n')
        time.sleep(2)
        line = b''
        for sleep in range(0, 60):
            (index, match, text) = self.telnet.expect([b'--\s*More\s*--', b'#', b'.*<y/n>.*', b'.*login:.*'], timeout=1)
            print("catpute")
            print(index)
            print(match)
            print(text)
            if index == 0:
                line = line + text
                self.telnet.write(' '.encode('ascii'))
                # time.sleep(2)
            elif index == 1:
                line += text
                break
            elif index == 2:
                line += text
                break
            elif index == 3:
                self.console_login()
                break
            elif index == -1:
                line = line + text
                self.telnet.write(' '.encode('ascii'))
            else:
                # time.sleep(2)
                None
            time.sleep(1)
        logger.debug("capture line")
        logger.debug(line)
        logger.debug('************************')
        logger.debug("stdo out from switch :{0}".format(line.decode('utf-8')))
        logger.debug('************************')
        lines = line.decode('utf-8').splitlines()
        # if line :lines.pop()
        return lines

    def flushbuffer(self):
        self.ssh.buffer = b''

    def telnet_exicute_command(self, cmd):
        self.ssh.write(cmd.encode('ascii') + b'\n')

    # def exicute_command(self, cmd):
    #     #self.ssh.sendline('\n')

    def telnet_get_vlan_information(self):
        show_vlan = "show vlan "
        self.telnet.write(show_vlan.encode('ascii') + b'\n')
        time.sleep(0.2)
        line = b""
        # checking for more command
        while True:
            (index, match, text) = self.telnet.expect([b'\s*#\s*'], timeout=2)
            if index == -1:
                line = line + text
                self.telnet.write(' '.encode('ascii'))
            elif index == 0:
                line += text
                break
            else:
                None
        # --------------fetching vlan info--------------------
        valn_data = {}
        vlan_split = re.split("Vlan ID", str(line))
        for x in range(1, len(vlan_split)):
            # ---------------------valn id----------------------------
            vlan_id = re.search(r'(:)\s*(\d+)', str(vlan_split[x]), re.I)
            valn_data[vlan_id.group(2)] = {}
            # ---------------------Member_Ports-----------------------
            vlan_splitt = vlan_split[x].split("Member Ports        :")
            vlan_splitt = vlan_splitt[1].split("Untagged Ports      :")
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\r\\r\\n', ',')
            vlan_splitt[0] = vlan_splitt[0].replace('\\x1b[100B\\r\\x1b[K\\r--More--\\x1b[K\\x1b\\r', ' ')
            Member_Ports = []
            for interfaces in vlan_splitt[0].split(","):
                if len(interfaces.split()) > 0:
                    Member_Ports.append(interfaces.split()[0])
            valn_data[vlan_id.group(2)]["Member Ports"] = Member_Ports
            # -----------------------Untagged ports------------------------
            vlan_splitt = vlan_split[x].split("Untagged Ports      :")
            vlan_splitt = vlan_splitt[1].split("Forbidden Ports     :")
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\r\\r\\n', ',')
            vlan_splitt[0] = vlan_splitt[0].replace('\\x1b[100B\\r\\x1b[K\\r--More--\\x1b[K\\x1b\\r', ' ')
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\x1b[K', ' ')
            Untagged_Ports = []
            for interfaces in vlan_splitt[0].split(","):
                if len(interfaces.split()) > 0:
                    Untagged_Ports.append(interfaces.split()[0])
            valn_data[vlan_id.group(2)]["Untagged Ports"] = Untagged_Ports

        return valn_data

    def get_vlan_information(self):
        show_vlan = ['show vlan']
        self.telnet.write(show_vlan.encode('ascii') + b'\n')
        time.sleep(0.2)
        line = b""
        # checking for more command
        while True:
            (index, match, text) = self.telnet.expect([b'\s*#\s*'], timeout=2)
            if index == -1:
                line = line + text
                self.telnet.write(' '.encode('ascii'))
            elif index == 0:
                line += text
                break
            else:
                None
        # --------------fetching vlan info--------------------
        valn_data = {}
        vlan_split = re.split("Vlan ID", str(line))
        for x in range(1, len(vlan_split)):
            # ---------------------valn id----------------------------
            vlan_id = re.search(r'(:)\s*(\d+)', str(vlan_split[x]), re.I)
            valn_data[vlan_id.group(2)] = {}
            # ---------------------Member_Ports-----------------------
            vlan_splitt = vlan_split[x].split("Member Ports        :")
            vlan_splitt = vlan_splitt[1].split("Untagged Ports      :")
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\r\\r\\n', ',')
            vlan_splitt[0] = vlan_splitt[0].replace('\\x1b[100B\\r\\x1b[K\\r--More--\\x1b[K\\x1b\\r', ' ')
            Member_Ports = []
            for interfaces in vlan_splitt[0].split(","):
                if len(interfaces.split()) > 0:
                    Member_Ports.append(interfaces.split()[0])
            valn_data[vlan_id.group(2)]["Member Ports"] = Member_Ports
            # -----------------------Untagged ports------------------------
            vlan_splitt = vlan_split[x].split("Untagged Ports      :")
            vlan_splitt = vlan_splitt[1].split("Forbidden Ports     :")
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\r\\r\\n', ',')
            vlan_splitt[0] = vlan_splitt[0].replace('\\x1b[100B\\r\\x1b[K\\r--More--\\x1b[K\\x1b\\r', ' ')
            vlan_splitt[0] = vlan_splitt[0].replace('\\r\\x1b[K', ' ')
            Untagged_Ports = []
            for interfaces in vlan_splitt[0].split(","):
                if len(interfaces.split()) > 0:
                    Untagged_Ports.append(interfaces.split()[0])
            valn_data[vlan_id.group(2)]["Untagged Ports"] = Untagged_Ports

        return valn_data

    def telnet_configure_interface(self, **kwargs):
        interface_name = {"Gi": "gigabitethernet"}
        for key in kwargs.keys():
            self.exicute_command("configure terminal")
            self.telnet.expect([b'\s*config*'])
            self.exicute_command("interface " + "{} {}".format(interface_name[key[0:2]], key[2:6]))
            self.telnet.expect([b'\s*config-if*'])

            if 'shutdown' in kwargs[key].keys():
                if kwargs[key]["shutdown"] == True:
                    self.exicute_command("shutdown")
                else:
                    self.exicute_command("no shutdown")
                self.telnet.expect([b'\s*config-if*'])

            self.exicute_command("exit")
            # self.telnet.expect([b'\s*config*'])#this line is not working properly
            self.exicute_command("exit")
            self.telnet.expect([b'\s*#*'])
        return True

    def configure_interface(self, **kwargs):
        
        interface_name = {"Gi": "gigabitethernet"}
        for key in kwargs.keys():
        
            self.capture(["configure terminal"])
            self.capture(["interface {} {}".format(interface_name[key[0:2]], key[2:6])])

            if 'shutdown' in kwargs[key].keys():
                if kwargs[key]["shutdown"] == True:
                    self.capture(["shutdown"])
            else:
                self.capture(["no shutdown"])

            self.capture(["exit"])
        return True

    def telnet_configure_range_of_interfaces(self, **kwargs):
        interface_name = {"Gi": "gigabitethernet"}
        for key in kwargs.keys():
            print(key)
            print(key[2:-1])
            self.exicute_command("configure terminal")
            self.telnet.expect([b'\s*config*'])
            self.exicute_command("interface " + "range " + "{} {}".format(interface_name[key[0:2]], key[2:]))
            self.telnet.expect([b'\s*config-if*'])

            if 'shutdown' in kwargs[key].keys():
                if kwargs[key]["shutdown"] == True:
                    self.exicute_command("shutdown")
                else:
                    self.exicute_command("no shutdown")
                self.telnet.expect([b'\s*config-if*'])

            self.exicute_command("exit")
            self.telnet.expect([b'\s*config'])  # this line is not working properly
            self.exicute_command("exit")
            self.telnet.expect([b'\s*#*'])
        return True

    def configure_range_of_interfaces(self, **kwargs):
        interface_name = {"Gi": "gigabitethernet"}

        for key in kwargs.keys():
            self.capture(["configure terminal"])
            self.capture(["interface {} {}".format(interface_name[key[0:2]], key[2:6])])

            if 'shutdown' in kwargs[key].keys():
                if kwargs[key]["shutdown"] == True:
                    self.capture(["shutdown"])
                else:
                    self.capture(["no shutdown"])

            self.capture(["exit"])
        return True

    def configure_vlan(self):
        pass

    def telnet_get_interface_information(self):
        show_interface = "show interfaces status "
        lines = self.capture(show_interface)
        interface_detailes = {}
        for line in lines:
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(connected|not connected)\s*', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["speed"] = re.search(
                    r'(\d+\s(Gbps|Mbps))', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["duplex"] = re.search(
                    r'(Full|Half)', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))][
                    "Negotiation"] = re.search(r'(Auto|No-Negotiation)', line, re.I).group(1)
                if re.search(r'(Auto-MDIX on)', line, re.I):
                    interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))][
                        "capability"] = re.search(r'(Auto-MDIX on)', line, re.I).group(1)

        logger.debug("switch interfaces informations")
        logger.debug(interface_detailes)
        return interface_detailes

    def get_interface_information(self):
        show_interface = ['show interfaces status']
        lines = self.capture(show_interface)
        interface_detailes = {}
        for line in lines.split('\n'):
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(connected|not connected)\s*', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["speed"] = re.search(
                    r'(\d+\s(Gbps|Mbps))', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["duplex"] = re.search(
                    r'(Full|Half)', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))][
                    "Negotiation"] = re.search(r'(Auto|No-Negotiation)', line, re.I).group(1)
                if re.search(r'(Auto-MDIX on)', line, re.I):
                    interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))][
                        "capability"] = re.search(r'(Auto-MDIX on)', line, re.I).group(1)

        logger.debug("switch interfaces informations")
        logger.debug(interface_detailes)
        return interface_detailes

    def get_connected_interfaces(self):
        up_interface = []
        all_interfaces = self.get_interface_information()
        for inter in all_interfaces.keys():
            if all_interfaces[inter]["status"] == "connected":
                up_interface.append(inter)
        logger.debug("connected interfaces")
        logger.debug(up_interface)
        return up_interface

    def telnet_get_dot1x_port_config(self):
        show_interface = "show dot1x all"
        lines = self.capture(show_interface)
        dot1x_port_status = {}
        interface = ""
        for line in lines:
            if re.search(r'(Dot1x Info for (te|gi)\s*\d\/\d+)', line, re.I):
                interface = re.search(r'(Dot1x Info for ((te|gi)\s*\d\/\d+))', line, re.I).group(2)
                dot1x_port_status[interface] = {}
            if re.search(
                    r'(((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s)(.+))',
                    line, re.I):
                dot1x_port_status[interface][re.search(
                    r'((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s(.+))',
                    line, re.I).group(2)] = re.search(
                    r'((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s(.+))',
                    line, re.I).group(3)
        return dot1x_port_status

    def get_dot1x_port_config(self):
        show_interface = ['show dot1x all']
        lines = self.capture(show_interface)
        dot1x_port_status = {}
        interface = ""
        for line in lines.split('\n'):
            if re.search(r'(Dot1x Info for (te|gi)\s*\d\/\d+)', line, re.I):
                interface = re.search(r'(Dot1x Info for ((te|gi)\s*\d\/\d+))', line, re.I).group(2)
                dot1x_port_status[interface] = {}
            if re.search(
                    r'(((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s)(.+))',
                    line, re.I):
                dot1x_port_status[interface][re.search(
                    r'((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s(.+))',
                    line, re.I).group(2)] = re.search(
                    r'((AuthMode|PortStatus|AccessControl|AuthSM State|SuppSM State|BendSM State|AuthPortStatus|SuppPortStatus|AdminControlDirection|OperControlDirection|MaxReq|Port Control|GuestVlan|QuietPeriod|Re-authentication|ReAuthPeriod|ServerTimeout|SuppTimeout|Tx Period)\s+=\s(.+))',
                    line, re.I).group(3)
        return dot1x_port_status

    def telnet_get_port_security_port_settings(self):
        show_interface = "show interface port-security"
        lines = self.capture(show_interface)
        port_security_port_status = {}
        for line in lines:
            if re.search(r'((te|gi)\s*\d\/\d+)', line, re.I):

                port_security_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)] = {}
                # logger.debug(line)
                temp = re.sub(r'[\s]+', ' ', line)
                temp = re.sub(r"'", ' ', temp)
                temp = re.sub(r"\\x1b\[K", ' ', temp)
                temp = re.sub(r"Mac Limit is", 'Mac_Limit_is', temp)
                temp = temp.split(" ")
                values = []
                for key in temp:
                    if key:
                        values.append(key)
                port_security_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)][values[1]] = values[2]

        return port_security_port_status

    def get_port_security_port_settings(self):
        show_interface = ['show interface port-security']
        lines = self.capture(show_interface)
        port_security_port_status = {}
        for line in lines.split('\n'):
            if re.search(r'((te|gi)\s*\d\/\d+)', line, re.I):

                port_security_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)] = {}
                # logger.debug(line)
                temp = re.sub(r'[\s]+', ' ', line)
                temp = re.sub(r"'", ' ', temp)
                temp = re.sub(r"\\x1b\[K", ' ', temp)
                temp = re.sub(r"Mac Limit is", 'Mac_Limit_is', temp)
                temp = temp.split(" ")
                values = []
                for key in temp:
                    if key:
                        values.append(key)
                port_security_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)][values[1]] = values[2]

        return port_security_port_status

    def telnet_get_interface_protocol_staus_description(self):
        # not written for descriptions
        show_interface = "show interfaces description "
        lines = self.capture(show_interface)
        interface_detailes = {}
        # print(lines)
        for line in lines:
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(up|down)\s*', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["protocol"] = \
                    re.findall(r'(up|down)', line, re.I)[1]
        logger.debug(interface_detailes)
        return interface_detailes

    def get_interface_protocol_staus_description(self):
        # not written for descriptions
        show_interface = ['show interfaces description']
        lines = self.capture(show_interface)
        interface_detailes = {}
        # print(lines)
        for line in lines.split('\n'):
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(up|down)\s*', line, re.I).group(1)
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["protocol"] = \
                    re.findall(r'(up|down)', line, re.I)[1]
        logger.debug(interface_detailes)
        return interface_detailes

    def windows_ping(self, host, source_ip):
        output = os.popen('ping {} -S {}'.format(host, source_ip)).read()
        logger.debug("stdo out for pinging")
        logger.debug(output)
        if re.search(r'Approximate round trip times in milli-seconds', output):
            logger.info('Ping is successful.')
            return True
        else:
            logger.info('Ping failed')
            return False

    def linux_ping(self, host, insterface):
        output = os.popen('ping {} -I {} -c 3'.format(host, insterface)).read()
        logger.debug("stdo out for pinging")
        logger.debug(output)
        if re.search(r' 0% packet loss', output):
            logger.info('Ping is successful.')
            return True
        else:
            logger.info('Ping failed')
            return False

    def windows_interface_restart(self, interface):
        logger.info("clinet interface is restarting")
        output = subprocess.Popen('ipconfig /release {}'.format(interface))
        time.sleep(10)
        logger.debug(output)
        output.kill()
        output = subprocess.Popen('ipconfig /renew {}'.format(interface))
        time.sleep(10)
        logger.debug(output)
        output.kill()

    def linux_renew_ip(self, interface):
        logger.info("clinet interface {} is nenewing ip".format(interface))
        output = os.popen('dhclient  -r {} '.format(interface)).read()
        logger.debug("stdo out for releasing ip")
        logger.debug(output)
        output = os.popen('dhclient {} '.format(interface)).read()
        logger.debug("stdo out for nenew ip")
        logger.debug(output)
        ip = self.liniux_interface_ip(interface)
        logger.debug("IP: {}".format(ip))
        print(ip)
        if ip:
            return True
        else:
            return False

    def remot_pc_ping_test(self, host, destination="192.168.168.168", interface="eth1", return_ifc_ip=False):
        ssh = Host(host)
        logger.info("remote clinet interface {} is nenewing ip".format(interface))
        output = ssh.send_command('dhclient  -r {} '.format(interface))
        output = ssh.send_command('dhclient {} '.format(interface))
        output = ssh.send_command('ifconfig')
        print(str(output))
        output = re.split("{0}".format(interface), output)
        if 2 <= len(output):
            re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
            ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
        logger.info(ip)
        # if 2 <= len(output):
        #     re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
        #     ip=re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
        # print("The ip of remot client {} with adapter {} is {}".format(host,interface,ip))
        output = ssh.send_command('ping {} -I {} -c 3'.format(destination, interface))
        if re.search(r' 0% packet loss', str(output)):
            if return_ifc_ip:
                logger.debug('Ping is successful.')
                return True, ip
            else:
                logger.debug('Ping is successful.')
                return True
        else:
            if return_ifc_ip:
                logger.debug('Ping failed')
                return False, ip
            else:
                logger.debug('Ping failed')
                return False

    def windows_interface_ip(self, interface):
        output = os.popen('ipconfig').read()
        output = re.split("Ethernet adapter {0}".format(interface), output)
        if 2 <= len(output):
            re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
            ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
        return ip

    def liniux_interface_ip(self, interface):
        output = os.popen('ifconfig').read()
        output = re.split("{0}".format(interface), output)
        if 2 <= len(output):
            re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
            ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', output[1], re.I).group(1)
        return ip

    def get_system_information(self):
        show_interface = ["show system information"]
        time.sleep(50)
        lines = self.capture(show_interface)
        system_information = {}
        for line in lines.split('\n'):
            if re.search(r'(Serial Nums)', line, re.I):
                system_information["serial number"] = re.search(r'(:\s)(\w+)', line, re.I).group(2)
        return system_information


    def telnet_is_switch_up(self):
        logger.info("switch is restarting..........")
        for sleep in range(0, 10):
            output = self.get_system_information()
            if "serial number" in output:
                logger.debug("switch is up...")
                return True
            else:
                logger.debug("switch is down...")
                time.sleep(1)
        return False

    def is_switch_up(self):

        logger.info("switch is restarting..........")
        time.sleep(20)
        output = self.get_system_information()
        logger.info("Printing output in is_switch_up", output)
        if "Serial Nums" in output:
            logger.debug("switch is up...")
            return True
        else:
            logger.debug("switch is down...")
            time.sleep(1)

        return output

    def telnet_get_system_information(self):
        show_interface = "show system information"
        lines = self.capture(show_interface)
        system_information = {}
        for line in lines:
            if re.search(r'(Serial Nums)', line, re.I):
                system_information["serial number"] = re.search(r'(:\s)(\w+)', line, re.I).group(2)
        return system_information

    def telnet_get_voice_vlan_port_status(self):
        show_interface = "show voice vlan"
        lines = self.capture(show_interface)
        voice_vlan_port_status = {}
        for line in lines:
            if re.search(r'((te|gi)\s*\d\/\d+)', line, re.I):

                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)] = {}
                # print(line)
                temp = re.sub(r'[\s]+', ' ', line)
                temp = re.sub(r"'", ' ', temp)
                temp = temp.split(" ")
                values = []
                for key in temp:
                    if key:
                        values.append(key)
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Enabled"] = values[1]
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Activated"] = values[2]
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Cos Mode"] = values[3]

        return voice_vlan_port_status

    def get_poe_inline(self):
        show_poe_inline = ["show power inline"]
        lines = self.capture(show_poe_inline)
        b = []
        for item in lines.split('\n'):
            c = re.findall(
                r"[0-9]+.\s+[a-z]+\s+[a-z]+\s+[a-z]+\s[a-z]+\s+[a-z0-9()]+\s+[a-z0-9]+\s+[.0-9]+\s+[0-9]+\s+[.0-9]+",
                item, re.I)
            d = re.findall(
                r"[0-9]+.\s+[a-z]+\s+[a-z]+\s+[a-z]+\s[a-z]+\s+[A-Za-z0-9()]+\s+[a-z0-9]+\s+[-]\s+[.0-9]+\s+[0-9]+\s+[.0-9]+",
                item, re.I)
            if c:
                # Replace whitespace character to spaces
                temp = re.sub(r'[\s]+', ' ', c[0])

                temp = re.sub(r"Auto Class", "Auto-Class", temp)
                b.append(temp.split(" "))
            if d:
                temp = re.sub(r'[\s]+', ' ', d[0])
                temp = re.sub(r"User defined", "User-defined", temp)
                t = temp.split(" ")
                temp = temp.replace(t[4], '')
                temp = re.sub("User-defined", "User-defined|" + t[4], temp)
                b.append(temp.split(" "))
        return_string = {}
        temp = {}
        header = ['Port', 'State', 'Priority', 'Power-Limit-type', 'Status', 'Class', 'Voltage(V)', 'Current(mA)',
                  'Power(W)']
        for index, i in enumerate(b):
            temp = {}
            index2 = 0
            flag = False
            for j in i:
                if flag == True:
                    flag = False
                    continue
                if index2 == 3:
                    t = j.split("|")
                    if t[0] == 'Auto-Class':
                        temp[header[index2]] = {t[0]: ""}
                    elif t[0] == 'User-defined':
                        temp[header[index2]] = {t[0]: t[1]}
                        flag = True
                else:
                    temp[header[index2]] = j
                return_string[index + 1] = temp
                index2 += 1
        return return_string

    def telnet_get_poe_inline(self):
        show_interface = "show power inline"
        lines = self.capture(show_interface)
        b = []
        for item in lines:
            c = re.findall(
                r"[0-9]+.\s+[a-z]+\s+[a-z]+\s+[a-z]+\s[a-z]+\s+[a-z0-9()]+\s+[a-z0-9]+\s+[.0-9]+\s+[0-9]+\s+[.0-9]+",
                item, re.I)
            d = re.findall(
                r"[0-9]+.\s+[a-z]+\s+[a-z]+\s+[a-z]+\s[a-z]+\s+[A-Za-z0-9()]+\s+[a-z0-9]+\s+[-]\s+[.0-9]+\s+[0-9]+\s+[.0-9]+",
                item, re.I)
            if c:
                # Replace whitespace character to spaces
                temp = re.sub(r'[\s]+', ' ', c[0])

                temp = re.sub(r"Auto Class", "Auto-Class", temp)
                b.append(temp.split(" "))
            if d:
                temp = re.sub(r'[\s]+', ' ', d[0])
                temp = re.sub(r"User defined", "User-defined", temp)
                t = temp.split(" ")
                temp = temp.replace(t[4], '')
                temp = re.sub("User-defined", "User-defined|" + t[4], temp)
                b.append(temp.split(" "))
        return_string = {}
        temp = {}
        header = ['Port', 'State', 'Priority', 'Power-Limit-type', 'Status', 'Class', 'Voltage(V)', 'Current(mA)',
                  'Power(W)']
        for index, i in enumerate(b):
            temp = {}
            index2 = 0
            flag = False
            for j in i:
                if flag == True:
                    flag = False
                    continue
                if index2 == 3:
                    t = j.split("|")
                    if t[0] == 'Auto-Class':
                        temp[header[index2]] = {t[0]: ""}
                    elif t[0] == 'User-defined':
                        temp[header[index2]] = {t[0]: t[1]}
                        flag = True
                else:
                    temp[header[index2]] = j
                return_string[index + 1] = temp
                index2 += 1
        return return_string

    def chek_traffic_path(self, exclude_interfaces):
        pass_interfaces = []
        up_interface = self.get_connected_interfaces()
        windows_interface_ip = self.windows_interface_ip("Ethernet1")
        for port in exclude_interfaces:
            up_interface.remove(port)
        logger.warning("interfaces participating in traffic path test")
        logger.warning(up_interface)
        for interface in up_interface:
            interface_config = {interface: {"shutdown": True}}
            self.configure_interface(**interface_config)
        for interface in up_interface:
            logger.info("sending traffic through " + str(interface))
            interface_config = {interface: {"shutdown": False}}
            self.configure_interface(**interface_config)
            try:
                self.windows_interface_restart("Ethernet1")
                windows_interface_ip = self.windows_interface_ip("Ethernet1")
                ping_result = self.windows_ping("8.8.8.8", windows_interface_ip)
                if ping_result:
                    pass_interfaces.append(interface)
                logger.debug(ping_result)

            except Exception as e:
                logger.debug("traffic flow have issue")
                logger.debug(e)

            interface_config = {interface: {"shutdown": True}}
            self.configure_interface(**interface_config)
        for interface in up_interface:
            interface_config = {interface: {"shutdown": False}}
            self.configure_interface(**interface_config)

        return pass_interfaces


    def get_switch_ip(self):

        show_ip = ["show ip interface"]
        ip_info = {}
        vlan = "vlan "
        lines = self.capture(show_ip)
        for line in lines.split('\n'):
            if re.search(r'((te|Gi)\d\/\d+)', line, re.I):
                vlan = re.search(r'(te|gi\d\/\d+)', line, re.I).group(1)
            if re.search(r'(vlan)(\d)', line):
                vlan = vlan + re.search(r'(vlan)(\d)', line).group(2)
            if re.search(r'(Internet Address is)(\s\d+.\d+)', line):
                ip_info[vlan] = re.search(r'(Internet Address is\s)(\d+.\d+.\d+.\d+)', line).group(2)
                vlan = "vlan "
        logger.debug("ip_info: {}".format(ip_info))
        return ip_info

    def telnet_get_switch_ip(self):

        show_ip = "show ip interface"
        ip_info = {}
        vlan = "vlan "
        lines = self.capture(show_ip)
        for line in lines:
            if re.search(r'((te|Gi)\d\/\d+)', line, re.I):
                vlan = re.search(r'(te|gi\d\/\d+)', line, re.I).group(1)
            if re.search(r'(vlan)(\d)', line):
                vlan = vlan + re.search(r'(vlan)(\d)', line).group(2)
            if re.search(r'(Internet Address is)(\s\d+.\d+)', line):
                ip_info[vlan] = re.search(r'(Internet Address is\s)(\d+.\d+.\d+.\d+)', line).group(2)
                vlan = "vlan "
        logger.debug("ip_info: {}".format(ip_info))
        return ip_info

    def telnet_get_port_isolation_status(self):
        # not written for descriptions
        show_port_isolation = "show port-isolation status "
        lines = self.capture(show_port_isolation)
        interface_detailes = {}
        for line in lines:
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(enable|disable)\s*', line, re.I).group(1)

        return interface_detailes

    def get_port_isolation_status(self):
        show_port_isolation = ["show port-isolation status "]
        lines = self.capture(show_port_isolation)
        interface_detailes = {}
        for line in lines.split('\n'):
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I):
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))] = {}
                interface_detailes[str(re.search(r'(te|gi\s*\d\/\d+)', line, re.I).group(1))]["status"] = re.search(
                    r'(enable|disable)\s*', line, re.I).group(1)

        return interface_detailes

    def get_interfaces_storm_control_settings(self):
        show_interface = ["show interfaces storm-control"]
        lines = self.capture(show_interface)
        storm_control_settings = {}
        interface = ""
        for line in lines.split('\n'):
            if re.search(r'((te|gi)\s*\d\/\d+)', line, re.I):
                interface = re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)
                storm_control_settings[interface] = {}

            if re.search(
                    r'((DLF Storm Control|Broadcast Storm Control|Broadcast Storm Control Limit|Multicast Storm Control|Unknown Multicast Storm Control)\s*)',
                    line, re.I):
                storm_control_settings[interface][re.search(
                    r'((DLF Storm Control|DLF Storm Control Limit|Broadcast Storm Control|Broadcast Storm Control Limit|Multicast Storm Control|Multicast Storm Control Limit|Unknown Multicast Storm Control|Unknown Multicast Storm Control Limit)\s*:\s*(.*))',
                    line, re.I).group(2)] = re.search(
                    r'((DLF Storm Control|DLF Storm Control Limit|Broadcast Storm Control|Broadcast Storm Control Limit|Multicast Storm Control|Multicast Storm Control Limit|Unknown Multicast Storm Control|Unknown Multicast Storm Control Limit)\s*:\s*(.*))',
                    line, re.I).group(3)
        return storm_control_settings

    def telnet_get_interfaces_rate_limit(self):
        show_interfaces_rate_limit = "show interfaces rate-limit"
        lines = self.capture(show_interfaces_rate_limit)
        interface_rate_limit = {}
        for line in lines.split('\n'):
            if re.search(r'(te|gi)\d\/\d+', line, re.I):
                interface = re.search(r'((te|gi)\d\/\d+)', line, re.I).group(1)
                interface_rate_limit[interface] = {}
            if re.search(r'Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size', line, re.I):
                interface_rate_limit[interface][
                    re.search(r'(Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size)', line,
                              re.I).group(0)] = re.search(r'(\d+\s+[a-z]+)', line, re.I).group(0)
        # logger.debug(interface_rate_limit)
        return interface_rate_limit

    def get_interfaces_rate_limit(self):
        show_interfaces_rate_limit = "show interfaces rate-limit"
        lines = self.capture(show_interfaces_rate_limit)
        interface_rate_limit = {}
        for line in lines:
            if re.search(r'(te|gi)\d\/\d+', line, re.I):
                interface = re.search(r'((te|gi)\d\/\d+)', line, re.I).group(1)
                interface_rate_limit[interface] = {}
            if re.search(r'Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size', line, re.I):
                interface_rate_limit[interface][
                    re.search(r'(Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size)', line,
                              re.I).group(0)] = re.search(r'(\d+\s+[a-z]+)', line, re.I).group(0)
        # logger.debug(interface_rate_limit)
        return interface_rate_limit

    def get_interfaces_rate_limit(self):
        # not written for descriptions
        show_interfaces_rate_limit = ["show interfaces rate-limit"]
        lines = self.capture(show_interfaces_rate_limit)
        interface_rate_limit = {}
        for line in lines.split('\n'):
            if re.search(r'(te|gi)\d\/\d+', line, re.I):
                interface = re.search(r'((te|gi)\d\/\d+)', line, re.I).group(1)
                interface_rate_limit[interface] = {}
            if re.search(r'Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size', line, re.I):
                interface_rate_limit[interface][
                    re.search(r'(Ingress Rate Limit|Ingress Burst size|Egress Rate Limit|Egress Burst Size)', line,
                              re.I).group(0)] = re.search(r'(\d+\s+[a-z]+)', line, re.I).group(0)
        # logger.debug(interface_rate_limit)
        return interface_rate_limit

    def telnet_factory_restore(self):
        commands = ['restore-defaults']
        for command in ['y']:
            commands.append(command)
        result = self.capture(commands)

        resp = json.dumps(result)
        return resp

    def factory_restore(self):
        commands = ['restore-defaults']
        for command in ['y']:
            commands.append(command)
        result = self.capture(commands)
        resp = json.dumps(result)
        return resp

    def factory_restore_auto_authorize(self):
        commands = ['restore-defaults']
        for command in ['y']:
            commands.append(command)
        result = self.capture(commands)
        resp = json.dumps(result)
        return resp

    def get_voice_vlan_port_status(self):
        command = ["show voice vlan"]
        lines = self.capture(command)
        print(lines)
        voice_vlan_port_status = {}
        for line in lines.split('\n'):
            if re.search(r'((te|gi)\s*\d\/\d+)', line, re.I):

                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)] = {}
                # print(line)
                temp = re.sub(r'[\s]+', ' ', line)
                temp = re.sub(r"'", ' ', temp)
                temp = temp.split(" ")
                values = []
                for key in temp:
                    if key:
                        values.append(key)
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Enabled"] = values[1]
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Activated"] = values[2]
                voice_vlan_port_status[re.search(r'((te|gi)\s*\d\/\d+)', line, re.I).group(1)]["Cos Mode"] = values[3]
        convert_dict = json.dumps(voice_vlan_port_status)
        return convert_dict


class Telnet_Network_sw(SWOCLI):
    def get_network_info_from_sw(self):
        show_ip_interface = "show ip interface "
        lines = super().capture(show_ip_interface)
        network = {}
        for line in lines:
            if re.search(r'(vlan)(\d+)', line, re.I):
                vlan_id = re.search(r'(vlan)(\d+)', line, re.I).group(2)
                network[vlan_id] = {}

            if re.search(r'(vlan)(\d+)(\s+)(is)(\s+)(up)', line, re.I):
                vlan_status = "vlan_status"
                network[vlan_id][vlan_status] = re.search(r'(vlan)(\d+)(\s+)(is)(\s+)(up)', line, re.I).group(6)

            if re.search(r'(line\s+protocol)(\s+)(is)(\s+)(up)', line, re.I):
                line_protocol = "line_protocol"
                network[vlan_id][line_protocol] = re.search(r'(line\s+protocol)(\s+)(is)(\s+)(up)', line, re.I).group(5)

            if re.search(r'(internet\s+address)(\s+is\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d+)', line, re.I):
                ip = "ip"
                network[vlan_id][ip] = re.search(
                    r'(internet\s+address)(\s+is\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d+)', line, re.I).group(3)

            if re.search(r'(broadcast\s+address\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I):
                broadcast_ip = "broadcast_ip"
                network[vlan_id][broadcast_ip] = re.search(
                    r'(broadcast\s+address\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I).group(2)

            if re.search(r'(ip\s+address\s+allocation\s+method\s+is\s+)(dynamic)', line, re.I):
                allocation = "allocation"
                network[vlan_id][allocation] = re.search(r'(ip\s+address\s+allocation\s+method\s+is\s+)(dynamic)', line,
                                                         re.I).group(2)

            if re.search(r'(ip\s+address\s+allocation\s+protocol\s+is\s+)(dhcp)', line, re.I):
                protocol = "protocol"
                network[vlan_id][protocol] = re.search(r'(ip\s+address\s+allocation\s+protocol\s+is\s+)(dhcp)', line,
                                                       re.I).group(2)
        return network

    def get_dns_info_from_sw(self):
        show_dns = "show ip dns name-server"
        lines = super().capture(show_dns)
        dns = {}
        for line in lines:
            if re.search(r'(\s+\d\s+)', line, re.I):
                index = re.search(r'((\s+)(\d)(\s+))', line, re.I).group(3)

                if re.search(r'(\s+\d\s+\t+\s+ipv4)', line, re.I):
                    dns[index] = {}
                    Address_type = "Address type"
                    dns[index][Address_type] = re.search(r'((\s+\d\s+\t+\s+)(ipv4))', line, re.I).group(3)

                # print(re.search(r'((\s+\d\s+\t+\s+)(ipv4))', line, re.I).group(3))

                if re.search(r'(\s+\d\s+\t+\s+ipv4\t\t\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I):
                    ip_address = "ip address"
                    dns[index][ip_address] = re.search(
                        r'(\s+\d\s+\t+\s+ipv4\t\t\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(2)
        # print(re.search(r'(\s+1\s+\t+\s+ipv4\t\t\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).groups())
        return dns


class Telnet_STP(SWOCLI):
    def get_stp_summary(self):
        show_ip_interface = "show spanning-tree summary"
        lines = super().capture(show_ip_interface)
        stp_summary = {}
        instance = ""
        for line in lines:
            if re.search(r'Spanning tree enabled protocol is\s+([a-z]+)', line, re.I):
                stp_summary["protocol"] = re.search(r'Spanning tree enabled protocol is\s+([a-z]+)', line, re.I).group(
                    1)

            if re.search(r'MST\d+', line, re.I):
                instance = re.search(r'MST\d+', line, re.I).group()
                stp_summary[instance] = {}
            if re.search(r'(te|gi)\d\/\d+', line, re.I):
                if instance:
                    interface = re.search(r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(1)
                    stp_summary[instance][interface] = {}
                    stp_summary[instance][interface]["Port-Role"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(3)
                    stp_summary[instance][interface]["Port-State"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(4)
                    stp_summary[instance][interface]["Port-Status"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(5)

                else:
                    interface = re.search(r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(1)
                    stp_summary[interface] = {}
                    stp_summary[interface]["Port-Role"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(3)
                    stp_summary[interface]["Port-State"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(4)
                    stp_summary[interface]["Port-Status"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(5)
        return stp_summary

    def get_stp_status(self):
        cmd = "show spanning-tree"
        lines = super().capture(cmd)
        stp_summary = {}
        for line in lines:
            if re.search(r'.*Spanning tree Protocol has been disabled.*', line, re.I):
                stp_summary["state"] = False
            else:
                stp_summary["state"] = True

            if re.search(r'.*Bridge is executing the rstp compatible Rapid Spanning Tree Protocol.*', line, re.I):
                stp_summary["protocol"] = "RSTP"
            if re.search(r'.*MST00 is executing the mstp compatible Multiple Spanning Tree Protocol.*', line, re.I):
                stp_summary["protocol"] = "MSTP"
            # else:
            #     stp_summary["protocol"]="Unknown"

        return stp_summary


class Telnet_Upgrade(SWOCLI):
    def tftp(self):
        show_ip_interface = "firmware upgrade %s "
        lines = super().capture(show_ip_interface)


class Telnet_StaticMAcAddress(SWOCLI):
    def get_static_mac_info(self):
        show_static_mac = "show mac-address-table static unicast "
        lines = super().capture(show_static_mac)
        static_mac = {}
        for line in lines:
            if re.search(r'(\d+)', line, re.I):
                vlan_id = re.search(r'(\d+)', line, re.I).group(1)
                static_mac[vlan_id] = {}
            if re.search(r'(\d+)', line, re.I):
                mac = re.search(r'(\d+)', line, re.I).group(1)
                static_mac[mac] = {}

        return static_mac


class Telnet_Macaddress(SWOCLI):
    def macAdressStaticUnicastTable(self):
        show_ip_route = "show mac-address-table static unicast"
        lines = super().capture(show_ip_route)
        print(lines)
        mac_Adress_Static_Unicast_Table = {}
        for line in lines:
            print("god please make it work")
            print(line)
            if re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I):
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(
                        3)] = {}
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Vlan'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(2)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Mac Address'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                               re.I).group(3)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Type'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(4)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'ConnectionId'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                                re.I).group(5)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Ports'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                         re.I).group(6)
                print("yah it may work")
        return mac_Adress_Static_Unicast_Table

    def macAdressDynamicTable(self):
        show_ip_route = "show mac-address-table"
        lines = super().capture(show_ip_route)
        print(lines)
        mac_Adress_Static_Unicast_Table = {}
        for line in lines:
            print("god please make it work")
            print(line)
            if re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I):
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(
                        3)] = {}
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Vlan'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(2)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Mac Address'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                               re.I).group(3)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Type'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(4)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'ConnectionId'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                                re.I).group(5)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Ports'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                         re.I).group(6)
        print(mac_Adress_Static_Unicast_Table)
        return mac_Adress_Static_Unicast_Table

    def macAgingTime(self):
        show_ip_route = "show mac-address-table aging-time"
        lines = super().capture(show_ip_route)
        mac_Adress_aging_time = {}
        for line in lines:
            if re.search(r'(Mac Address Aging Time)', line, re.I):
                mac_Adress_aging_time[
                    re.search(r'((Mac Address Aging Time)\s*:\s*(.*))', line, re.I).group(2)] = re.search(
                    r'((Mac Address Aging Time)\s*:\s*(.*))', line, re.I).group(3)
        return mac_Adress_aging_time


class Telnet_User(SWOCLI):
    def listUsers(self):
        show_ip_route = "listuser"
        lines = super().capture(show_ip_route)
        users_list = {}
        for line in lines:

            if re.search(r'((\w+)\s+(\d+).*)', line, re.I):
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)] = {}
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)]['user'] = re.search(
                    r'((\w+)\s+(\d+).*)', line, re.I).group(2)
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)]['privilege'] = re.search(
                    r'((\w+)\s+(\d+).*)', line, re.I).group(3)
        return users_list


class Telnet_StaticRoute(SWOCLI):
    def get_staticroute_info_from_sw(self):
        show_ip_route = "show ip route "
        lines = super().capture(show_ip_route)
        staticroute = {}
        for line in lines:
            if re.search(r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                         re.I):
                staticroute["destination_ip"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(2)
                staticroute["subnet_mask"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(3)
                staticroute["gateway"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(4)
            if re.search(r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*)', line, re.I):
                print(re.search(r'(.* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*)', line, re.I).groups())

        return staticroute


class Network_sw(SWOCLI):
    def get_network_info_from_sw(self):
        show_ip_interface = ['show ip interface']
        lines = self.capture(show_ip_interface)
        network = {}
        for line in lines.split('\n'):
            if re.search(r'(vlan)(\d+)', line, re.I):
                vlan_id = re.search(r'(vlan)(\d+)', line, re.I).group(2)
                network[vlan_id] = {}

            if re.search(r'(vlan)(\d+)(\s+)(is)(\s+)(up)', line, re.I):
                vlan_status = "vlan_status"
                network[vlan_id][vlan_status] = re.search(r'(vlan)(\d+)(\s+)(is)(\s+)(up)', line, re.I).group(6)

            if re.search(r'(line\s+protocol)(\s+)(is)(\s+)(up)', line, re.I):
                line_protocol = "line_protocol"
                network[vlan_id][line_protocol] = re.search(r'(line\s+protocol)(\s+)(is)(\s+)(up)', line, re.I).group(5)

            if re.search(r'(internet\s+address)(\s+is\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d+)', line, re.I):
                ip = "ip"
                network[vlan_id][ip] = re.search(
                    r'(internet\s+address)(\s+is\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d+)', line, re.I).group(3)

            if re.search(r'(broadcast\s+address\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I):
                broadcast_ip = "broadcast_ip"
                network[vlan_id][broadcast_ip] = re.search(
                    r'(broadcast\s+address\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I).group(2)

            if re.search(r'(ip\s+address\s+allocation\s+method\s+is\s+)(dynamic)', line, re.I):
                allocation = "allocation"
                network[vlan_id][allocation] = re.search(r'(ip\s+address\s+allocation\s+method\s+is\s+)(dynamic)', line,
                                                         re.I).group(2)

            if re.search(r'(ip\s+address\s+allocation\s+protocol\s+is\s+)(dhcp)', line, re.I):
                protocol = "protocol"
                network[vlan_id][protocol] = re.search(r'(ip\s+address\s+allocation\s+protocol\s+is\s+)(dhcp)', line,
                                                       re.I).group(2)
        return network

    def get_dns_info_from_sw(self):
        show_dns = ['show ip dns name-server']
        lines = self.capture(show_dns)
        dns = {}
        for line in lines.split('\n'):
            if re.search(r'(\s+\d\s+)', line, re.I):
                index = re.search(r'((\s+)(\d)(\s+))', line, re.I).group(3)

                if re.search(r'(\s+\d\s+\t+\s+ipv4)', line, re.I):
                    dns[index] = {}
                    Address_type = "Address type"
                    dns[index][Address_type] = re.search(r'((\s+\d\s+\t+\s+)(ipv4))', line, re.I).group(3)

                # print(re.search(r'((\s+\d\s+\t+\s+)(ipv4))', line, re.I).group(3))

                if re.search(r'(\s+\d\s+\t+\s+ipv4\t\t\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, re.I):
                    ip_address = "ip address"
                    dns[index][ip_address] = re.search(
                        r'(\s+\d\s+\t+\s+ipv4\t\t\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(2)
        # print(re.search(r'(\s+1\s+\t+\s+ipv4\t\t\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).groups())
        return dns


class STP(SWOCLI):
    def get_stp_summary(self):
        show_ip_interface = ['show spanning-tree summary']
        lines = self.capture(show_ip_interface)
        stp_summary = {}
        instance = ""
        for line in lines.split('\n'):
            if re.search(r'Spanning tree enabled protocol is\s+([a-z]+)', line, re.I):
                stp_summary["protocol"] = re.search(r'Spanning tree enabled protocol is\s+([a-z]+)', line, re.I).group(
                    1)

            if re.search(r'MST\d+', line, re.I):
                instance = re.search(r'MST\d+', line, re.I).group()
                stp_summary[instance] = {}
            if re.search(r'(te|gi)\d\/\d+', line, re.I):
                if instance:
                    interface = re.search(r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(1)
                    stp_summary[instance][interface] = {}
                    stp_summary[instance][interface]["Port-Role"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(3)
                    stp_summary[instance][interface]["Port-State"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(4)
                    stp_summary[instance][interface]["Port-Status"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(5)

                else:
                    interface = re.search(r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(1)
                    stp_summary[interface] = {}
                    stp_summary[interface]["Port-Role"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(3)
                    stp_summary[interface]["Port-State"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(4)
                    stp_summary[interface]["Port-Status"] = re.search(
                        r'((te|gi)\d\/\d+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)', line, re.I).group(5)
        return stp_summary

    def get_stp_status(self):
        cmd = ['show spanning-tree']
        lines = self.capture(cmd)
        stp_summary = {}
        for line in lines.split('\n'):
            if re.search(r'.*Spanning tree Protocol has been disabled.*', line, re.I):
                stp_summary["state"] = False
            else:
                stp_summary["state"] = True

            if re.search(r'.*Bridge is executing the rstp compatible Rapid Spanning Tree Protocol.*', line, re.I):
                stp_summary["protocol"] = "RSTP"
            if re.search(r'.*MST00 is executing the mstp compatible Multiple Spanning Tree Protocol.*', line, re.I):
                stp_summary["protocol"] = "MSTP"
            # else:
            #     stp_summary["protocol"]="Unknown"

        return stp_summary


class Upgrade(SWOCLI):
    def tftp(self):
        show_ip_interface = ['firmware upgrade %s']
        lines = self.capture(show_ip_interface)


class StaticMAcAddress(SWOCLI):
    def get_static_mac_info(self):
        show_static_mac = ['show mac-address-table static unicast']
        lines = self.capture(show_static_mac)
        static_mac = {}
        for line in lines.split('\n'):
            if re.search(r'(\d+)', line, re.I):
                vlan_id = re.search(r'(\d+)', line, re.I).group(1)
                static_mac[vlan_id] = {}
            if re.search(r'(\d+)', line, re.I):
                mac = re.search(r'(\d+)', line, re.I).group(1)
                static_mac[mac] = {}

        return static_mac


class Macaddress(SWOCLI):
    def macAdressStaticUnicastTable(self):
        show_ip_route = ['show mac-address-table static unicast']
        lines = self.capture(show_ip_route)
        mac_Adress_Static_Unicast_Table = {}
        for line in lines.split('\n'):
            if re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I):
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(
                        3)] = {}
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Vlan'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(2)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Mac Address'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                               re.I).group(3)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Type'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(4)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'ConnectionId'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                                re.I).group(5)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Ports'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                         re.I).group(6)
        return mac_Adress_Static_Unicast_Table

    def macAdressDynamicTable(self):
        show_ip_route = ['show mac-address-table']
        lines = self.capture(show_ip_route)
        mac_Adress_Static_Unicast_Table = {}
        for line in lines.split('\n'):
            if re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I):
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(
                        3)] = {}
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Vlan'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(2)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Mac Address'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                               re.I).group(3)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Type'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                        re.I).group(4)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'ConnectionId'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                                re.I).group(5)
                mac_Adress_Static_Unicast_Table[
                    re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line, re.I).group(3)][
                    'Ports'] = re.search(r'((\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+(.*)\s+(\w+/\d+))', line,
                                         re.I).group(6)
        return mac_Adress_Static_Unicast_Table

    def macAgingTime(self):
        show_ip_route = ['show mac-address-table aging-time']
        lines = self.capture(show_ip_route)
        mac_Adress_aging_time = {}
        for line in lines.split('\n'):
            if re.search(r'(Mac Address Aging Time)', line, re.I):
                mac_Adress_aging_time[
                    re.search(r'((Mac Address Aging Time)\s*:\s*(.*))', line, re.I).group(2)] = re.search(
                    r'((Mac Address Aging Time)\s*:\s*(.*))', line, re.I).group(3)
        return mac_Adress_aging_time


class User(SWOCLI):
    def listUsers(self):
        show_ip_route = ['listuser']
        lines = self.capture(show_ip_route)
        users_list = {}
        for line in lines.split('\n'):

            if re.search(r'((\w+)\s+(\d+).*)', line, re.I):
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)] = {}
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)]['user'] = re.search(
                    r'((\w+)\s+(\d+).*)', line, re.I).group(2)
                users_list[re.search(r'((\w+)\s+(\d+).*)', line, re.I).group(2)]['privilege'] = re.search(
                    r'((\w+)\s+(\d+).*)', line, re.I).group(3)
        return users_list


class StaticRoute(SWOCLI):
    def get_staticroute_info_from_sw(self):
        show_ip_route = ['show ip route']
        lines = self.capture(show_ip_route)
        staticroute = {}
        for line in lines.split('\n'):
            if re.search(r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                         re.I):
                staticroute["destination_ip"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(2)
                staticroute["subnet_mask"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(3)
                staticroute["gateway"] = re.search(
                    r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2}).* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line,
                    re.I).group(4)
            if re.search(r'(.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*)', line, re.I):
                print(re.search(r'(.* (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d+).*)', line, re.I).groups())

        return staticroute


class Qos(SWOCLI):
    def get_qos_info_from_sw(self):
        show_qos_info = ["show qos global info"]
        lines = super().capture(show_qos_info)
        qos_global_info = {}
        for line in lines.split('\n'):
            if re.search(r'((System Control|Trustmode)\s*)', line, re.I):
                qos_global_info[re.search(r'((System Control|Trustmode)\s*)', line, re.I).group(2)] = re.search(
                    r'((System Control|Trustmode)\s*:\s*(.*))', line, re.I).group(3)
                # print(re.search(r'((System Control|Trustmode)\s*:\s*(.*))',line,re.I).groups(2))
        return qos_global_info

    def get_qos_schedule_method_from_sw(self):
        show_schedule_method = ["show scheduler"]
        lines = super().capture(show_schedule_method)
        qos_schedule_method_info = {}
        qos_schedule_method_info["queue"] = {}
        for line in lines.split('\n'):
            if re.search(r'((Scheduler Algo)\s*)', line, re.I):
                qos_schedule_method_info[re.search(r'((Scheduler Algo)\s*)', line, re.I).group(2)] = re.search(
                    r'((Scheduler Algo)\s*:\s*(.*))', line, re.I).group(3).strip()
                print(re.search(r'((Scheduler Algo)\s*)', line, re.I).groups())
                print(re.search(r'((Scheduler Algo)\s*:\s*(.*))', line, re.I).group(3).strip())

            if "Scheduler Algo" in qos_schedule_method_info.keys():
                if qos_schedule_method_info["Scheduler Algo"] == "weightedRoundRobin":
                    if re.search(r'(^(\d)\s*)', line, re.I):
                        qos_schedule_method_info["queue"][re.search(r'((\d)\s*)', line, re.I).group(2)] = re.search(
                            r'((\d)(\s*)(\d+)(\s*))', line, re.I).group(4)
                        # print(re.match(r'((^\d\s*)(\d)(\s*))',line,re.I).groups())
        return qos_schedule_method_info

    def get_qos_IPDSCP_from_sw(self):
        show_IPDSCP = ["show priority-map in-priority-type ipDscp"]
        lines = super().capture(show_IPDSCP)
        qos_IPDSCP_info = {}
        qos_IPDSCP_info["queue"] = {}
        for line in lines.split('\n'):
            # if re.search(r'(\s*:\s*(.*))',line,re.I):
            #     print(re.search(r'(\s*:\s*(.*))',line,re.I).group(2))

            if re.search(r'((\d+.*)\s+:\s+(\d))', line, re.I):
                #     print(re.search(r'((\d+.*)\s+:\s+(\d))',line,re.I).group(2).strip())

                qos_IPDSCP_info["queue"][re.search(r'(\s*:\s*(.*))', line, re.I).group(2)] = re.search(
                    r'((\d+.*)\s+:\s+(\d))', line, re.I).group(2).strip().split(",")
        logger.info(qos_IPDSCP_info)
        #         print(re.search(r'((Scheduler Algo)\s*:\s*(.*))',line,re.I).group(3).strip())
        return qos_IPDSCP_info

    def get_qos_CoS_from_sw(self):
        show_CoS = ["show priority-map in-priority-type vlanPri"]
        lines = super().capture(show_CoS)
        qos_CoS_info = []

        for line in lines.split('\n'):
            # print(line)
            if re.search(r'(\d\s*:(.*))', line, re.I):
                print(re.search(r'((\d.*)\s*:(.*))', line, re.I).group(2).strip().split(","))
                qos_CoS_info.append({"cos_id": re.search(r'((\d.*)\s*:(.*))', line, re.I).group(2).strip().split(","),
                                     "queue_id": re.search(r'(\d\s*:(.*))', line, re.I).group(2).strip()})
        logger.info(qos_CoS_info)

        return qos_CoS_info


class RadiusServer(SWOCLI):
    def get_radius_server_info_from_sw(self):
        show_radius_server_info = ["show radius server"]
        lines = super().capture(show_radius_server_info)
        radius_server_global_info = {}
        for line in lines.split('\n'):
            if re.search(
                    r'((Index|Server address|Shared secret|Radius Server Status|Response Time|Maximum Retransmission|Authentication Port|Accounting port)\s*)',
                    line, re.I):
                radius_server_global_info[re.search(
                    r'((Index|Server address|Shared secret|Radius Server Status|Response Time|Maximum Retransmission|Authentication Port|Accounting port)\s*)',
                    line, re.I).group(2)] = re.search(
                    r'((Index|Server address|Shared secret|Radius Server Status|Response Time|Maximum Retransmission|Authentication Port|Accounting port)\s*:\s*(.*))',
                    line, re.I).group(3).strip()
                # print(re.search(r'((System Control|Trustmode)\s*:\s*(.*))',line,re.I).groups(2))
        return radius_server_global_info


class VoiceVlan(SWOCLI):
    def get_voice_vlan_config(self):
        show_ip_route = ["show voice vlan"]
        lines = super().capture(show_ip_route)
        voice_vlan_config = {}
        for line in lines.split('\n'):
            if re.search(
                    r'((Administrate Voice VLAN state|Voice VLAN ID|Voice VLAN VPT|Voice VLAN DSCP|Voice VLAN CoS|Voice VLAN 1p Remark|Voice VLAN Timer|Voice VLAN Aging Time)\s*)',
                    line, re.I):
                voice_vlan_config[re.search(
                    r'((Administrate Voice VLAN state|Voice VLAN ID|Voice VLAN VPT|Voice VLAN DSCP|Voice VLAN CoS|Voice VLAN 1p Remark|Voice VLAN Timer|Voice VLAN Aging Time)\s*)\s*:\s*(.*)',
                    line, re.I).group(2)] = re.search(
                    r'((Administrate Voice VLAN state|Voice VLAN ID|Voice VLAN VPT|Voice VLAN DSCP|Voice VLAN CoS|Voice VLAN 1p Remark|Voice VLAN Timer|Voice VLAN Aging Time)\s*:\s*(.*))',
                    line, re.I).group(3).strip()
                # print(re.search(r'((Administrate Voice VLAN state|Voice VLAN ID|Voice VLAN VPT|Voice VLAN DSCP|Voice VLAN CoS|Voice VLAN 1p Remark|Voice VLAN Timer|Voice VLAN Aging Time)\s*:\s*((.*)\s*))',line, re.I).groups())
        return voice_vlan_config


if __name__ == "__main__":
    a = SWOCLI("10.5.3.58", 2009)
    a.get_dot1x_port_config()
