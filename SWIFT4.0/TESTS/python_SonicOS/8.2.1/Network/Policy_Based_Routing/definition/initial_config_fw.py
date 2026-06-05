from definition.initial_parameter import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    def test_00_01_Config_X1_IPv4(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 to static failed")

    def test_00_02_Config_X2_IPv4(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'dns1': Parameter.X2_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 to static failed")

    def test_00_02_Config_X3_IPv4(self):
        x3_static = {
            'if': 'X3',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'dns1': Parameter.X3_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 to static failed")