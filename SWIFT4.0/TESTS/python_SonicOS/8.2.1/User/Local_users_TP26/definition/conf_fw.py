from definition.initial_parameter import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_config_x1_interface(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.0.0.100',
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'mgmt_https': True,
            'user_https': True,
        }
        resp = interface.config_interface(**x1_static)
        Assertion.assert_equal(resp, True, 'x1 not configured')

    def test_02_enable_api(self):
        api_dict = {
            'sonicos-api': True,
            'basic': True,
        }
        result = admin.sonicos_api(**api_dict)
        Assertion.assert_equal(result, True, "ERR: Enable api failed.")


