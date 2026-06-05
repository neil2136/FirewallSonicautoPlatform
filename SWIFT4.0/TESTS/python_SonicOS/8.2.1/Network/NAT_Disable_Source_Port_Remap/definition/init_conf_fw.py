from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_configure_x1_v4(self):
        x1_opt = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': "12.12.1.1"

        }
        res = interfacev4api.config_interface(**x1_opt)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_configure_x0_v6(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(
            res, True, "ERR: Configure X0 IPv6 static failed")

    def test_03_configure_x1_v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfacev6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(
            res, True, "ERR: Configure X1 IPv6 static failed")

    def test_04_register_fw(self):
        for i in range(5):
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
