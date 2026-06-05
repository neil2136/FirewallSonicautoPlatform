import os
import sys
import re
import time
import copy
import requests
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + 'CLI/CLI3_Access_Rules/testcases')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + 'CLI/CLI3_Access_Rules')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
           '/CLI/CLI3_Access_Rules/testplan/access_rules.json'


from utm import Firewall
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.firewall import AccessRuleCli
from lib.modules.CLI.network import RouteCli
from lib.modules.API.network import AddressobjectsApi, InterfaceIPv4Api
from lib.modules.CLI.system import LicenseCli


# parameters on the openstack
class Parameter:
    FIREWALL = '10.8.105.173'
    X1_IP = '10.8.105.173'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# configure fw
source_ao_dict = {
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
dest_ao_dict = {
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


# class Test_ACLUUIDTests and Test_ACLNonUUIDTests
check_uuid_cfg_dict = {
    'from': False,
    'to': False,
    'source': False,
    'destination': False,
    'service': False,
    'action': False,
    'comment': False
}
check_nonuuid_cfg_dict = {
    'enable': False,
    'action': False,
    'flowreport': False,
    'packetmonitor': False,
    'botnetfilter': False,
    'priority': False,
    'restore': False
}


# paramenters on the test case
access_rule_dict = {
    'version': 'ipv4',
    'from': 'LAN',
    'to': 'WAN',
    'action': 'deny',
    'src_name': source_ao_dict['host']['name'],
    'dst_name': dest_ao_dict['host']['name'],
    'service_name': 'HTTPS',
    'comment': 'AutoACLCLITest',
    'extracmds': None
}
access_rule_uuid_dict = {
    'version': access_rule_dict['version'],
    'uuid': ''
}
edit_access_rule_dict = {
    'version': access_rule_dict['version'],
    'from': access_rule_dict['from'],
    'to': access_rule_dict['to'],
    'action': access_rule_dict['action'],
    'src_name': access_rule_dict['src_name'],
    'dst_name': access_rule_dict['dst_name'],
    'service_name': access_rule_dict['service_name']
}
show_access_rule_dict = {
    'version': access_rule_dict['version'],
    'from': access_rule_dict['from'],
    'to': access_rule_dict['to'],
    'type': 'custom'
}
show_access_rule_uuid_dict = {
    'version': access_rule_dict['version'],
    'type': 'uuid'
}


# Instantiate objects including API,CLI
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
lc = LicenseCli(fw_cli)
accessrulecli = AccessRuleCli(fw_cli)
localao = AddressobjectsApi(fw)
interfacecfg = InterfaceIPv4Api(fw)
