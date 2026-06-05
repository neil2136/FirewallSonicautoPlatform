from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"        

    def test_00_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    @repeat_method(5)
    def test_register_fw(self):
        # license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
