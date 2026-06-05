from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_configure_x1_v4(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': Parameter.X1_GW
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')
        
    @repeat_method(5)
    def test_02_register_fw(self):
        time.sleep(10)
        res = licensecli.register("online")
        Assertion.assert_equal(res, True, "ERR: register fw failed")
