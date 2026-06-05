from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"        

    def test_00_01_Set_X2_Interface(self):
        x1_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '13.0.0.10',
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'mgmt_https': True,
            'mgmt_ping': True,
            'user_https': True

        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_00_02_Config_X1_Interface(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '12.0.0.100',
            'netmask': '255.255.255.0',
            'gateway': '12.0.0.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'user_https': True
        }
        resp = interface.config_interface(**x1_static)
        Assertion.assert_equal(resp, True, 'x1 not configured')
        
   
    def test_00_03_register_fw(self):
        license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
