import os
import sys
import re
import time
import copy
import requests
import json


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'CLI/CLI3_Enhancement/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                'CLI/CLI3_Enhancement')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
    '/CLI/CLI3_Enhancement/testplan/enhancement.json'


import unittest
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.network import ServiceCli, NatpolicyCli
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.CLI.system import LicenseCli


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# configure fw
x1_static = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}
source_AO_dict = {
    'host': {
        "object_type": "host",
        "name": "192.168.168.10",
        "zone": "LAN",
        "value": '192.168.168.10'
    },
    'range': {
        "object_type": "range",
        "name": "192.168.168.11-13",
        "zone": "LAN",
        "value": '192.168.168.11,192.168.168.13'
    },
    'network': {
        "object_type": "network",
        "name": "192.168.168.0",
        "zone": "LAN",
        "value": '192.168.168.0,255.255.255.0'
    }
}
dest_AO_dict = {
    'host': {
        "object_type": "host",
        "name": "10.10.10.10",
        "zone": "LAN",
        "value": '10.10.10.10'
    },
    'range': {
        "object_type": "range",
        "name": "10.10.10.11-13",
        "zone": "LAN",
        "value": '10.10.10.11,10.10.10.13'
    },
    'network': {
        "object_type": "network",
        "name": "10.10.10.0",
        "zone": "LAN",
        "value": '10.10.10.0,255.255.255.0'
    }
}


# class Test_ACLUUIDTests
g_acl_check_dict = {
    'from': False,
    'to': False,
    'source': False,
    'destination': False,
    'service': False,
    'action': False,
}
# class Test_NATPolicyTests
g_nat_check_dict = {
    'inbound': False,
    'outbound': False,
    'trans_source': False
}


# paramenters on the test case
# case 01-03,17,18
service_object_dict = {
    'name': 'AutoAddSrvO',
    'protocol': 'udp',
    'sub-type': '',
    'port': '1 80'
}
edit_service_object_dict = {
    'name': service_object_dict['name'],
    'protocol': 'ah'
}
# case 04-06, 19-20
service_group_dict = {
    'name': 'AutoAddSrvG',
    'add-group': ['Ping'],
    'add-object': ['HTTPS']
}
edit_service_group_dict = {
    'name': service_group_dict['name'],
    'name-new': 'AutoAddSrvG_new',
    'add-group': ['Ping6'],
    'del-group': ['Ping'],
    'add-object': ['FTP'],
    'del-object': ['HTTPS']
}
# case 11-16
access_rule_dict = {
    'version': 'ipv4',
    'from': 'LAN',
    'to': 'WAN',
    'action': 'deny',
    'src_name': source_AO_dict['host']['name'],
    'dst_name': dest_AO_dict['host']['name'],
    'service_name': 'HTTPS',
    'comment': 'AutoAddedACL',
    'extracmds': None
}
access_rule_uuid_dict = {
    'version': access_rule_dict['version'],
    'uuid': ''
}
show_access_rule_uuid_dict = {
    'version': access_rule_dict['version'],
    'type': 'uuid'
}
show_access_rule_dict = {
    'version': access_rule_dict['version'],
    'from': access_rule_dict['from'],
    'to': access_rule_dict['to'],
    'type': 'custom'
}
# case 07-10
nat_policy_dict = {
    'version': 'ipv4',
    'inbound': 'X0',
    'outbound': 'X1',
    'orig_source_type': 'group',
    'orig_source': 'LAN Subnets',
    'trans_source_type': 'original',
    'trans_source': '',
    'orig_dest_type': 'any',
    'trans_dest_type': 'original',
    'orig_service_type': 'protocol',
    'orig_service': 'TCP 20 20',
    'trans_service_type': 'name',
    'trans_service': 'BGP',
    'name': 'add_nat',
    'comment': 'AutoAddedNAT'
}
nat_policy_uuid_dict = {
    'version': nat_policy_dict['version'],
    'uuid': ''
}
show_nat_policy_dict = {
    'version': nat_policy_dict['version'],
    'entries': 'all',
    'type': 'custom',
    'inbound': nat_policy_dict['inbound'],
    'outbound': nat_policy_dict['outbound']
}


fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')
lccli = LicenseCli(fw_cli)
accessrulecli = AccessRuleCli(fw_cli)
localaoapi = AddressobjectsApi(fw)
interfacecfgapi = InterfaceIPv4Api(fw)
servicecli = ServiceCli(fw_cli)
natpolicycli = NatpolicyCli(fw_cli)
