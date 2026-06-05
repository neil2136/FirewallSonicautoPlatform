from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"        

    def test_00_01_Set_X1_Interface(self):
        x1_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.0.0.10',
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'mgmt_https': True,
            'mgmt_ping': True,
            'user_https': True

        }
        rc = configure_user.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
        
   
    # def test_00_02_register_fw(self):
    #     license = LicenseCli(fw_cli)
    #     rc = license.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")
