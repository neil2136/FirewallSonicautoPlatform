import sys
import os
import re
import copy
import time
import subprocess
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from contextvars import ContextVar


# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli
from lib.modules.API import dpissl
from lib.modules.API import securityservices
from lib.modules.API.log import LogMonitorApi, SyslogSettingsApi, LogSettingsApi
from lib.modules.API.system import SettingApi
from lib.modules.API.policy import AppRulesApi
from lib.modules.API.firewall import MatchobjectApi, AppControlApi


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME']+'/Log/DPI_tag_in_Syslog_Connection_Closed/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path+'testplan/DPI_tag_in_Syslog_Connection_Closed.json'
syslog_conf_path = suite_path + 'definition/file/syslog'
http_path = suite_path + 'definition/file/http_server'
udp_path = suite_path + 'definition/file'
syslog_file = '/var/log/messages'
cert_path = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
tool_path = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/tools'


os_obj = Openstack(Params.testbed)
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
PC3_ETH1_IP = os_obj.get_node_interface_ip('PC3', 'eth1')
PC3_ETH2_IP = os_obj.get_node_interface_ip('PC3', 'eth2')

logger.info(f"""
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
PC3_ETH1_IP is: {PC3_ETH1_IP}
PC3_ETH2_IP is: {PC3_ETH2_IP}
""")

pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH1_IP)
pc3_login = Host(PC3_ETH1_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_NET = '12.12.1.0'
    X2_IP = '13.13.1.168'
    X2_NET = '13.13.1.0'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    httpserver_ip = PC2_ETH2_IP
    dmz_httpserver = PC3_ETH2_IP


# Instantiate objects including API import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)

fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

if_v4_api = network.InterfaceIPv4Api(fw)
license_cli = LicenseCli(fw_cli)
cdpi_api = dpissl.ClientSslApi(fw)
spy_api = securityservices.AntiSpywareApi(fw)
gav_api = securityservices.GAV(fw)
ips_api = securityservices.IPSApi(fw)
log_mon_api = LogMonitorApi(fw)
syslog_api = SyslogSettingsApi(fw)
ao_api = network.AddressobjectsApi(fw)
app_rule_api = AppRulesApi(fw)
match_api = MatchobjectApi(fw)
log_settings_api = LogSettingsApi(fw)
setting_api = SettingApi(fw)
app_control_api = AppControlApi(fw)
content_filter_api = securityservices.ContentFilterApi(fw)
zone_api = network.ZoneObjectsApi(fw)

spy_params_d = {
    'enable': True,
    'high_danger_prevent': False,
    'medium_danger_prevent': False,
    'low_danger_prevent': False,
    'high_danger_detect': True,
    'medium_danger_detect': True,
    'low_danger_detect': True,
    'smtp': False,
}

app_rule_base = {
    "app_rules": {
        "policy": [
            {
                "name": "http",
                "enable": True,
                "type": {
                    "app_control": True
                },
                "source": {
                    "service": {
                        "any": True
                    },
                    "address": {
                        "any": True
                    }
                },
                "destination": {
                    "service": {
                        "any": True
                    },
                    "address": {
                        "any": True
                    }
                },
                "exclusion": {
                    "address": {},
                    "service": {}
                },
                "match_object": {
                    "included": "http",
                    "excluded": ""
                },
                "action_object": "Reset/Drop",
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {}
                },
                "schedule": {
                    "always_on": True
                },
                "flow_reporting": False,
                "logging": True,
                "log": {
                    "individual": False,
                    "redundancy": {
                        "global": True
                    }
                },
                "app_control_message_format": True,
                "zone": {
                    "any": True
                }
            }
        ]
    }
}

match_obj_base = {
    "name": "http",
    "object_type": "application-list",
    "application": [{"category": {"id": 74}, "app": {"id": 1277}}]
    }

syslog_para = {
    'facility': 'local_use_0',
    'format': 'default',
    'id': 'firewall',
    'override_s': 'off',
}

log_dict = {
    "log": {
        "event": [
            {
                "priority_level": "alert",
                "log_monitor": {"redundancy_interval": 0},
                "email_alert": {"redundancy_interval": 0},
                "syslog": {"redundancy_interval": 0},
                # "trap": {"redundancy_interval": 0},
                "ipfix": {},
                "event_profile": {"syslog_server_profile": 0},
                "log_digest": True,
                "color": {"hex": "0x00000000"},
                "alert_email": {}
            }
        ]
    }
}

log_97_upodate = {
    "id": 97,
    "name": "Syslog Website Accessed",
}

log_537_upodate = {
    "id": 537,
    "name": "Connection Closed",
}

log_97_dict = copy.deepcopy(log_dict)
log_97_dict["log"]["event"][0].update(log_97_upodate)

log_537_dict = copy.deepcopy(log_dict)
log_537_dict["log"]["event"][0].update(log_537_upodate)

logsetting_list = [log_537_dict, log_97_dict]

ac_global = {
    "enable": True,
    "log_all": False,
    "log_filename": False,
    'log_redundancy': {'filter': {'value': 1}}
}
