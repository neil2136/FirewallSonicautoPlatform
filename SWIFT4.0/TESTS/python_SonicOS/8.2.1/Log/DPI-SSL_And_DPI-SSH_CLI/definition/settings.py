import os
import sys
import re
import time
import copy
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test,repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

from lib.modules.API import network, system, log
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.policy import Settings
from lib.modules.API.system import CertificateApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/DPI-SSL_And_DPI-SSH_CLI')

OpenS = Openstack(Params.testbed)
MASK = '255.255.255.0'
DUT_X0 = '192.168.168.168'
DUT_X1 = '13.0.0.10'
DUT_X1_GW = '13.0.0.1'
pc1_ip = OpenS.get_node_interface_ip('PC1','eth0')
pc2_ip = "13.0.0.5"
PC2 = Host('15.0.0.4', user='root', password='password')
PC1 = Host(pc1_ip, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/DPI-SSL_And_DPI-SSH_CLI/testplan/testplan_DPI-SSL_And_DPI-SSH.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/DPI-SSL_And_DPI-SSH_CLI/confs/'
dpissl_server_cert = CONFS_PATH + 'cert_local.pfx'

fw_api = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

Linterface = network.InterfaceIPv4Api(fw_api)
LAddrOBJ = network.AddressobjectsApi(fw_api)
dpissl_cli = Settings(fw_cli)

snmp_obj = system.SNMPApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw_api)
audit_logobj = log.AuditlogMonitorApi(fw_api)
logsetting_obj = log.LogSettingsApi(fw_api)
certobj = CertificateApi(fw_api)

syslog_param = {
    "name":pc1_ip,
}

local_obj = {
    "object_type": "host",
    "name": pc1_ip,
    "zone": "LAN",
    "value": pc1_ip,
}

syslog_obj = {
    "object_type": "host",
    "name": 'test_syslog',
    "zone": "LAN",
    "value": '192.168.168.100',
}

snmp_json = {
    "snmp": {
        "enable": True,
        "system_name": "sonicwall",
        "get_community_name": "public",
        "trap_community_name": "public",
        "host_1": pc2_ip,
        "host_2": "",
        "host_3": "",
        "host_4": ""
    }
}

Lx1 = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': DUT_X1,
    'netmask': MASK,
    'gateway': DUT_X1_GW,
    'dns1': Params.G_DNS1,
    'dns2': Params.G_DNS2,
    'dns3': Params.G_DNS3,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True
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
                    "alert_email": {}
                }]
            }
}
