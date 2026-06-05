import sys
import os
import time
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_VLAN')
from runner.unittest.setup import Test
from lib.modules.API import network
from lib.modules.CLI import system
from lib.modules.API import vpn
from utm import Firewall
from testcases.settings import Parameter
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host


ip = Parameter.X0_IP
rem_ip = Parameter.X1_IP
fw = Firewall(ip, user='admin', password='password')
rem_fw = Firewall(rem_ip, user='admin', password='password')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
ao = network.AddressobjectsApi(fw)
rem_interface = network.InterfaceIPv4Api(rem_fw)
rem_interface_v6 = network.InterfaceIPv6Api(rem_fw)
rem_ao = network.AddressobjectsApi(rem_fw)
rem_setting_cli = system.SettingCli(rem_fw)
rem_vpn = vpn.VpnbasesettingApi(rem_fw)


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_IP['ipv4']['X1'],
            'gateway': Parameter.X1_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")    

    def test_00_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_IP['ipv4']['X2'],
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_03_add_ao(self):
        dut_ipv6 = {
            'name' :Parameter.REMOTE_X2_IPv6_Network,
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.REMOTE_X2_IPv6_Network,
            'mask': '/64',
        }
        rc = ao.config_ipv6_addressobject(**dut_ipv6)
        Assertion.assert_equal(rc, True, "ERR: add ao failed")
