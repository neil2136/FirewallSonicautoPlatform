from definition.settings_totp import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    
    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.10.0.30',
            'netmask': '255.255.255.0',
            'gateway': '10.10.0.1',
            'mgmt_https': True,
            'user_https': True,
        }
        rc = interface_ipv4.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
        
    def test_00_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '10.11.0.30',
            'netmask': '255.255.255.0',
            'gateway': '10.11.0.1',
            'mgmt-https': True,
            'mgmt-ssh': True,
            'mgmt-snmp': False,
            'user_https': True
            }
        output = interface_ipv4.config_interface(**x2_static)
        Assertion.assert_equal(output, True, "ERR: Config interface X2 failed")

    @repeat_method(2)
    def test_00_03_register_fw(self):
        rc = lc.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")    





