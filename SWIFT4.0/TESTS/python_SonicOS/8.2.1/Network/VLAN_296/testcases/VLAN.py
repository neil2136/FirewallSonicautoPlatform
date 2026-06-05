from definition.global_v import *

class TestVLAN_01(Test):
    uuid = "SOSAIOT-TC-57262"
    description= show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X4_LAN_Zone(self):
        x4_static = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x4_static)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static LAN Zone failed") 

    def test_02_Add_Vlan_subinterface_to_X4(self):
        x4_vlan1 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
        }
        x4_vlan2 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN2_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN2_IP,
        }
        rc1 = interface_obj.add_interface(**x4_vlan1)
        rc2 = interface_obj.add_interface(**x4_vlan2)
        Assertion.assert_equal(rc1&rc2, True, "ERR: Add Vlan interfaces to X4 failed") 


class TestVLAN_24(Test):
    uuid = "SOSAIOT-TC-57277"
    description= show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Delete_Vlan_subinterface(self):
        x4_vlan1 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': str(X4_VLAN1_ID),
        }
        x4_vlan2 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': str(X4_VLAN2_ID),
        }
        
        rc1 = interface_obj.del_interface( **x4_vlan1 )
        rc2 = interface_obj.del_interface( **x4_vlan2 )
        Assertion.assert_equal(rc1&rc2, True, "ERR: Delete X4 Vlan sub interfaces failed") 


class TestVLAN_26(Test):
    uuid = "SOSAIOT-TC-57279"
    description= show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_Vlan_subinterface_to_X4(self):
        x4_vlan1 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interface_obj.add_interface(**x4_vlan1)
        Assertion.assert_equal(rc1, True, "ERR: Add Vlan interfaces to X4 failed")

    @repeat_method(3)
    def test_02_Verify_Vlan_subinterface_PC_management_DUT(self):
        fw.api_logout()
        flag = False
        command = 'python3 ' +  bin_path + 'login_DUT_from_vlan_interface.py -i ' + Parameter.X4_VLAN1_IP + ' -a login'
        ret = PC2_login.send_command( command )
        if re.search(r'True', ret):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Login DUT from vlan subinterface failed")     


class TestVLAN_37(Test):
    uuid = "SOSAIOT-TC-57290"
    description= show_testcase_info(Parameter.TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X2_LAN_Zone(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static LAN Zone failed") 

    def test_02_verify_traffic_from_X2_to_X4_sub_interface(self):
        flag = 0
        os.system(f'route add -net {Parameter.X4_VLAN1_SUB} netmask {Parameter.MASK} gw {Parameter.X2_IP}')
        PC2_login.send_command(f'route add -host {PC1_ETH3_IP} gw {Parameter.X4_VLAN1_IP}')
        ping_result = os.popen(f'ping {PC2_ETH2_IP} -c 5').read()
        logger.info(ping_result)
        if '100% packet loss' in ping_result:
            flag = 1
            logger.info("ping traffic failed")
        Assertion.assert_equal(flag, 0, f"ERR: Traffic from  X2 host to X4 subinterface host failed")

class TestVLAN_39(Test):
    uuid = "SOSAIOT-TC-57292"
    description= show_testcase_info(Parameter.TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_Vlan_subinterface_to_X4(self):
        x4_vlan2 = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN2_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN2_IP,
        }
        rc1 = interface_obj.add_interface(**x4_vlan2)
        Assertion.assert_equal(rc1, True, "ERR: Add Vlan interfaces to X4 failed") 

    def test_02_verify_traffic_from_X4_sub_interface1_to_X4_sub_interface2(self):
        flag = 0
        PC2_login.send_command(f'route add -host {PC4_ETH2_IP} gw {Parameter.X4_VLAN1_IP}')
        PC4_login.send_command(f'route add -host {PC2_ETH2_IP} gw {Parameter.X4_VLAN2_IP}')
        ping_result = str( PC4_login.send_command(f'ping {PC2_ETH2_IP} -c 5') )
        logger.info(ping_result)
        if '100% packet loss' in ping_result:
            flag = 1
            logger.info("ping traffic failed")
        Assertion.assert_equal(flag, 0, f"ERR: Traffic from  X4 subinterface1 host to X4 subinterfaces host failed")
