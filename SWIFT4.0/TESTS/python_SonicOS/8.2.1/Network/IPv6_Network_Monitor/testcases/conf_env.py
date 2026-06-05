from settings import *

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
ao = network.AddressobjectsApi(fw)


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'dns1':'1.1.1.1',
            'gateway': Parameter.DUT_X1_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")    

    def test_00_02_add_ao(self):
        ao1 = {
            "object_type":"host",
            "name": 'probe_gw',
            "zone": 'WAN',
            "value":  Parameter.PROBE_GW
        }
        rc = ao.config_addressobject(**ao1)  
        ao2 = {
            "object_type":"host",
            "name": 'probe_remote',
            "zone": 'WAN',
            "value":  Parameter.PROBE_REMOTE
        }
        rc &= ao.config_addressobject(**ao2) 
        ao3 = {
            "object_type":"host",
            "name": 'probe_gw_2',
            "zone": 'WAN',
            "value":  Parameter.PROBE_GW_2
        }
        rc &= ao.config_addressobject(**ao3) 
        Assertion.assert_equal(rc, True, "ERR: Add ao failed.")    

    def test_01_01_assign_X1_IPv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.DUT_X1_IPV6,  
            'prefix_length': 64
        }
        out = interface_v6.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Config X1 IPv6 address failed!")