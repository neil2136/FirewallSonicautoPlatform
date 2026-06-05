from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
			'dns1': Params.G_DNS1,
			'dns2': Params.G_DNS2,
			'dns3': Params.G_DNS3,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_https': True
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(3)
    def test_00_03_Register_fw(self):
        time.sleep(10)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


