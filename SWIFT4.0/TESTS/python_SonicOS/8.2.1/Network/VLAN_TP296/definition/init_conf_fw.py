from definition.settings import *


class TestConfigFW_Local(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.10.0.168',
            'netmask': '255.255.255.0',
            'gateway': '10.10.0.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }

        rc = interfacev4api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
