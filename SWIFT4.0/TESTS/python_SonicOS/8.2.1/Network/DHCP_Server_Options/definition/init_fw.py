from definition.global_v import *

class TestInitConfig(Test):
    uuid = 'NonTC'
   
    def test_01_Set_X2_IP_and_LAN(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': FW_X2_IP,
            'netmask':MASK
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IP and LAN failed")

    def test_01_Config_X3(self):
        logger.info("config x3 interface... ")
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': FW_X3_IP,
            'netmask': '255.255.255.0',
        }
        rc = interface_obj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

