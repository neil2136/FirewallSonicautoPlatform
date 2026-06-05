from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_x2_to_lan(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_lan_arm_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


