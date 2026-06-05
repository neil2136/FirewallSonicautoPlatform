from definition.init_param import *

class Test_01_DHCP_Multi_Scope_2372_tc_8(Test):
    uuid = "SOSAIOT-TC-56882"
    description= show_testcase_info(Parameter.TESTPLAN, '1714164', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714164')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_default_trusted_relay_agent_list(self):
        logger.info('verify default trusted relay agent list...')
        flag = False
        output = dhcpCli.show_address_group_trusted_relay_agent()
        logger.info(output)
        if re.search(r'name "Default Trusted Relay Agent List', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify default trusted relay agent list failed")


class Test_02_DHCP_Multi_Scope_2372_tc_9(Test):
    uuid = "SOSAIOT-TC-56883"
    description= show_testcase_info(Parameter.TESTPLAN, '1714173', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714173')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_default_dynamic_scope(self):
        logger.info('delete default dynamic scope...')
        rc = dhcpObj.delete_dhcp_server_scope_v4(scope='dynamic', p1='192.168.168.1', p2='192.168.168.167')
        Assertion.assert_equal(rc, True, "ERR: check the scope not exits failed")

    def test_02_add_dynamic_scope_bound_to_interface(self):
        logger.info('add dynamic scope bound to interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.168.220",
                                "to": "192.168.168.230",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "192.168.168.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**scope)
        Assertion.assert_equal(rc, True, "ERR: add dynamic scope not bound to any interface failed")
    
    def test_03_check_the_add_result(self):
        logger.info('check the add result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        if re.search(r'from\': \'192.168.168.220\', \'to\': \'192.168.168.230', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the add scope failed")


class Test_03_DHCP_Multi_Scope_2372_tc_10(Test):
    uuid = "SOSAIOT-TC-56868"
    description= show_testcase_info(Parameter.TESTPLAN, '1714088', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714088')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_dynamic_scope_bound_to_interface(self):
        logger.info('edit dynamic scope bound to interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.168.221",
                                "to": "192.168.168.230",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "192.168.168.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "0.0.0.0",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.edit_dhcp_server_scope_v4(scope='dynamic', p1='192.168.168.220', p2='192.168.168.230', **scope)
        Assertion.assert_equal(rc, True, "ERR: edit dynamic scope bound to interface failed")

    def test_03_check_the_edit_result(self):
        logger.info('check the edit result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        if re.search(r'from\': \'192.168.168.221\', \'to\': \'192.168.168.230', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the edit scope failed")


class Test_04_DHCP_Multi_Scope_2372_tc_11(Test):
    uuid = "SOSAIOT-TC-56869"
    description= show_testcase_info(Parameter.TESTPLAN, '1714089', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714089')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_dynamic_scope(self):
        logger.info('check the scope not exits...')
        rc = dhcpObj.delete_dhcp_server_scope_v4(scope='dynamic', p1='192.168.168.221', p2='192.168.168.230')
        Assertion.assert_equal(rc, True, "ERR: check the scope not exits failed")

    def test_02_check_the_delete_result(self):
        logger.info('check the delete result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        if not re.search(r'from\': \'192.168.168.221\', \'to\': \'192.168.168.230', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the delete result failed")


class Test_05_DHCP_Multi_Scope_2372_tc_12(Test):
    uuid = "SOSAIOT-TC-56870"
    description= show_testcase_info(Parameter.TESTPLAN, '1714090', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714090')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_scope_bound_to_interface(self):
        logger.info('add static scope bound to interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "192.168.168.245",
                                "mac": "112233445566",
                                "enable": True,
                                "name": "tc12",
                                "lease_time": 1440,
                                "default_gateway": "192.168.168.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_static(**scope)
        Assertion.assert_equal(rc, True, "ERR: add static scope bound to interface failed")

    def test_02_check_the_add_result(self):
        logger.info('check the add result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static(name='tc12')
        logger.info(output)
        ip = output['dhcp_server']['ipv4']['scope']['static'][0]['ip']
        if ip == '192.168.168.245':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the add scope failed")


class Test_06_DHCP_Multi_Scope_2372_tc_13(Test):
    uuid = "SOSAIOT-TC-56871"
    description= show_testcase_info(Parameter.TESTPLAN, '1714091', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714091')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_the_static_scope(self):
        logger.info('edit the static scope...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "192.168.168.246",
                                "mac": "112233445566",
                                "enable": True,
                                "name": "tc12",
                                "lease_time": 1440,
                                "default_gateway": "192.168.168.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "0.0.0.0",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.edit_dhcp_server_scope_v4(scope='static', p1='192.168.168.245', p2='112233445566', **scope)
        Assertion.assert_equal(rc, True, "ERR: edit the static scope failed")

    def test_02_check_the_edit_result(self):
        logger.info('check the edit result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static(name='tc12')
        logger.info(output)
        ip = output['dhcp_server']['ipv4']['scope']['static'][0]['ip']
        if ip == '192.168.168.246':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the edit scope failed")


class Test_07_DHCP_Multi_Scope_2372_tc_14(Test):
    uuid = "SOSAIOT-TC-56872"
    description= show_testcase_info(Parameter.TESTPLAN, '1714092', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714092')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_the_static_scope(self):
        logger.info('delete the static scope...')
        rc = dhcpObj.delete_dhcp_server_scope_v4(scope='static', p1='192.168.168.246', p2='112233445566')
        Assertion.assert_equal(rc, True, "ERR: delete the static scope failed")

    def test_02_check_the_delete_result(self):
        logger.info('check the delete result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static(name='tc12')
        logger.info(output)
        ip = output['dhcp_server']['ipv4']
        if ip == {}:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the delete scope failed")


class Test_08_DHCP_Multi_Scope_2372_tc_15(Test):
    uuid = "SOSAIOT-TC-56873"
    description= show_testcase_info(Parameter.TESTPLAN, '1714093', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714093')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_scope_not_bound_to_any_interface(self):
        logger.info('add dynamic scope not bound to any interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.1",
                                "to": "2.2.2.10",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.11",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**scope)
        Assertion.assert_equal(rc, True, "ERR: add dynamic scope not bound to any interface failed")

    def test_02_check_the_add_result(self):
        logger.info('check the add result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        ip1 = output['dhcp_server']['ipv4']['scope']['dynamic'][0]['from']
        ip2 = output['dhcp_server']['ipv4']['scope']['dynamic'][0]['to']
        if ip1 == '2.2.2.1' and ip2 == '2.2.2.10':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the add scope failed")


class Test_09_DHCP_Multi_Scope_2372_tc_16(Test):
    uuid = "SOSAIOT-TC-56874"
    description= show_testcase_info(Parameter.TESTPLAN, '1714094', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714094')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_dynamic_scope_not_bound_to_any_interface(self):
        logger.info('edit dynamic scope not bound to any interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.2",
                                "to": "2.2.2.10",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.11",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "0.0.0.0",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }        
        rc = dhcpObj.edit_dhcp_server_scope_v4(scope='dynamic', p1='2.2.2.1', p2='2.2.2.10', **scope)
        Assertion.assert_equal(rc, True, "ERR: edit scope not bound to any interface  failed")

    def test_02_check_the_edit_result(self):
        logger.info('check the edit result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        ip1 = output['dhcp_server']['ipv4']['scope']['dynamic'][0]['from']
        ip2 = output['dhcp_server']['ipv4']['scope']['dynamic'][0]['to']
        if ip1 == '2.2.2.2' and ip2 == '2.2.2.10':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the edit scope failed")


class Test_10_DHCP_Multi_Scope_2372_tc_17(Test):
    uuid = "SOSAIOT-TC-56875"
    description= show_testcase_info(Parameter.TESTPLAN, '1714095', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714095')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_the_added_dynamic_scope(self):
        logger.info('delete the added dynamic scope...')
        rc=dhcpObj.delete_dhcp_server_scope_v4(scope='dynamic', p1='2.2.2.2', p2='2.2.2.10')
        Assertion.assert_equal(rc, True, "ERR: delete the added dynamic scope failed")

    def test_02_check_the_delete_result(self):
        logger.info('check the delete result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_dynamic()
        logger.info(output)
        if not re.search(r'from\': \'2.2.2.2\', \'to\': \'2.2.2.10', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the delete scope failed")


class Test_11_DHCP_Multi_Scope_2372_tc_18(Test):
    uuid = "SOSAIOT-TC-56876"
    description= show_testcase_info(Parameter.TESTPLAN, '1714096', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714096')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_scope_not_bound_to_interface(self):
        logger.info('add static scope not bound to interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "3.3.3.1",
                                "mac": "122233445566",
                                "enable": True,
                                "name": "tc18",
                                "lease_time": 1440,
                                "default_gateway": "3.3.3.2",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc=dhcpObj.add_dhcp_server_scope_static(**scope)
        Assertion.assert_equal(rc, True, "ERR: add static scope not bound to interface failed")

    def test_02_check_the_add_result(self):
        logger.info('check the add result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static(name='tc18')
        logger.info(output)
        ip = output['dhcp_server']['ipv4']['scope']['static'][0]['ip']
        if ip == '3.3.3.1':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the add scope failed")


class Test_12_DHCP_Multi_Scope_2372_tc_19(Test):
    uuid = "SOSAIOT-TC-56877"
    description= show_testcase_info(Parameter.TESTPLAN, '1714097', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714097')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_the_added_static_scope(self):
        logger.info('edit the added static scope...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "3.3.3.2",
                                "mac": "122233445566",
                                "enable": True,
                                "name": "tc18",
                                "lease_time": 1440,
                                "default_gateway": "3.3.3.3",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "0.0.0.0",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.edit_dhcp_server_scope_v4(scope='static', p1='3.3.3.1', p2='122233445566', **scope)
        Assertion.assert_equal(rc, True, "ERR: edit the added static scope failed")

    def test_02_check_the_edit_result(self):
        logger.info('check the edit result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static(name='tc18')
        logger.info(output)
        ip = output['dhcp_server']['ipv4']['scope']['static'][0]['ip']
        if ip == '3.3.3.2':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the edit scope failed")


class Test_13_DHCP_Multi_Scope_2372_tc_20(Test):
    uuid = "SOSAIOT-TC-56878"
    description= show_testcase_info(Parameter.TESTPLAN, '1714099', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714099')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_the_static_scope(self):
        logger.info('delete the static scope...')
        rc=dhcpObj.delete_dhcp_server_scope_v4(scope='static', p1='3.3.3.2', p2='122233445566')
        Assertion.assert_equal(rc, True, "ERR: delete the added dynamic scope failed")

    def test_02_check_the_delete_result(self):
        logger.info('check the delete result...')
        flag = False
        output = dhcpObj.get_dhcp_server_scope_static()
        logger.info(output)
        ip = output['dhcp_server']['ipv4']
        if ip == {}:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check the delete scope failed")


class Test_14_DHCP_Multi_Scope_2372_tc_28(Test):
    uuid = "SOSAIOT-TC-56879"
    description= show_testcase_info(Parameter.TESTPLAN, '1714107', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714107')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info('config interface x2...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_add_dynamic_scope_bound_to_interface(self):
        logger.info('add dynamic scope bound to interface...')
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.2",
                                "to": "2.2.2.254",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.1",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**scope)
        Assertion.assert_equal(rc, True, "ERR: add dynamic scope bound to interface failed")

    def test_03_verify_client_get_ip_lease_from_dhcp_server(self):
        logger.info('verify client get ip lease from dhcp server...')
        flag = False
        cmds = (
            'pkill dhclient',
            'ifconfig eth1 0.0.0.0 0.0.0.0',
            'dhclient eth1',
        )
        for cmd in cmds:
            logger.info('run cmd in pc1:{}'.format(cmd))
            local_host.send_command(cmd)

        sleep(5)
        eth1_ip = local_host.send_command('ifconfig eth1')
        logger.info(eth1_ip)
        pid = local_host.send_command('pidof dhclient')
        match_str = re.search(r'inet\s+(2.2.2.\d+)', str(eth1_ip), re.S|re.I)
        if match_str:
            logger.info('get ip address of eth1:{}'.format(match_str.group(1)))
            local_host.send_command('dhclient -r eth1')
            local_host.send_command('kill {}'.format(pid))
            local_host.send_command('ifdown eth1')
            flag = True
        else:
            local_host.send_command('kill {}'.format(pid))
            local_host.send_command('ifdown eth1')
        Assertion.assert_equal(flag, True, "ERR: verify client get ip lease form dhcp server failed")


class Test_15_DHCP_Multi_Scope_2372_tc_32(Test):
    uuid = "SOSAIOT-TC-56880"
    description= show_testcase_info(Parameter.TESTPLAN, '1714112', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714112')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_the_added_dynamic_scope(self):
        logger.info('delete the added dynamic scope...')
        rc=dhcpObj.delete_dhcp_server_scope_v4(scope='dynamic', p1='2.2.2.2', p2='2.2.2.254')
        Assertion.assert_equal(rc, True, "ERR: delete the added dynamic scope failed")

    def test_02_add_static_scope(self):
        logger.info('add static scope not bound to interface...')
        eth1= local_host.send_command('ifconfig eth1')
        match_str = re.search(r'ether\s(\w+:\w+:\w+:\w+:\w+:\w+)', str(eth1), re.S|re.I)
        eth1_mac = match_str.group(1)
        scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "2.2.2.22",
                                "mac": eth1_mac,
                                "enable": True,
                                "name": "tc32",
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.1",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "wins": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": ""
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": ""
                                },
                                "generic_option": {},
                                "always_send_option": False
                            }
                        ]
                    }
                }
            }
        }
        rc=dhcpObj.add_dhcp_server_scope_static(**scope)
        Assertion.assert_equal(rc, True, "ERR: add static scope not bound to interface failed")
        
    def test_03_verify_client_get_ip_lease_from_dhcp_server(self):
        logger.info('verify client get ip lease from dhcp server...')
        flag = False
        cmds = (
            'pkill dhclient',
            'ifconfig eth1 0.0.0.0 0.0.0.0',
            'dhclient eth1',
        )
        for cmd in cmds:
            logger.info('run cmd in pc1:{}'.format(cmd))
            local_host.send_command(cmd)

        sleep(5)
        eth1_ip = local_host.send_command('ifconfig eth1')
        logger.info(eth1_ip)
        pid = local_host.send_command('pidof dhclient')
        match_str = re.search(r'inet\s+(2.2.2.22)', str(eth1_ip), re.S|re.I)
        if match_str:
            logger.info('get ip address of eth1:{}'.format(match_str.group(1)))
            local_host.send_command('dhclient -r eth1')
            local_host.send_command('kill {}'.format(pid))
            local_host.send_command('ifdown eth1')
            flag = True
        else:
            local_host.send_command('kill {}'.format(pid))
            local_host.send_command('ifdown eth1')
        Assertion.assert_equal(flag, True, "ERR: verify client get ip lease form dhcp server failed")


class Test_16_DHCP_Multi_Scope_2372_tc_67(Test):
    uuid = "SOSAIOT-TC-56881"
    description= show_testcase_info(Parameter.TESTPLAN, '1714150', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714150')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_dhcp_trusted_relay_agent_list(self):
        logger.info('enable trusted dhcp relay agent list...')
        dhcp = {
            "dhcp_server": {
                "ipv4": {
                    "trusted_relay_agents": "Default Trusted Relay Agent List",
                    "recycle_expired_lease": 0
                }
            }
        }

        rc = dhcpObj.config_dhcp_server_settings(**dhcp)
        Assertion.assert_equal(rc, True, "ERR: enable trusted dhcp relay agent list failed")

    def test_02_download_tsr_and_verify_dhcp_setting(self):
        logger.info('download tsr and verify dhcp setting...')
        flag = False
        output = diagObj.get_tsr_part(func = 'Network', lab1 = 'DHCP Server')
        logger.info(output)
        if re.search(r'Trusted DHCP Relay Agent List Enabled', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: download tsr and verify dhcp setting failed')


