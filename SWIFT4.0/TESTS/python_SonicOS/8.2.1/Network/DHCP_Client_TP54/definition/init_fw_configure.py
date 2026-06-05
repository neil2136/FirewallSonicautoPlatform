from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_as_dhcp_mode(self):
        res = interfacev4api.config_interface(**x1_dhcp_dict)
        # res &= interfacev4api.disable_interface(name='X1')
        # res &= interfacev4api.enable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: Configure X1 status to DHCP failed")

    def test_02_restart_fw(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: restart fw failed")

    @repeat_method(3)
    def test_03_register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

