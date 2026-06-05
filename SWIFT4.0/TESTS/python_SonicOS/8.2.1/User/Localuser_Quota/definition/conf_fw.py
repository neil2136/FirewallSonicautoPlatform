from definition.initial_parameter import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_config_x1_interface(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'user_https': True,
        }
        resp = interface.config_interface(**x1_static)
        Assertion.assert_equal(resp, True, 'x1 not configured')

