from definition.settings import *


class TestMacSpoof_2(Test):
    uuid = "SOSAIOT-TC-56844"
    description= show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_interface_settings(self):
        flag = False
        output = mac_obj.get_mac_anti_spoof_settings(version = 4, name = 'X2') 
        if len( output['mac_ip_anti_spoof']['interface'] ) == 1 and \
            output['mac_ip_anti_spoof']['interface'][0]['name'] == 'X2':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get mac-ip anti-spoof intereface settings failed")

    def test_02_Get_all_interfaces_settings(self):
        flag = False
        interface_name = []
        output = mac_obj.get_mac_anti_spoof_settings(version = 4)
        if len( output['mac_ip_anti_spoof']['interface'] ) == 4:
            for info in output['mac_ip_anti_spoof']['interface']:
                interface_name.append(info['name'])
            interface_name = sorted(interface_name)
            if interface_name == ['X0', 'X1', 'X2', 'X3']:
                flag = True
        elif len( output['mac_ip_anti_spoof']['interface'] ) == 5:
            for info in output['mac_ip_anti_spoof']['interface']:
                interface_name.append(info['name'])
            interface_name = sorted(interface_name)
            if interface_name == ['W0', 'X0', 'X1', 'X2', 'X3']:
                flag = True
        else:
            logger.info("Verify interfaces mac-ip anti spoof info failed")
        Assertion.assert_equal(flag, True, "ERR: get mac-ip anti-spoof intereface settings failed")


class TestMacSpoof_3(Test):
    uuid = "SOSAIOT-TC-56846"
    description= show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_interface_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X2',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X2', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit mac-ip anti-spoof intereface settings failed")

    def test_02_Get_interface_settings(self):
        flag = False
        output = mac_obj.get_mac_anti_spoof_settings(version = 4, name = 'X2') 
        if output['mac_ip_anti_spoof']['interface'][0]['name'] == 'X2' and \
            output['mac_ip_anti_spoof']['interface'][0]['enable'] == True:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Edit mac-ip anti-spoof intereface settings failed")


class TestMacSpoof_16(Test):
    uuid = "SOSAIOT-TC-56842"
    description= show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_arp_entry(self): 
        logger.info(Parameter.PC2_ETH0_MAC)
        add_arp = {
            "arp":{
                "entry":[
                    {
                        "ip":PC2_ETH0_IP,
                        "mac":Parameter.PC2_ETH0_MAC,
                        "interface":"X3",
                        "publish":False,
                        "bind_mac":False,
                        "dynamic":False
                    }
                ]
            }
        }
        ret2 = arp_obj.add_arp_entry( **add_arp)
        logger.info(ret2)
        Assertion.assert_equal(ret2, True, "ERR: Add static arp failed")
           
    def test_02_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': True, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_03_verify_cache(self):
        flag = False
        output = mac_obj.get_reporting_cache()
        logger.info(output)
        for entry in output:
            if entry['ip_address'] == PC2_ETH0_IP:
                flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify cache failed")

    def test_04_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_05_verify_cache(self):
        flag = False
        output = mac_obj.get_reporting_cache()
        logger.info(output)
        for entry in output:
            if entry['ip_address'] == PC2_ETH0_IP:
                flag = True
        Assertion.assert_equal(flag, False, "ERR: Verify cache failed")

    def test_06_del_static_arp_entry(self): 
        ret = arp_obj.delete_arp_entry(ip = PC2_ETH0_IP, mac = Parameter.PC2_ETH0_MAC, interface = 'X3')
        Assertion.assert_equal(ret, True, "ERR: del static arp failed")


