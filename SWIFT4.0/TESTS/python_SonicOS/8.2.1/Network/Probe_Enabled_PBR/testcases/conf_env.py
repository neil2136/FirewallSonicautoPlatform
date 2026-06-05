from settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'dns1':'1.1.1.1',
            'gateway': Parameter.DUT_X1_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")    

    def test_00_02_add_ao(self):
        ao1 = {
            "object_type":"host",
            "name": 'wanhost',
            "zone": 'WAN',
            "value":  Parameter.WAN_GW
        }
        rc = ao.config_addressobject(**ao1)  
        ao2 = {
            "object_type":"host",
            "name": 'remotehost',
            "zone": 'WAN',
            "value":  Parameter.REMOTE_HOST
        }
        rc &= ao.config_addressobject(**ao2) 
        Assertion.assert_equal(rc, True, "ERR: Add ao failed.")    
