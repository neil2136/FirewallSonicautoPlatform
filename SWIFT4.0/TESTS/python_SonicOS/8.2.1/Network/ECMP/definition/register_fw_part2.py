from definition.settings_part2 import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_config_x1_to_wan(self):
        x1_static_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '13.11.1.1',
            'dns1':  Parameter.DNS1,
            'dns2':  Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }

        res = interfacev4api.config_interface(**x1_static_dict)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static wan failed")

    @repeat_method(10)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

