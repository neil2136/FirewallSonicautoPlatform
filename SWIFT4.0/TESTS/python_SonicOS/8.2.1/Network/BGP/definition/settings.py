__author__ = 'CHU'
import os
import sys
import re
import time
import copy
import paramunittest
import unittest

from runner.settings import logger, Params
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/BGP')

from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.ui.fw_page import FWPage
from lib.modules.API import network
from lib.modules.CLI.system import LicenseCli

G_DNS1 = Params.G_DNS1
G_DNS2 = Params.G_DNS2

os_obj = Openstack(Params.testbed)
LC_X3_VLAN_ID = os_obj.get_node_interface_vlan_id('UTM', 'X3:1')
RT_X3_VLAN_ID = os_obj.get_node_interface_vlan_id('RemoteGEN5', 'X3:1')


class Parameter():
    FIREWALL 		= '192.168.168.168'
    # Local DUT
    VLAN_ID = LC_X3_VLAN_ID

    DUT_IP ={
        'X0'      : '192.168.168.168',
        'X1'      : "12.12.1.200",
        'X3_SUB'  : "12.12.2.200",

    }

    RT_IP = {
        'X0'        : "172.16.1.101",
        'X1'        : "12.12.1.201",
        'X2'        : "172.16.2.101",
        'X3_SUB'    : "12.12.2.201",
    }

    dut_x0 = {
        'if'    : 'X0',
        'zone'  : 'LAN',
        'mode'  : 'static',
        'ip'    : DUT_IP['X0'],
        'mask'  : '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh'  : True,
        'mgmt_ping' : True,
    }

    dut_x1 = {
        'if'    : 'X1',
        'zone'  : 'WAN',
        'mode'  : 'static',
        'ip'    : DUT_IP['X1'],
        'mask'  : '255.255.255.0',
        'gateway':'12.12.1.1',
        'mgmt_https': True,
        'mgmt_ssh'  : True,
        'mgmt_ping' : True,
        'dns1':G_DNS1
    }

    dut_x3_sub = {
        'zone'           : 'WAN',
        'type'           : 'vlan',
        'vlan_tag'       : VLAN_ID,
        'if'             : 'X3',
        'mode'           : 'static',
        'ip'             : DUT_IP["X3_SUB"],
        'dns1'           : '0.0.0.0',
        'dns2'           : '0.0.0.0',
        'dns3'           : '0.0.0.0',
    }

    rmt_x2 = {
        'if'        : 'x2',
        'zone'      : 'wan',
        'mode'      : 'static',
        'ip'        : RT_IP["X2"],
        'mask'      : '255.255.255.0',
        'dns1'      : G_DNS1,
        'dns2'      : G_DNS2,

    }

    lb_opt_en = {
            'enable'    : True,
            'probes'    : True,
    }

    probe_cfg = {
        'name'          : '+Default+LB+Group',
        'interface'     : 'X1',
        'probe_type'    : 'logical',
        'probe_option'  : 'both',
        'main_protocol' : 'tcp',
        'main_value'    : 50000,
        'alter_protocol': 'tcp',
        'alter_value'   : 50000,
        'rank':1,
   }

    bin_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/BGP/bin'
    cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
    plan_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/BGP/testplan/'
    TESTPLAN = plan_path + 'BGP.json'

lip = Parameter.FIREWALL
rip = Parameter.RT_IP['X1']
fw = Firewall(lip, user='admin', password='password', supported_config_mode='api')
rt = Firewall(rip, user='admin', password='password', supported_config_mode='api')
cl1 = Firewall(lip, user='admin', password='password', supported_config_mode='cli-ssh')
cl2 = Firewall(rip, user='admin', password='password', supported_config_mode='cli-ssh')


from definition.Func import Function
clear = Function()
lc_ip = Parameter.DUT_IP['X1']
rt_ip = Parameter.RT_IP['X1']
lc_sub = Parameter.DUT_IP['X3_SUB']
rt_sub = Parameter.RT_IP['X3_SUB']
interface =  network.InterfaceIPv4Api(fw)
failover = network.FailoverLbApi(fw)
dyn_route = network.DynamicRoutingApi(fw)
license_obj = LicenseCli(cl1)

ui_obj = FWPage()
stime = 10



