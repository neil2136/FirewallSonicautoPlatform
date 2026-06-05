from definition.settings import *

class TestConf_FW(Test):
    uuid="NonTC"
    goto_teardown = True
    
        
    def test_01_config_x2(self):
        x2_static = {
            'if': 'X2',
            'zone': "DMZ",
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = interfacev4api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')
        
    def test_02_config_x3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = interfacev4api.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, 'ERR: config X3 failed')