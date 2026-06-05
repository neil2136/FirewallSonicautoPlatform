from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_v4(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 ipv4 address failed")

    def test_03_config_x2(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_v4_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 ipv4 address failed")

