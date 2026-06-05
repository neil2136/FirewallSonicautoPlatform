from definition.settings import *

class config_interface(Test):
    uuid = 'NonTC'
    logger.info('debug tool')
    stage_description = 'Configuring x3 interface'
    logger.info(stage_description)
    def test_config_interface(self):
        wan_interface = {
            'if': 'X3',
			'zone': 'WAN',
			'mode': 'static',
			'ip': '10.10.10.10',
			'netmask': '255.255.255.0',
			'gateway': '10.10.10.1',
			'dns': '10.5.3.52',
			'mgmt-https': True,
			'mgmt-ssh': True,
			'mgmt-snmp': False,
			'user_https': True
		}
        response = interfaceapi.config_interface(**wan_interface)
        logger.info(response)
        if response:
            logger.info('Addres Object Created')
        else:
            logger.info('Error in creating Address Object')
        logger.info(response)


class Test_01_Configure_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48518"
    description = show_testcase_info(TESTPLAN, "1", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_vlan_interface(self):
        rs = interfacecli.add_interface(**vlan_interface_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(interface='x3 vlan 200')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
            vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: configure vlan interface failed")


class Test_02_Edit_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48519"
    description = show_testcase_info(TESTPLAN, "2", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")
        
    def test_01_edit_vlan_interface(self):
        rs = interfacecli.config_interface(**edit_vlan_interface_dict)
        logger.info(f'show edit a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(interface='x3 vlan 200')
        logger.info(f'show x0 interface status: {show_result}')
        output = True if 'ip ' + \
            vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(
            output, True, "ERR: configure vlan interface failed")
        

class Test_03_Delete_Vlan_Interface(Test):
    uuid = "SOSAIOT-TC-48520"
    description = show_testcase_info(TESTPLAN, "3", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_vlan_interface(self):
        rs = interfacecli.del_interface(**vlan_interface_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(interface='x3 vlan 200')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
            vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(output, False, "ERR: configure vlan interface failed")


class Test_04_Delete_multiple_Vlan_Interfaces(Test):
    uuid = "SOSAIOT-TC-48521"
    description = show_testcase_info(TESTPLAN, "4", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_multiple_vlan_interface(self):
        rs = interfacecli.del_all_vlan_interfaces()
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(interface='x3 vlan 200')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
            vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(output, False, "ERR: configure vlan interface failed")


class Test_05_Delete_All_Vlan_Interfaces(Test):
    uuid = "SOSAIOT-TC-48522"
    description = show_testcase_info(TESTPLAN, "5", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_all_vlan_interface(self):
        rs = interfacecli.del_all_vlan_interfaces()
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = interfacecli.show_interface_status(interface='x3 vlan 200')
        logger.info(f'show x2 interface status: {show_result}')
        output = True if 'ip ' + \
            vlan_interface_dict['ip'] in show_result else False
        Assertion.assert_equal(output, False, "ERR: configure vlan interface failed")


class Test_06_Add_ARP_entries(Test):
    uuid = "SOSAIOT-TC-48523"
    description = show_testcase_info(TESTPLAN, "6", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Add_Arp_entries(self):
        rs = arpcli.add_arp_entry(**arp_entry_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = arpcli.show_arp_entry()
        logger.info(f'show arp entry status: {show_result}')
        # Assertion.assert_equal(show_result, True, "ERR: configure vlan interface failed")


class Test_07_Edit_ARP_entries(Test):
    uuid = "SOSAIOT-TC-48524"
    description = show_testcase_info(TESTPLAN, "7", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Edit_Arp_entries(self):
        rs = arpcli.edit_arp_entry(arp_entry_dict,edit_arp_entry_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = arpcli.show_arp_entry()
        logger.info(f'show arp entry status: {show_result}')
        # Assertion.assert_equal(show_result, "'192.168.168.100'", "ERR: configure vlan interface failed")


class Test_08_Delete_ARP_entry(Test):
    uuid = "SOSAIOT-TC-48525"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Delete_ARP_entry(self):
        rs = arpcli.del_arp_entry(**arp_entry_dict)
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = arpcli.show_arp_entry()
        logger.info(f'show arp entry status: {show_result}')
        # Assertion.assert_equal(show_result, "'192.168.168.100'", "ERR: configure vlan interface failed")


class Test_09_Delete_all_ARP_entry(Test):
    uuid = "SOSAIOT-TC-48527"
    description = show_testcase_info(TESTPLAN, "9", description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Delete_all_ARP_entry(self):
        rs = arpcli.del_all_arp_entries()
        logger.info(f'show add a vlan interface result: {rs}')
        show_result = arpcli.show_arp_entry()
        logger.info(f'show arp entry status: {show_result}')
        # Assertion.assert_equal(show_result, "'192.168.168.100'", "ERR: configure vlan interface failed")
