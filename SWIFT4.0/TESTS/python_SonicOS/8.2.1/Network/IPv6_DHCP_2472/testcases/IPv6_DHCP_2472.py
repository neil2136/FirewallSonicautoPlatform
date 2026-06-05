from definition.init_param import *

class Test_01_IPv6_DHCP_2472_tc_1(Test):
    uuid = "SOSAIOT-TC-56546"
    description= show_testcase_info(Parameter.TESTPLAN, '1714066', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714066')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_option_object(self):
        logger.info('add option object...')
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test1",
                                "number": 22,
                                "value": [
                                    {
                                        "ip": "2004::4"
                                    }
                                ],
                                "array": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        Assertion.assert_equal(rc, True, "ERR: add option object failed")

    def test_02_verify_and_delete_option_object(self):
        logger.info('verify and delete option object...')
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test1')
        logger.info(output)
        rc = dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test1')
        Assertion.assert_equal(rc, True, "ERR: verify and delete option object failed")


class Test_02_IPv6_DHCP_2472_tc_2(Test):
    uuid = "SOSAIOT-TC-56551"
    description= show_testcase_info(Parameter.TESTPLAN, '1714077', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714077')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test2",
                                "number": 12,
                                "value": [
                                    {
                                        "ip": "2003::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test2')
        name = 'test'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
        except:
            logger.info('can\'t get dhcp server option object...')
        logger.info(name)
        if name == 'test2':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_02_edit_and_verify_option_object(self):
        logger.info('edit option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test_2",
                                "number": 22,
                                "value": [
                                    {
                                        "ip": "2005::4"
                                    }
                                ],

                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.edit_dhcp_server_option_object(version = 6, name = 'test2', **dhcp_option)
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test_2')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test_2' and ip == '2005::4':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_03_delete_option_object(self):
        logger.info('delete option object...')
        rc = dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test_2')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test_2', str(output), re.I|re.M):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: delete option object failed")


class Test_03_IPv6_DHCP_2472_tc_3(Test):
    uuid = "SOSAIOT-TC-56552"
    description= show_testcase_info(Parameter.TESTPLAN, '1714080', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714080')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test3",
                                "number": 12,
                                "value": [
                                    {
                                        "ip": "2003::3"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test3')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test3' and ip == '2003::3':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_03_delete_option_object(self):
        logger.info('delete option object...')
        rc = dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test3')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test3', str(output), re.I|re.M):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: delete option object failed")


class Test_04_IPv6_DHCP_2472_tc_4(Test):
    uuid = "SOSAIOT-TC-56553"
    description= show_testcase_info(Parameter.TESTPLAN, '1714081', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714081')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option1 = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test4",
                                "number": 12,
                                "value": [
                                    {
                                        "ip": "2005::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        dhcp_option2 = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test5",
                                "number": 12,
                                "value": [
                                    {
                                        "ip": "2006::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        dhcp_option3 = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test6",
                                "number": 12,
                                "value": [
                                    {
                                        "ip": "2005::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option1)
        rc &= dhcpObj.add_dhcp_server_option_object(**dhcp_option2)
        rc &= dhcpObj.add_dhcp_server_option_object(**dhcp_option3)
       
        output1 = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test4')
        output2 = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test5')
        output3 = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test6')
        name1 = 'test1'
        name2 = 'test2'
        name3 = 'test3'
        ip1 = '2000::1'
        ip2 = '2000::2'
        ip3 = '2000::3'
        try:
            name1 = output1['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip1 = output1['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
            
            name2 = output2['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip2 = output2['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        
            name3 = output3['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip3 = output3['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        if name1 == 'test4' and name2 == 'test5' and name3 == 'test6' and \
            ip1 == '2005::4' and ip2 == '2006::4' and ip3 == '2005::4':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_02_delete_all_option_object(self):
        logger.info('delete all option object...')
        option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test4"
                            },
                            {
                                "name": "test5"
                            },
                            {
                                "name": "test6"
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.delete_all_dhcp_server_option_object(version =6, **option)
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test4', str(output), re.I|re.M) and not re.search(r'test5', str(output), re.I|re.M) \
            and not re.search(r'test6', str(output), re.I|re.M):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: delete all option object failed")


class Test_05_IPv6_DHCP_2472_tc_10(Test):
    uuid = "SOSAIOT-TC-56547"
    description= show_testcase_info(Parameter.TESTPLAN, '1714067', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714067')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test10",
                                "number": 22,
                                "value": [
                                    {
                                        "ip": "2004::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test10')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test10' and ip == '2004::4':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_02_add_valid_dynamic_scopes(self):
        logger.info('add valid dynamic scopes...')
        dynamic_option = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "test",
                                "range": {
                                    "from": "2001::5",
                                    "to": "2001::15"
                                },
                                "enable": True,
                                "prefix": "2001::",
                                "lifetime": {
                                    "valid": 2160,
                                    "preferred": 1440
                                },
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "generic_option": {
                                    "object": "test10"
                                },
                                "always_send_option": True
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**dynamic_option)
        Assertion.assert_equal(rc, True, "ERR: add valid dynamic scopes failed")

    def test_03_delete_and_verify_option_object(self):
        logger.info('delete option object...')
        flag = False
        output1 = dhcpObj.delete_dhcp_server_option_object_msg(version =6, name = 'test10')
        logger.info('delete:{}'.format(output1))
        output2 = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output2)
        if re.search(r'DHCPv6 Option Object/Group in use by DHCPv6 Server', str(output1), re.I|re.M) and \
            re.search(r'test10', str(output2), re.I|re.M) :
            flag =True
        Assertion.assert_equal(flag, True, "ERR: delete and verify option object failed")

    def test_04_delete_dynamic_scope_and_option_object(self):
        logger.info('delete dynamic scope and option object...')
        rc = dhcpObj.del_dhcp_server_scope_dynamic(version =6, name = 'test')
        rc &= dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test10')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test10', str(output), re.I|re.M) :
            flag =True
        Assertion.assert_equal(rc&flag, True, "ERR: delete dynamic scope and option object failed")


class Test_06_IPv6_DHCP_2472_tc_11(Test):
    uuid = "SOSAIOT-TC-56548"
    description= show_testcase_info(Parameter.TESTPLAN, '1714068', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714068')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test11",
                                "number": 22,
                                "value": [
                                    {
                                        "ip": "2004::4"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test11')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test11' and ip == '2004::4':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_02_add_valid_dynamic_scopes(self):
        logger.info('add valid dynamic scopes...')
        dynamic_option = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "test_x1",
                                "range": {
                                    "from": "2001::5",
                                    "to": "2001::15"
                                },
                                "enable": True,
                                "prefix": "2001::",
                                "lifetime": {
                                    "valid": 2160,
                                    "preferred": 1440
                                },
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "generic_option": {
                                    "object": "test11"
                                },
                                "always_send_option": True
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**dynamic_option)
        Assertion.assert_equal(rc, True, "ERR: add valid dynamic scopes failed")


    def test_03_dhcp_client_and_verify(self):
        logger.info('dhcp client and verify')
        flag = False
        try:
            local_host.send_command('dhclient -6 -nw eth1')
            sleep(30)
        except Exception as e:
            logger.info(e)
            return
        finally:
            local_host.send_command('pkill dhclient ')

        output = local_host.send_command('ifconfig eth1')
        logger.info(output)
        if re.search(r".*inet6\s+2001\W+\d+.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:dhcp client and verify failed")

    def test_05_delete_dynamic_scopes_and_option_object(self):
        logger.info('delete option object...')
        rc = dhcpObj.del_dhcp_server_scope_dynamic(version =6, name = 'test_x1')
        rc &= dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test11')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test11', str(output), re.I|re.M) :
            flag =True
        Assertion.assert_equal(rc&flag, True, "ERR: delete dynamic scope and option object failed")


class Test_07_IPv6_DHCP_2472_tc_14(Test):
    uuid = "SOSAIOT-TC-56549"
    description= show_testcase_info(Parameter.TESTPLAN, '1714071', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714071')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test14",
                                "number": 23,
                                "value": [
                                    {
                                        "ip": "2005::201"
                                    }
                                ],
                                "array": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option)
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test14')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test14' and ip == '2005::201':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")

    def test_02_export_prefs(self):
        logger.info('export prefs...')
        flag = False
        local_host.send_command('rm -rf /tmp/test.exp')
        rc = settingObj.export_setting_exp()
        output = local_host.send_command('ls -l /tmp')
        if re.search(r".*test\.exp.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: export prefs failed")

    def test_03_reboot_fw_with_default_factory(self):
        logger.info('reboot fw with default factory...')
        rc = settingObj.boot_fw(mode = 2)
        Assertion.assert_equal(rc, True, "ERR: reboot fw with default factory failed")

    def test_04_import_prefs(self):
        logger.info('import prefs...')
        rc = settingObj.import_setting_exp(filepath = '/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: import prefs failed")

    def test_05_verify_option_object(self):
        logger.info('verify option object...')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test14')
        name = 'test'
        ip = '2000::1'
        try:
            name = output['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip = output['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name)
        logger.info(ip)
        if name == 'test14' and ip == '2005::201':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify option object failed")

    def test_06_delete_option_object(self):
        logger.info('delete option object...')
        rc = dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test14')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test14', str(output), re.I|re.M) :
            flag =True
        Assertion.assert_equal(flag, True, "ERR: delete option object failed")


class Test_08_IPv6_DHCP_2472_tc_16(Test):
    uuid = "SOSAIOT-TC-56550"
    description= show_testcase_info(Parameter.TESTPLAN, '1714073', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1714073')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_and_verify_option_object(self):
        logger.info('add option object...')
        flag = False
        dhcp_option1 = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test16_1",
                                "number": 22,
                                "value": [
                                    {
                                        "ip": "2003::201"
                                    }
                                ],
                                "array": False
                            }
                        ]
                    }
                }
            }
        }
        dhcp_option2 = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "object": [
                            {
                                "name": "test16_2",
                                "number": 23,
                                "value": [
                                    {
                                        "ip": "2004::201"
                                    }
                                ],
                                "array": False
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_object(**dhcp_option1)
        rc &= dhcpObj.add_dhcp_server_option_object(**dhcp_option2)
        output1 = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test16_1')
        output2 = dhcpObj.get_dhcp_server_option_object(version = 6, name = 'test16_2')
        name1 = 'test1'
        name2 = 'test2'
        ip1 = '2000::1'
        ip2 = '2000::2'
        try:
            name1 = output1['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip1 = output1['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
      
            name2 = output2['dhcp_server']['ipv6']['option']['object'][0]['name']
            ip2 = output2['dhcp_server']['ipv6']['option']['object'][0]['value'][0]['ip']
        except:
            logger.info('can\'t get dhcp server option...')
        logger.info(name1)
        logger.info(ip1) 
        logger.info(name2)
        logger.info(ip2)
        if name1 == 'test16_1' and name2 == 'test16_2' and \
            ip1 == '2003::201' and ip2 == '2004::201':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add option object failed")


    def test_02_add_option_groups(self):
        logger.info('add option groups...')
        group_option = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "group": [
                            {
                                "name": "group",
                                "option": {
                                    "object": [
                                        {
                                            "name": "test16_1"
                                        },
                                        {
                                            "name": "test16_2"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_option_group(**group_option)
        Assertion.assert_equal(rc, True, "ERR: add option group failed")


    def test_03_add_valid_dynamic_scopes(self):
        logger.info('add valid dynamic scopes...')
        dynamic_option = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "test16",
                                "range": {
                                    "from": "2001::5",
                                    "to": "2001::15"
                                },
                                "enable": True,
                                "prefix": "2001::",
                                "lifetime": {
                                    "valid": 2160,
                                    "preferred": 1440
                                },
                                "comment": "",
                                "domain_name": "",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                },
                                "generic_option": {
                                    "group": "group"
                                },
                                "always_send_option": True
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcpObj.add_dhcp_server_scope_dynamic(**dynamic_option)
        Assertion.assert_equal(rc, True, "ERR: add valid dynamic scopes failed")

    def test_04_dhcp_client_and_verify(self):
        logger.info('dhcp client and verify')
        flag = False
        try:
            local_host.send_command('dhclient -6 -nw eth1')
            sleep(30)
        except Exception as e:
            logger.info(e)
            return
        finally:
            local_host.send_command('pkill dhclient ')
        output = local_host.send_command('ifconfig eth1')
        logger.info(output)
        if re.search(r".*inet6\s+2001\W+\d+.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:dhcp client and verify failed")

    def test_05_delete_option_object(self):
        logger.info('delete option object...')
        output = dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test16_1')
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: delete option object failed")

    def test_06_dhcp_client_and_verify(self):
        logger.info('dhcp client and verify')
        flag = False
        try:
            local_host.send_command('dhclient -6 -nw eth1')
            sleep(30)
        except Exception as e:
            logger.info(e)
            return
        finally:
            local_host.send_command('pkill dhclient ')
        output = local_host.send_command('ifconfig eth1')
        logger.info(output)
        if re.search(r".*inet6\s+2001\W+\d+.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:dhcp client and verify failed")

    def test_07_delete_dynamic_scopes_and_option_object(self):
        logger.info('delete option object...')
        rc = dhcpObj.del_dhcp_server_scope_dynamic(version =6, name = 'test16')
        rc &= dhcpObj.delete_dhcp_server_option_group(version =6, name = 'group')
        rc &= dhcpObj.delete_dhcp_server_option_object(version =6, name = 'test16_2')
        flag = False
        output = dhcpObj.get_dhcp_server_option_object(version = 6)
        logger.info(output)
        if not re.search(r'test16_2', str(output), re.I|re.M) :
            flag =True
        Assertion.assert_equal(rc&flag, True, "ERR: delete dynamic scope and option object failed")
