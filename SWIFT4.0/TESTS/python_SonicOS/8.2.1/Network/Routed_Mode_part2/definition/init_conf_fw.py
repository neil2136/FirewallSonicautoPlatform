from definition.settings import *


class TestConfigFW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_Config_X0_ipv4(self):
        logger.info("config x0 ipv4 interface... ")
        rc = interface_obj.config_interface(**x0_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_02_Config_X0_ipv6(self):
        logger.info("config x0 ipv6 interface... ")
        rc = interface_obj_v6.config_interface_ipv6(**x0_lan_ipv6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X0 ipv6 failed!")

    def test_03_Config_X1_ipv4(self):
        logger.info("config x1 ipv4 interface... ")
        rc = interface_obj.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_04_Config_X1_ipv6(self):
        logger.info("config x1 ipv6 interface... ")
        rc = interface_obj_v6.config_interface_ipv6(**x1_wan_ipv6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X1 ipv6 failed!")

    def test_05_Config_X4_vlan_ipv4(self):
        logger.info("config x4 vlan interface... ")
        rc = interface_obj.add_interface(**x4_vlan1_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 vlan interface failed")
        resp = interface_obj.get_interface_status('x4:V' + str(X4_VLAN1_ID))
        logger.info(f'....show x4 vlan subinterface configuration{resp}')

    @repeat_method(10)
    def test_06_Register_fw(self):
        time.sleep(20)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
