from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.0.0.100',
            'netmask': '255.255.255.0',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'gateway': '13.0.0.1',
            'mgmt_https': True,
            'user_https': True
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '23.0.0.100',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'user_https': True
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(5)
    def test_register_fw(self):
        # license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")