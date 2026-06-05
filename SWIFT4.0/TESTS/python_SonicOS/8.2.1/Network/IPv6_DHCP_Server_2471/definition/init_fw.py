from definition.global_v import *

class TestInitConfig(Test):
    uuid = 'NonTC'
   
    def test_01_Config_Network(self):
        cmd_list = [f"ifconfig eth1 {PC1_WAN_IP}/24 up",
            f"ifconfig eth2 {PC1_DMZ_IP}/24 up",
            f"ifconfig eth3 {PC1_SEC_LAN_IP}/24 up"]
        ret = 0
        for cmd in cmd_list:
            logger.info(cmd)
            ret = ret + os.system(cmd)
        Assertion.assert_equal(ret, 0, "ERR:config interface ip failed on PC1")

    def test_02_Set_X1_IP(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': X1_IP,
            'gateway': X1_GW,
            'dns1': X1_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_Set_X2_IP_and_DMZ(self):
        x2_static = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'static',
            'ip': DMZ_IP,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IP and DMZ failed")


    def test_04_Set_X3_IP_and_LAN(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': SEC_LAN_IP,
        }
        rc = interface_obj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IP and LAN failed")
      

        
