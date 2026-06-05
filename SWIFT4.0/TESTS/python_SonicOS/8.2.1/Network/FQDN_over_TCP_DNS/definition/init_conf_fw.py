from definition.settings import *


class TestConfigFW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("Config X1 interface")
        res = interfacev4api.config_interface(**x1_wan_v4_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_Config_X1_V6(self):
        logger.info("config X1 interface V6")
        rc = interfacev6api.config_interface_ipv6(**x1_wan_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv6 to static failed")

    def test_03_Config_X2(self):
        logger.info("Config X2 interface")
        res = interfacev4api.config_interface(**x2_lan_v4_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    def test_04_Config_X2_V6(self):
        logger.info("config X2 interface V6")
        rc = interfacev6api.config_interface_ipv6(**x2_lan_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv6 to static failed")

    @repeat_method(10)
    def test_05_register_fw(self):
        logger.info("Sleep 20s before registering firewall")
        time.sleep(20)
        res = licensecli.register("online")
        Assertion.assert_equal(res, True, "ERR: Register fw failed")

    def test_06_add_addr_obj(self):
        rc_ao_1 = aoapi.config_addressobject(**fqdn_ao_1_dict)
        rc_ao_2 = aoapi.config_addressobject(**fqdn_ao_2_dict)
        rc = [rc_ao_1, rc_ao_2]
        Assertion.assert_equal(all(rc), True, "ERR: Add AO for DNS test failed.")
