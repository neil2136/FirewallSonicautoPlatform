from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1_IPv4(self):
        x1_static_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ping': True,

        }
        res = interfacev4api.config_interface(**x1_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 IPv4 to static failed")

    def test_00_02_Config_X2_IPv4(self):
        x2_static_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        res = interfacev4api.config_interface(**x2_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 IPv4 to static failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


