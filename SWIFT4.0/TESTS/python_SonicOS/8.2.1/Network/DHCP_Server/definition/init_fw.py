from definition.global_v import *

class TestInitConfig(Test):
    uuid = 'NonTC'
   
    def test_01_Set_X2_IP_and_LAN(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': X2_IP,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IP and LAN failed")

    def test_02_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': '255.255.255.0',
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

