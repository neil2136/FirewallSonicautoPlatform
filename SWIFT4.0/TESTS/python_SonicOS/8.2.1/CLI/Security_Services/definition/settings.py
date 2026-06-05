import os
import sys
import re
import time
import copy
import requests
import asyncio
import unittest
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from util.enhancedinfo import show_testcase_info
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from nose_parameterized import parameterized

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/CLI')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/CLI/Security_Services')


from lib.modules.API import network
from lib.modules.CLI.network import RouteCli
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import log
from lib.modules.CLI import sdwan
from util.dpissl.lib.mail_server import StartMailServer
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.API.system import DiagnosticApi

# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X1_IP = '12.12.1.168'
    X1_SUBNET = '12.12.1.0'
    X1_GW = '12.12.1.1'
    X1_NAT = '12.12.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    MASK = '255.255.255.0'
    PC1_IP = '192.168.168.110'
    PC2_IP = '192.168.168.120'
    PC3_IP = '12.12.1.130'
    CONF_PATH =os.environ["PYTHON_SONICOS_HOME"] + '/CLI/Security_Services/definition/config'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/Security_Services/testplan/testplan.json'
    postfix_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/postfix_1k/'
    dovecot_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/dovecot_1k/'
    mail_server_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/cert/'


fw_api = Firewall( Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall( Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
  
pc1 = Host('localhost')
static_pc = Params.testbed + '-PC2'
pc2 = Host(static_pc)
start_mail_server = StartMailServer(pc1,Parameter.postfix_1k_path,Parameter.dovecot_1k_path,Parameter.mail_server_path+'vsftpd_1k.key',Parameter.mail_server_path+'vsftpd_1k.crt')

interfaceapi = network.InterfaceIPv4Api(fw_api)
licensecli = LicenseCli(fw_cli)
LAddrOBJ = network.AddressobjectsApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
logsetting_obj = log.LogSettingsApi(fw_api)
snmp_obj = system.SNMPApi(fw_api)
sdwancligrp = sdwan.SdwanGroupCli(fw_cli)
sdwancliprobe = sdwan.SdwanPerformanceProbeCli(fw_cli)
sdwan_psp = sdwan.PathSelectionProfileCli(fw_cli)
sdwancliobject = sdwan.SdwanPerformanceClassObjectsCli(fw_cli)
configroutepolicy = RouteCli(fw_cli)
accessrulecli = AccessRuleCli(fw_cli)
audit_logobj = log.AuditlogMonitorApi(fw_api)
log_obj = log.LogMonitorApi(fw_api)
log_automation = log.LogAutomationApi(fw_api)
log_category = log.LogCategoryApi(fw_api)
diag_api = DiagnosticApi(fw_api)
zone_obj = network.ZoneObjectsApi(fw_api)

x1_wan_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': False,
    'mgmt_ping': True,
    'user_https': False,
    'mgmt-snmp': False,
}
syslog_obj = {
    "object_type": "host",
    "name": 'test_syslog',
    "zone": "LAN",
    "value": Parameter.PC1_IP,
}
syslog_param = {
    "name":'test_syslog',
}
log_level_settings = {
            "log": {
                "event": [{
                    "id": 1382,
                    "name": "",
                    "category": "Log",
                    "group": "",
                    "priority_level": "alert",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 600
                    },
                    "syslog": {
                        "redundancy_interval": 0
                    },
                    "event_profile": {
                        "syslog_server_profile": 0
                    },
                    "trap":{
                        "redundancy_interval":0
                    },
                    "ipfix": {
                        "redundancy_interval": 60
                    },
                    "log_digest": True ,
                    "color": {
                        "hex": "0x00FF0000"
                    },
                    "alert_email":{
                        "address":"test@sonicauto.com"
                    }
                }]
            }
}
log_sdwan_category = {
    "log":{
        "category":
        [
            {
                "id":17,
                "name":"SD-WAN",
                "priority_level":"alert",
                "log_email":"test@sonicauto.com",
                "log_monitor":{"type":"mixed"},
                "email_alert":{"type":"enabled", "redundancy_interval":{}},
                "syslog":{"type":"mixed"},
                "trap":{"type":"mixed"},
                "ipfix":{"type":"mixed"},
                "event_profile":{"syslog_server_profile":0},
                "log_digest":{"mixed":True},
                "color":{"leave_unchanged":True},
                "alert_email":{}
            }
        ]
    }
}
snmp_json = {"snmp":
            {
                "enable": True,
                "system_name": "sonicwall",
                "get_community_name": "public",
                "trap_community_name": "public",
                "host_1": Parameter.PC2_IP,
                "host_2": "",
                "host_3": "",
                "host_4": ""
            }
}
