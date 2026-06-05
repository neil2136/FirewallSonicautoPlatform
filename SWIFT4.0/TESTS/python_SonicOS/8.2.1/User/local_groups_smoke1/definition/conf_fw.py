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

    # def test_register_fw(self):
    #     # license = LicenseCli(fw_cli)
    #     rc = license.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")


