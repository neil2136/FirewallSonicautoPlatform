import os
import sys
import copy
import re
import time
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Email_Audit_Records_Automation')
from multiprocessing import Process
import multiprocessing
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,system,log
from utm import Firewall
import unittest
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.log import LogAutomationCli

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
PC2 = Host(Params.testbed + '-PC2')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Log/Email_Audit_Records_Automation/testplan/Email_Audit_Records_Automation.json'
DUT_X0_IPV4 = '192.168.168.168'
DUT_X1_IPV4 = '13.0.0.10'
PC2_ETH0_IPV4 = '13.0.0.5'
PC1_ETH0_IPV4 = '192.168.168.200'

fw_api = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto',ssh_version=2, supported_config_mode='cli-ssh')

interfacev4api = network.InterfaceIPv4Api(fw_api)
license_obj = LicenseCli(fw_cli)
Lsetting = system.SettingApi(fw_api)
log_automation = log.LogAutomationApi(fw_api)
logAuto_cli = LogAutomationCli(fw_cli)


ftp_path = os.environ['PYTHON_SONICOS_HOME'] + '/Log/Email_Audit_Records_Automation/definition'
ftp_commands=[f'cp -r {ftp_path}/ftpusers /etc/vsftpd/',f'cp -r {ftp_path}/vsftpd.conf /etc/vsftpd/',
              f'cat /etc/vsftpd/ftpusers',
              f'cat /etc/vsftpd/vsftpd.conf']
active_ftp=['systemctl restart vsftpd','systemctl status  vsftpd']
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X1_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }

