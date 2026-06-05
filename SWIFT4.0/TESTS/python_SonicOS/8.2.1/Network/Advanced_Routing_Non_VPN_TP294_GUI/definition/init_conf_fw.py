from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