class TestMacSpoof_17(Test):
    uuid = "SOSAIOT-TC-56843"
    description= show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': True,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_02_add_dhcp_scope_for_X3(self):
        dynamic_entry1 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "12.12.3.20",
                                "to": "12.12.3.50",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "12.12.3.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret = dhcp_obj.add_dhcp_server_scope_dynamic( **dynamic_entry1 )
        Assertion.assert_equal(ret, True, "ERR: Add dynamic entries to X3 failed")

    @repeat_method(5)
    def test_03_verify_result(self):
        rc1 = False
        rc2 = False
        PC2_login.send_command("ip -4 a flush dev eth0")
        output = PC2_login.send_command("ip a show eth0")
        logger.info(output) 
        PC2_login.send_command("dhclient -r eth0")
        output = PC2_login.send_command("ip a show eth0")
        logger.info(output) 
        PC2_login.send_command("dhclient -nw eth0")
        time.sleep(10)
        output = PC2_login.send_command("ip a show eth0")
        logger.info(output)
        match = re.search(r'(12.12.3.\d{2})', output, re.I)
        if match:
            rc1 = True
            logger.info('PC2 eth0 get IP address ' + match.group(1))
        else:
            logger.info('PC2 eth0 failed to get IP adddress.')
        time.sleep(5)
        break_flag = False
        for i in range (1, 10):
            time.sleep(5)
            output = mac_obj.get_reporting_cache()
            logger.info(output)
            if output:
                for entry in output:
                    if entry['interface'] == 'X3':
                        rc2 = True
                        break_flag = True
                        break
                if break_flag:
                    break
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Verify result failed")

    def test_04_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_05_verify_cache(self):
        flag = False
        output = mac_obj.get_reporting_cache()
        logger.info(output)
        for entry in output:
            if entry['ip_address'] == PC2_ETH0_IP:
                flag = True
        Assertion.assert_equal(flag, False, "ERR: Verify cache failed")
 
    def test_06_restore_configuration(self):
        PC2_login.send_command("dhclient -r eth0")
        time.sleep(3)
        PC2_login.send_command("ifconfig eth0 {} netmask 255.255.255.0".format(PC2_ETH0_IP))
        output = PC2_login.send_command("ip a show eth0")
        logger.info(output)
        ret = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'dynamic', p1 = '12.12.3.20', p2 = '12.12.3.50' )
        Assertion.assert_equal(ret, True, "ERR: Restore configuration failed")


class TestMacSpoof_20(Test):
    uuid = "SOSAIOT-TC-56845"
    description= show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': True,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_02_add_anti_spoof_cache(self): 
        add_cache = {
            "mac_ip_anti_spoof": {
                "cache": {
                    "entry": [
                        {
                            "ip": PC2_ETH0_IP,
                            "mac": "121212121212",
                            "interface": "X3",
                            "router": False,
                            "blacklisted": False,
                        }
                    ]
                }
            }
        }
        ret = mac_obj.add_anti_spoof_cache( **add_cache)
        Assertion.assert_equal(ret, True, "ERR: Add anti spoof cache failed")

    def test_03_verify_traffic(self):
        flag = False
        os.system("route add -host {} gw {}".format(PC2_ETH0_IP, FIREWALL))
        PC2_login.send_command("route add -host {} gw {}".format(PC1_ETH0_IP, X3_IP))
        output = PC2_login.send_command("route -n")
        logger.info(output)
        PC2_login.send_command("ip n flush all")
        output = PC2_login.send_command("ping {} -c 5".format(PC1_ETH0_IP))
        logger.info(output)
        if '100% packet loss' in output: 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify traffic failed")

    def test_04_delete_anti_spoof_cache(self): 
        ret = mac_obj.delete_anti_spoof_cache( ip = PC2_ETH0_IP, mac = '121212121212', interface = 'X3')
        Assertion.assert_equal(ret, True, "ERR: Delete anti spoof cache failed")

    def test_05_edit_X3_anti_spoof_settings(self):
        spoof_edit = {
            'mac_ip_anti_spoof': {
                'interface': [
                    {
                        'name': 'X3',
                        'enable': True,
                        'static_arp': False, 
                        'dhcp_server': False,
                        'dhcp_relay': False,
                        'arp_lock': False,
                        'arp_watch': False,
                        'enforce_ingress': False,
                        'spoof_detection': False,
                        'allow_management': True
                    }
                ]
            }
        }
        output = mac_obj.edit_mac_anti_spoof_settings(version = 4, name = 'X3', **spoof_edit) 
        Assertion.assert_equal(output, True, "ERR: Edit X3 mac-ip anti-spoof settings failed")

    def test_06_verify_traffic(self):
        flag = False
        PC2_login.send_command("ip n flush all")
        output = PC2_login.send_command("ping {} -c 5".format(PC1_ETH0_IP))
        logger.info(output)
        if '100% packet loss' not in output: 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify traffic failed")