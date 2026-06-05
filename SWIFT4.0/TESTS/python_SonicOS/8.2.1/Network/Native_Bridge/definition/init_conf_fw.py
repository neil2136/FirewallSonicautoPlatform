from definition.settings import *


class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '11.1.1.1',
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc1, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc1, True, "ERR: Config X1 to static failed")
