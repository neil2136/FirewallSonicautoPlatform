from http import server
import os
import sys
import re
import copy
import time

from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from nose_parameterized import parameterized
import paramunittest

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.policy import NatPolicyApi
from lib.modules.API.network import InterfaceIPv4Api, DnsSettingsApi, AddressobjectsApi, ArpApi, AddressgroupsApi, DnsProxyApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.log import LogMonitorApi, LogCategoryApi, LogSettingsApi
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.API.firewall import AccessRuleApi
from lib.modules.API.system import PacketmonitorApi, DiagnosticApi, SettingApi, TimeApi
from lib.modules.CLI.system import LicenseCli


# import form test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Dynamic_Address_Object_Full/'
sys.path.append(suite_path)
defi_path = suite_path + 'definition/'
confs_path = defi_path + '/conf_files/'
TESTPLAN = suite_path + 'testplan/Dynamic_Address_Object.json'

# Instantiate objects including common_lib import
os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC1_ETH3_IP = os_obj.get_node_interface_ip('PC1', 'eth3')
PC1_ETH4_IP = os_obj.get_node_interface_ip('PC1', 'eth4')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC1_ETH2_IP: {PC1_ETH2_IP}'
            f'\n PC1_ETH3_IP: {PC1_ETH3_IP}'
            f'\n PC1_ETH4_IP: {PC1_ETH4_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC2_ETH1_IP}')
PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH1_IP)


# parameters on the fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X2_IP = '14.1.1.168'
    MASK = '255.255.255.0'
    X1_IP = '13.0.0.168'
    X1_GW = '13.0.0.10'
    X1_DNS1 = '13.0.0.10'
    X1_DNS2 = '10.190.202.200'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    VALID_DNS = X1_DNS1
    FAKE_DNS1 = '2.2.2.2'
    FAKE_DNS2 = '3.3.3.3'
    FAKE_DNS3 = '5.5.5.5'
    PC1_ETH0_MAC = ''
    PC1_ETH0_MAC_org = ''
    PC1_ETH0_LINKLOCAL = ''
    PC1_ETH2_MAC = ''
    PC1_ETH2_MAC_org = ''
    PC1_ETH2_LINKLOCAL = ''
    DAO_host_ip = '13.0.0.12'


# Instantiate objects including API,CLI import
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
aoapi = AddressobjectsApi(fw)
interfaceapi = InterfaceIPv4Api(fw)
accessruleapi = AccessRuleIPv4Api(fw)
natrulesapi = NatPolicyApi(fw)
logmonitorapi = LogMonitorApi(fw)
diagnosticapi = DiagnosticApi(fw)
logcategoryapi = LogCategoryApi(fw)
logsettingsapi = LogSettingsApi(fw)
arpapi = ArpApi(fw)
dnsapi = DnsSettingsApi(fw)
pkgapi = PacketmonitorApi(fw)
aocli = AddressObjectCli(fw_cli)
aograpi = AddressgroupsApi(fw)
aclapi = AccessRuleApi(fw)
settingapi = SettingApi(fw)
timeapi = TimeApi(fw)
licensecli = LicenseCli(fw_cli)
dnsproxyapi = DnsProxyApi(fw)


# parameters on the test cases
class CaseParams:
    fw_time_tc01 = {}
    fw_time_tc09 = {}
    fw_time_tc22 = {}
    fw_time_tc03 = {}
    fw_time_tc24 = {}
    fw_time_tc30 = {}
    tc12aonewip = "14.1.1.200"
    invalidmac = "11:22:33:33:44:55"
    invalidfqdn = 'jewfiojaojfoi.cjofiwjaoi.orfg'
    maxfqdnaonum = 0
    maxmacaonum = 0
    # maxmacaonum = 2630


fqdn_ao_dict = {
    "object_type": "fqdn",
    "name": "fqdntest",
    "zone": "WAN",
    "value": "www12.limitFQDN.com",
    "dns_ttl": 0,
}

mac_ao_dict = {
    "object_type": "mac",
    "name": "mactest",
    "zone": "LAN",
    "value": "",
    "multi_homed": False,
}

static_arp_dict = {
    'ip': PC1_ETH2_IP,
    'mac': '',
    'interface': 'X2',
    'publish': False,
    'bind_mac': False,
}

acl_dict = {
    'name': 'deny_lan_to_wan',
    'from': 'LAN',
    'to': 'WAN',
    'source_addr': {"name": ''},
    'dst_addr': {"name": ''},
    'service': {"name": "HTTP"},
    'action': 'deny',
    "comment": '',
}

dns_dict = {
    "dns": {
        "server": {
            "inherit": False,
            "static": {
                "primary": Parameter.VALID_DNS,
                "secondary": '0.0.0.0',
                "tertiary": '0.0.0.0',
            }
        }
    }
}

dns_24_update = {
    "primary": Parameter.FAKE_DNS1
}

dns_25_update = {
    "primary": Parameter.FAKE_DNS1,
    "secondary": Parameter.FAKE_DNS2,
    "tertiary": Parameter.VALID_DNS,
}

dns_26_update = {
    "tertiary": Parameter.FAKE_DNS3
}

dns_36_update = {
    "fqdn_over_tcp_dns": True,
}

dns_24 = copy.deepcopy(dns_dict)
dns_24["dns"]["server"]["static"].update(dns_24_update)

dns_25 = copy.deepcopy(dns_dict)
dns_25["dns"]["server"]["static"].update(dns_25_update)

dns_26 = copy.deepcopy(dns_25)
dns_26["dns"]["server"]["static"].update(dns_26_update)

dns_36 = copy.deepcopy(dns_dict)
dns_36["dns"].update(dns_36_update)

logger.info(f'\n dns_dict: {dns_dict}'
            f'\n dns_24: {dns_24}'
            f'\n dns_25: {dns_25}'
            f'\n dns_26: {dns_26}'
            f'\n dns_36: {dns_36}'
            )

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

log_524_upodate = {
    "id": 524,
    "name": "Web Request Drop",
}
log_880_upodate = {
    "id": 880,
    "name": "Failed to Resolve Dynamic Address Object",
}
log_911_upodate = {
    "id": 911,
    "name": "Added Host Entry",
}
log_912_upodate = {
    "id": 912,
    "name": "Removed Host Entry",
}

log_524_dict = copy.deepcopy(log_dict)
log_524_dict["log"]["event"][0].update(log_524_upodate)

log_880_dict = copy.deepcopy(log_dict)
log_880_dict["log"]["event"][0].update(log_880_upodate)

log_911_dict = copy.deepcopy(log_dict)
log_911_dict["log"]["event"][0].update(log_911_upodate)

log_912_dict = copy.deepcopy(log_dict)
log_912_dict["log"]["event"][0].update(log_912_upodate)

logger.info(f'\n log_settings_dict: {log_dict}'
            f'\n log_524_dict: {log_524_dict}'
            f'\n log_880_dict: {log_880_dict}'
            f'\n log_911_dict: {log_911_dict}'
            f'\n log_912_dict: {log_912_dict}')

logsetting_list = [log_524_dict, log_880_dict, log_911_dict, log_912_dict]
