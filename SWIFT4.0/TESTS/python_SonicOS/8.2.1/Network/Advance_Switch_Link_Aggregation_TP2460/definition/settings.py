import os
import sys
import re
import time

import unittest
import paramunittest
from nose_parameterized import parameterized

from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.switching import LinkAggregationApi,VlanTrunkApi
from lib.modules.CLI.system import StatusCli
from lib.modules.API.system import SettingApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Advance_Switch_Link_Aggregation_TP2460')

FIREWALL = '192.168.168.168'
X0_NET = '192.168.168.0'
X0_PC = '192.168.168.169'

X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'

X1_PC = '172.17.1.169'
X1_ZONE = 'WAN'

X3_IP = '12.12.3.101'
X3_NET = '12.12.3.1'
X3_ZONE = 'LAN'
MASK = '255.255.255.0'

trunk_X5 = 'X5'
trunk_X6 = 'X6'
trunk_X7 = 'X7'

DNS1 = Params.G_DNS1
DNS2 = Params.G_DNS2
LAG_Port_256 = 256
LAG_Port_20 = 20
LAG_Port_200 = 200
LAG_Port_100 = 100
os_obj = Openstack(Params.testbed)
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + \
'/Network/Advance_Switch_Link_Aggregation_TP2460/testplan/Advance_Switch_Link_Aggregation_TP2460.json'
TESTPATH = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Advance_Switch_Link_Aggregation_TP2460'

os_stack = Openstack(Params.testbed)

vlan_id_X3 = os_stack.get_node_interface_vlan_id('UTM','X3:1')
vlan_id_X4 = os_stack.get_node_interface_vlan_id('UTM','X4:1')

fw_api = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')

interface_api = InterfaceIPv4Api(fw_api)
system_cli = StatusCli(fw_cli)
LAG_config = LinkAggregationApi(fw_api)
VlanPort = VlanTrunkApi(fw_api)
setting_obj = SettingApi(fw_api)

trunkport_X5 = {
	"port": trunk_X5,
}
trunkport_X6 = {
	"port": trunk_X6,
}
trunkport_X7 = {
	"port": trunk_X7,
}

x1_static = {
    'if': 'X1',
    'zone': X1_ZONE,
    'mode': 'static',
    'ip': X1_IP,
    'netmask': MASK,
    'gateway': X1_GW,
    'dns1': DNS1,
    'dns2': DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
    'multicast': True
}
add_LAG_ports_X5 = {
	"switch": {
		"link_aggregation": [{
			"port": "X5",
			"key": {
				"id": 100
			},
			"member": [],
			"lacp": False,
			"load_balance_type": {
				"source": "mac"
			}
		}]
	}
}
add_LAG_ports_X6 = {
	"switch": {
		"link_aggregation": [{
			"port": "X6",
			"key": {
				"id": 100
			},
			"member": [],
			"lacp": False,
			"load_balance_type": {
				"source": "mac"
			}
		}]
	}
}
add_LAG_ports_X7 = {
	"switch": {
		"link_aggregation": [{
			"port": "X7",
			"key": {
				"id": 200
			},
			"member": [],
			"lacp": False,
			"load_balance_type": {
				"source": "mac"
			}
		}]
	}
}

