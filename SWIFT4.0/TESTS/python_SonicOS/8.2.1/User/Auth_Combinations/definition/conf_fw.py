from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X0(self):
        x0_interface = {
            'if': 'X0',
            'zone': 'LAN',
            'ip': FIREWALL,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x0_interface)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_Config_X2(self):
        logger.info("config x2 interface... ")
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(3)
    def test_04_Register_fw(self):
        time.sleep(10)
        rc = lc.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
