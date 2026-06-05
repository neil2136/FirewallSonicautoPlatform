from definition.initial_parameter import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
            
        }
        resp = interface.config_interface(**x1_static)
        Assertion.assert_equal(resp, True, 'x1 not configured')

    @repeat_method(5)
    def test_register_fw(self):
        # license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

