from definition.init_param import *


class Test_01_Routed_Mode_tc_66(Test):
    uuid = "SOSAIOT-TC-57186"
    description= show_testcase_info(Parameter.TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_interface_x2(self):
        logger.info('config interface x2...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                'any': True    #network.py 298
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_get_nat_policy_and_check(self):
        logger.info('get nat policy and check...')
        flag = False
        output = natObj.get_nat_policy()
        logger.info('check...')

        # {'ipv4': {'uuid': '179e5ab3-cbd4-103a-0800-2cb8ed6d798c', 'name': 'Default NAT Policy',
        #  'enable': True, 'comment': 'Auto-added No-NAT Policy for Inbound to X2', 'dns_doctoring': False, 
        #  'priority': {'auto': True}, 'inbound': 'any', 'outbound': 'X2', 'source': {'any': True}, 
        #  'translated_source': {'original': True}, 'destination': {'name': 'X2 Subnet'}, 
        #  'translated_destination': {'original': True}, 'service': {'any': True}, 
        #  'translated_service': {'original': True}, 'ticket': {'tag1': '', 'tag2': '', 'tag3': ''}}},

        if re.search(r"Auto-added No-NAT Policy for Outbound from X2", str(output), re.S|re.I)  and \
            re.search(r"Auto-added No-NAT Policy for Inbound to X2", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get nat policy and check failed")


class Test_02_Routed_Mode_tc_67(Test):
    uuid = "SOSAIOT-TC-57187"
    description= show_testcase_info(Parameter.TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
        
    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_ssh': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_config_interface_x0(self):
        logger.info('config interface x0...')
        x0 = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X0_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X0_GW,
            'routed_mode': {
                "interface": "X1"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x0)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_03_verify_traffic(self):
        logger.info('verify traffic...')
        flag = False
        cmd = 'route add -host {} gw 192.168.168.168'.format(PC2_ETH1_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        local_host.send_command(cmd)
        capture_cmd = "nohup tshark -i eth1 -f 'icmp' -a duration:20 -V > /tmp/packet.txt 2>&1 &"
        pc1_ssh = Host(PC1_ETH2_IP, user='root', password='password')

        logger.info('run capture cmd in pc1:{}'.format(capture_cmd))
        pc1_ssh.send_command(capture_cmd)
        logger.info('run capture cmd in pc2:{}'.format(capture_cmd))
        pc2_ssh.send_command(capture_cmd)
        local_host.send_command('ping {} -c 5'.format(PC2_ETH1_IP))
        output_pc1 = local_host.send_command('cat /tmp/packet.txt')
        output_pc2 = pc2_ssh.send_command('cat /tmp/packet.txt')
        if re.search(r" Source: 192.168.168.169.*Destination: 13.0.0.100", str(output_pc1), re.S|re.I|re.M)  and \
            re.search(r"Source: 192.168.168.169.*Destination: 13.0.0.100", str(output_pc2), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify traffic failed")


class Test_03_Routed_Mode_tc_68(Test):
    uuid = "SOSAIOT-TC-57188"
    description= show_testcase_info(Parameter.TESTPLAN, '68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '68')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_interface_x2_disable_routed_mode(self):
        logger.info('config interface x2...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_get_nat_policy_and_check(self):
        logger.info('get nat policy and check...')
        flag = True
        output = natObj.get_nat_policy()
        logger.info('check...')
        if re.search(r"Auto-added No-NAT Policy for Inbound to X2", str(output), re.S|re.I)  and \
            re.search(r"Auto-added No-NAT Policy for Outbound from X2", str(output), re.S|re.I) :
            flag = False
        Assertion.assert_equal(flag, True, "ERR: get nat policy and check failed")

class Test_04_Routed_Mode_tc_69(Test):
    uuid = "SOSAIOT-TC-57189"
    description= show_testcase_info(Parameter.TESTPLAN, '69', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '69')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_new_custom_zones(self):
        logger.info('add new custom zones...')
        zone1 = {
            "zones": [
                {
                    "name": "test1",
                    "security_type": "trusted",
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_to_lower": True,
                        "allow_from_higher": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            },
                            "enable": False
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {}
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "header": {},
                            "footer": {}
                        }
                    }
                }
            ]
        }
        zone2 = {
            "zones": [
                {
                    "name": "test2",
                    "security_type": "public",
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_to_lower": True,
                        "allow_from_higher": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            },
                            "enable": False
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {}
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "header": {},
                            "footer": {}
                        }
                    }
                }
            ]
        }
        zone3 = {
            "zones": [
                {
                    "name": "test3",
                    "security_type": "wireless",
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_to_lower": True,
                        "allow_from_higher": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            },
                            "enable": False
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {}
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "header": {},
                            "footer": {}
                        }
                    }
                }
            ]
        }
        rc = zone_obj.add_zone_object(**zone1)
        rc &= zone_obj.add_zone_object(**zone2)
        rc &= zone_obj.add_zone_object(**zone3)
        Assertion.assert_equal(rc, True, "ERR: add new zones failed")

    def test_02_config_interface_x2_in_zone_test1_and_verify_routed_mode(self):
        logger.info('config interface x2 in zone test1 and verify routed mode...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'test1',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        if re.search(r"zone.*test1.*routed_mode\W+any\W+True", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 in zone test1 and verify routed mode failed")

    def test_03_config_interface_x2_in_zone_test2_and_verify_routed_mode(self):
        logger.info('config interface x2 in zone test2 and verify routed mode...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'test2',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        if re.search(r"zone.*test2.*routed_mode\W+any\W+True", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 in zone test2 and verify routed mode failed")

    def test_04_config_interface_x2_in_zone_test3_and_verify_routed_mode(self):
        logger.info('config interface x2 in zone test3 and verify routed mode...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'test3',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.0.0',
            'routed_mode': {
                'any': True    
            },
            'sp_limit': 2,
            'reserve_address': 'dynamic',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        if re.search(r"zone.*test3.*routed_mode\W+any\W+True", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 in zone test3 and verify routed mode failed")


class Test_05_Routed_Mode_tc_70(Test):
    uuid = "SOSAIOT-TC-57190"
    description= show_testcase_info(Parameter.TESTPLAN, '70', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '70')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_config_x2_wan_and_verify_routed_mode(self):
        logger.info('config interface x2 WAN and verify routed mode...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'wan',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        if re.search(r"zone.*WAN.*routed_mode\W+any\W+True", str(output), re.S|re.I) == None:
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 in zone WAN and verify routed mode failed")

    def test_02_config_x3_DMZ_and_check_nat_policy(self):
        logger.info('config interface x3 DMZ and check nat policy...')
        flag = False
        x3 = {
            'if': 'X3',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x3)
        output = natObj.get_nat_policy()
        logger.info('check...')
        if re.search(r"Auto-added No-NAT Policy for Inbound to X3", str(output), re.S|re.I)  and \
            re.search(r"Auto-added No-NAT Policy for Outbound from X3", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X3 in zone DMZ and check nat policy failed")


    def test_03_config_x3_WAN_and_check_nat_policy(self):
        logger.info('config interface x3 WAN and check nat policy...')
        flag = False
        x3 = {
            'if': 'X3',
            'zone': 'wan',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'dns1': Params.G_DNS1,
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x3)
        output = natObj.get_nat_policy()
        logger.info('check...')
        if re.search(r"Auto-added No-NAT Policy for Inbound to X3", str(output), re.S|re.I) == None and \
            re.search(r"Auto-added No-NAT Policy for Outbound from X3", str(output), re.S|re.I) == None:
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X3 in zone WAN and check nat policy failed")
    

class Test_06_Routed_Mode_tc_71(Test):
    uuid = "SOSAIOT-TC-57191"
    description= show_testcase_info(Parameter.TESTPLAN, '71', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_config_x2_LAN_and_check_nat_policy(self):
        logger.info('config interface x2 LAN and check nat policy...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'routed_mode': {
                'any': True    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = natObj.get_nat_policy()
        logger.info('check...')
        if re.search(r"Auto-added No-NAT Policy for Inbound to X2", str(output), re.S|re.I)  and \
            re.search(r"Auto-added No-NAT Policy for Outbound from X2", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 in zone LAN and check nat policy failed")
    
    def test_02_config_x2_wire_mode_and_check_nat_policy_and_routed_mode(self):
        logger.info('config interface x2 to wire mode and check nat policy and routed mode...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.unassign_interface(interface='X3')
        rc &= interface_obj.config_interface(**x2)
        output = natObj.get_nat_policy()
        output2 = interface_obj.get_interface_status('X2')
        logger.info('check...')
        if re.search(r"Auto-added No-NAT Policy for Inbound to X2", str(output), re.S|re.I)  and \
            re.search(r"Auto-added No-NAT Policy for Outbound from X2", str(output), re.S|re.I)  and\
            re.search(r"zone.*LAN.*routed_mode\W+any\W+True", str(output2), re.S|re.I) == None:
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 to wire mode and check nat policy and routed mode failed")

class Test_07_Routed_Mode_tc_72(Test):
    uuid = "SOSAIOT-TC-57192"
    description= show_testcase_info(Parameter.TESTPLAN, '72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_config_x2_in_wan_and_x3_in_lan(self):
        logger.info('config interface x2 in wan zone and x3 in lan zone...')
        x2 = {
            'if': 'X2',
            'zone': 'wan',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'routed_mode': {
                'interface': 'X2'    
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        rc &= interface_obj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X2 in wan zone and x3 in lan zone failed")

    def test_02_switch_x2_from_wan_to_lan(self):
        logger.info('config interface x2 from wan to lan zone...')
        x2 = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, False, "ERR: switch X2 from wan to lan zone failed")
 