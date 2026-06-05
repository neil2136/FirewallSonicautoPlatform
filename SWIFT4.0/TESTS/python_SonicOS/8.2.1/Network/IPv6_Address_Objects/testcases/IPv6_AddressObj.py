import os
import sys
import unittest
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Address_Objects')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Address_Objects/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test
from runner.settings import logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from lib.setting import Parameter
from lib.modules.API.network import InterfaceIPv6Api,AddressobjectsApi,AddressgroupsApi

fw = Firewall(Parameter.FIREWALL, user= 'admin', password= 'password', supported_config_mode='api')
interface = InterfaceIPv6Api(fw)
addressobj = AddressobjectsApi(fw)
addressgroup = AddressgroupsApi(fw)

class Test_IPv6_AddrObj_01(Test):
    uuid = "SOSAIOT-TC-56398"
    description = show_testcase_info(Parameter.TESTPLAN, "2", description=True)['title']

    def test_01_00_add_IPv6AddrObj_range(self):
        addressobj_opt = {
            'name': 'range test LAN',
            'zone': 'LAN',
            'object_type': 'range',
            'begin':'2001::2',
            'end': '2001::5'
        }
        rc = addressobj.config_ipv6_addressobject(**addressobj_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_01_01_delete_IPv6AddrObj(self):
        addressobj_del = {
            'ip_type': 'ipv6',
            'name': 'range test LAN',
        }
        rc = addressobj.del_addressobject(**addressobj_del)
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")

class Test_IPv6_AddrObj_02(Test):
    uuid = "SOSAIOT-TC-56404"
    description = show_testcase_info(Parameter.TESTPLAN, "4", description=True)['title']

    def test_02_00_add_IPv6AddrObj_host(self):
        addressobj_opt = {
            'name': 'host test WAN',
            'zone': 'WAN',
            'object_type': 'host',
            'ip': '2002::2'
        }
        rc = addressobj.config_ipv6_addressobject(**addressobj_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_01_delete_IPv6AddrObj(self):
        addressobj_del = {
            'ip_type': 'ipv6',
            'name': 'host test WAN',
        }
        rc = addressobj.del_addressobject(**addressobj_del)
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")

class Test_IPv6_AddrObj_03(Test):
    uuid = "SOSAIOT-TC-56400"
    description = show_testcase_info(Parameter.TESTPLAN, "24", description=True)['title']

    def test_03_00_add_IPv6AddrObj_network(self):
        addressobj_opt = {
            'name': 'network test SSLVPN',
            'zone': 'SSLVPN',
            'object_type': 'network',
            'subnet': '2007::11',
            'mask':'/64'
        }
        rc = addressobj.config_ipv6_addressobject(**addressobj_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_01_delete_IPv6AddrObj(self):
        addressobj_del = {
            'ip_type': 'ipv6',
            'name': 'network test SSLVPN',
        }
        rc = addressobj.del_addressobject(**addressobj_del)
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")

class Test_IPv6_AddrObj_04(Test):
    uuid = "SOSAIOT-TC-56402"
    description = show_testcase_info(Parameter.TESTPLAN, "29", description=True)['title']

    def test_04_00_add_IPv4AddrObj(self):
        addressobj_opt = {
            'name': 'test1',
            'zone': 'LAN',
            'object_type': 'host',
            'value': '172.168.1.100',
        }
        rc = addressobj.config_addressobject(**addressobj_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv4 Address Obj Failed!")

    def test_04_01_add_IPv6AddrObj(self):
        addressobj_opt = {
            'name': 'test2',
            'zone': 'LAN',
            'object_type': 'range',
            'begin': '2000::2',
            'end': '2000::5',
        }
        rc = addressobj.config_ipv6_addressobject(**addressobj_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_04_02_add_AddrGroup(self):
        addressgroup_opt = {
            'name': 'test',
            'group_type': 'ipv6',
            'addr_obj': {
                'ipv4': 'test1',
                'ipv6': 'test2'
            }
        }
        rc = addressgroup.config_ipv4to6_addressgroup(**addressgroup_opt)
        Assertion.assert_equal(rc, True, "ERR: Add IPv6 Address group Failed!")


class Test_IPv6_AddrObj_05(Test):
    uuid = "SOSAIOT-TC-56403"
    description = show_testcase_info(Parameter.TESTPLAN, "38", description=True)['title']

    def test_05_00_delete_IPv6AddrGroup(self):
        rc = addressgroup.delete_addressgroup(group_type='ipv6', group_path='name', group_name_uuid='test')
        Assertion.assert_equal(rc, True, " ERR: Delete IPv6 Address Group Failed! ")

    def test_05_01_delete_IPv6AddrObj(self):
        addressobj_del = {
            'ip_type': 'ipv6',
            'name': 'test2',
        }
        rc = addressobj.del_addressobject(**addressobj_del)
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")

    def test_05_02_delete_IPv4AddrObj(self):
        addressobj_del = {
            'ip_type': 'ipv4',
            'name': 'test1',
        }
        rc = addressobj.del_addressobject(**addressobj_del)
        Assertion.assert_equal(rc, True, "ERR: Delete IPv4 Address Object Failed!")


