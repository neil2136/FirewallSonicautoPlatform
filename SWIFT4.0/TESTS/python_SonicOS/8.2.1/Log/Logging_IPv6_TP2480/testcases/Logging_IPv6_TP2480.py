from definition.init_param import *


class Test_01_Logging_IPv6_TP2480_tc_11(Test):
    uuid = "SOSAIOT-TC-55540"
    description= show_testcase_info(Parameter.TESTPLAN, '1529951', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529951')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ping_dut_ipv6_lan_and_verify_log(self):
        logger.info('ping dut ipv6 lan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 {} -s 65507 -i 0.01 -c 100'.format(Parameter.X0_IPv6)
        local_host.send_command(cmd)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Ping of death dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping dut ipv6 lan and verify log failed")


class Test_02_Logging_IPv6_TP2480_tc_12(Test):
    uuid = "SOSAIOT-TC-55541"
    description= show_testcase_info(Parameter.TESTPLAN, '1529952', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529952')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_login_and_check_authentication_access_log(self):
        logger.info('login and check authentication access log...')
        flag = False
        systemlogObj.clear_log()
        fw.api_login()
        sleep(5)
        fw.api_logout()
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Administrator login allowed', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: login and check authentication access log failed")


class Test_03_Logging_IPv6_TP2480_tc_17(Test):
    uuid = "SOSAIOT-TC-55542"
    description= show_testcase_info(Parameter.TESTPLAN, '1529955', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529955')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_to_wan_deny_icmpv6_access_rule(self):
        logger.info('add lan to wan deny icmpv6 access rule...')
        opt = {
            "access_rules": [
                {
                    "ipv6": {
                        "name": "My Rule",
                        "comment": "",
                        "action": "deny",
                        "priority": {
                            "auto": True
                        },
                        "enable": True,
                        "from": "LAN",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "to": "WAN",
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "service": {
                            "group": "ICMPv6"
                        },
                      "logging": True,
                    }
                }
            ]
        }
        rc = accessRulesIpv6Obj.add_accessrule_ipv6(**opt)
        Assertion.assert_equal(rc, True, "ERR: add lan to wan deny icmpv6 access rule failed")
    
    @repeat_method(3)
    def test_02_add_ipv6_route_on_pc1(self):
        logger.info('add ipv6 route on pc1...')
        flag = False
        cmd = 'route -A inet6 add {}/64 gw {} dev eth1'.format(Parameter.X1_IPv6, Parameter.X0_IPv6)
        local_host.send_command(cmd)
        output = local_host.send_command('route -6n')
        logger.info(output)
        if re.search(r'2001::/64\s+2000::168', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: login and check authentication access log failed")

    def test_03_from_lan_ping_wan_and_verify_log(self):
        logger.info('from lan ping wan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 {} -c 5 -I eth1'.format(Parameter.X1_IPv6)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'ICMPv6 packet from LAN dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan ping wan and verify log failed")


class Test_04_Logging_IPv6_TP2480_tc_18(Test):
    uuid = "SOSAIOT-TC-55543"
    description= show_testcase_info(Parameter.TESTPLAN, '1529956', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529956')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_to_wan_https_deny_rule(self):
        logger.info('add lan to wan https deny access rule...')
        opt = {
            "access_rules": [
                {
                    "ipv6": {
                        "name": "My Rule",
                        "comment": "",
                        "action": "deny",
                        "priority": {
                            "auto": True
                        },
                        "enable": True,
                        "from": "LAN",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "to": "WAN",
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "service": {
                            "name": "HTTP"
                        },
                      "logging": True,
                    }
                }
            ]
        }
        rc = accessRulesIpv6Obj.add_accessrule_ipv6(**opt)
        Assertion.assert_equal(rc, True, "ERR: add lan to wan https deny access rule failed")

    def test_02_enable_web_access_request_log(self):
        logger.info('enable web access request log...')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 524,
                        "name": "Web Request Drop",
                        "category": "Network",
                        "group": "Network Access",
                        "priority_level": "notice",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable web access request log failed")

    def test_03_from_lan_http_wan_and_verify_log(self):
        logger.info('from lan http wan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'curl -6 http://[{}]'.format(Parameter.X1_IPv6)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Web access Request dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan http wan and verify log failed")


class Test_05_Logging_IPv6_TP2480_tc_20(Test):
    uuid = "SOSAIOT-TC-55545"
    description= show_testcase_info(Parameter.TESTPLAN, '1529958', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529958')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_DAO_log(self):
        logger.info('enable dynamic address object log event...')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 911,
                        "name": "Added Host Entry",
                        "category": "Network",
                        "group": "Dynamic Address Objects",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    },
                    {
                        "id": 912,
                        "name": "Removed Host Entry",
                        "category": "Network",
                        "group": "Dynamic Address Objects",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    },
                    {
                        "id": 880,
                        "name": "Failed to Resolve Dynamic Address Object",
                        "category": "Network",
                        "group": "Dynamic Address Objects",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable web access request log failed")

    def test_02_add_dynamic_address_object_and_verify_log(self):
        logger.info('add dynamic address object and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "object_type":"FQDN",
            "name":"test",
            "zone":"LAN",
            "value":  "www.baidu.com"
        }
        addressObj.config_addressobject(**opt)
        sleep(10)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Added host entry to dynamic address object', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add dynamic address object and verify log failed")

    def test_03_delete_dynamic_address_object_and_verify_log(self):
        logger.info('add dynamic address object and verify log...')
        flag = False
        systemlogObj.clear_log()
        addressObj.del_ao_by_name(name='test',version='fqdn')
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Removed host entry from dynamic address object', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: delete dynamic address object and verify log failed")


class Test_06_Logging_IPv6_TP2480_tc_27(Test):
    uuid = "SOSAIOT-TC-55546"
    description= show_testcase_info(Parameter.TESTPLAN, '1529963', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529963')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_nat_policy_log_event(self):
        logger.info('enable nat policy log event...')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 1313,
                        "name": "NAT Policy Add",
                        "category": "Network",
                        "group": "NAT Policy",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {
                            "redundancy_interval": 60
                        },
                        "log_digest": False,
                        "alert_email": {}
                    },
                    {
                        "id": 1314,
                        "name": "NAT Policy Modify",
                        "category": "Network",
                        "group": "NAT Policy",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {
                            "redundancy_interval": 60
                        },
                        "log_digest": False,
                        "alert_email": {}
                    },
                    {
                        "id": 1315,
                        "name": "NAT Policy Delete",
                        "category": "Network",
                        "group": "NAT Policy",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {
                            "redundancy_interval": 60
                        },
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable web access request log failed")

    def test_02_add_NAT_policy_and_verify_log(self):
        logger.info('add NAT policy and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "nat_policies": [
                {
                    "ipv6": {
                        "name": "My Rule",
                        "reflexive": False,
                        "source_port_remap": True,
                        "inbound": "any",
                        "outbound": "any",
                        "comment": "",
                        "enable": True,
                        "translated_destination": {
                            "original": True
                        },
                        "translated_source": {
                            "group": "WAN IPv6 Subnets"
                        },
                        "translated_service": {
                            "original": True
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "any": True
                        },
                        "service": {
                            "any": True
                        },
                        "priority": {
                            "auto": True
                        },
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        }
                    }
                }
            ]
        }
        natObj.add_nat_policy(**opt)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'NAT policy added', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add NAT policy and verify log failed")

    def test_03_modify_NAT_policy_and_verify_log(self):
        logger.info('modify NAT policy and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "nat_policies": [
                {
                    "ipv6": {
                        "uuid": "00000000-0000-0002-0800-2cb8ed6d7fe0",
                        "name": "My Rule",
                        "source_port_remap": True,
                        "inbound": "any",
                        "outbound": "any",
                        "comment": "",
                        "enable": True,
                        "translated_destination": {
                            "original": True
                        },
                        "translated_source": {
                            "group": "X1 IPv6 Addresses"
                        },
                        "translated_service": {
                            "original": True
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "any": True
                        },
                        "service": {
                            "any": True
                        },
                        "priority": {
                            "auto": True
                        },
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        }
                    }
                }
            ]
        }
        natObj.edit_nat_policy_by_name(name='My Rule', version='v6', **opt)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'NAT policy modified', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: modify NAT policy and verify log failed")
    
    def test_04_delete_NAT_policy_and_verify_log(self):
        logger.info('delete NAT policy and verify log...')
        flag = False
        systemlogObj.clear_log()
        natObj.del_nat_policy(name='My Rule', version='v6')
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'NAT policy deleted', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: delete NAT policy and verify log failed")


class Test_07_Logging_IPv6_TP2480_tc_29(Test):
    uuid = "SOSAIOT-TC-55547"
    description= show_testcase_info(Parameter.TESTPLAN, '1529965', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529965')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_ipv6_interface_and_verify_log(self):
        logger.info('change ipv6 interface and verify log...')
        flag = False
        systemlogObj.clear_log()
        x1 = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': IPv6_test,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        interface_ipv6_obj.config_interface_ipv6(**x1)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Configuration succeeded:\s+\'IPv6 Interface Static IP', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: change ipv6 interface and verify log failed")


class Test_08_Logging_IPv6_TP2480_tc_3(Test):
    uuid = "SOSAIOT-TC-55548"
    description= show_testcase_info(Parameter.TESTPLAN, '1529966', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529966')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_from_lan_ping6_lan_ipv6_and_verify_log(self):
        logger.info('from lan ping6 lan ipv6 interface and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 {} -s 65507 -i 0.01 -c 100'.format(Parameter.X0_IPv6)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Ping of death dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan ping6 lan ipv6 interface and verify log failed")


class Test_09_Logging_IPv6_TP2480_tc_30(Test):
    uuid = "SOSAIOT-TC-55549"
    description= show_testcase_info(Parameter.TESTPLAN, '1529967', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529967')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_network_monitor_and_verify_log(self):
        logger.info('add network monitor and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "network_monitors": [
                {
                    "policy": {
                        "ipv6": {
                            "name": "test_tc30",
                            "probe": {
                                "target": {
                                    "name": "X1 IPv6 Link-Local Address"
                                },
                                "type": {
                                    "ping": "non-explicit"
                                },
                                "interval": 5
                            },
                            "reply_timeout": 1,
                            "interval": {
                                "missed": 3,
                                "successful": 3
                            },
                            "must_respond": False,
                            "comment": ""
                        }
                    }
                }
            ]
        }
        networkMonitorObj.add_network_monitor(**opt)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Network Monitor Policy test_tc30 Added', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add network monitor and verify log failed")

    def test_02_modify_network_monitor_and_verify_log(self):
        logger.info('modify network monitor and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "network_monitors": [
                {
                    "policy": {
                        "ipv6": {
                            "name": "test_tc30",
                            "probe": {
                                "target": {
                                    "name": "X0 IPv6 Link-Local Address"
                                },
                                "type": {
                                    "ping": "non-explicit"
                                },
                                "interval": 5
                            },
                            "reply_timeout": 1,
                            "interval": {
                                "missed": 3,
                                "successful": 3
                            },
                            "must_respond": False,
                            "comment": ""
                        }
                    }
                }
            ]
        }
        networkMonitorObj.edit_network_monitor(**opt)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Network Monitor Policy test_tc30 Modified', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: modify network monitor and verify log failed")

    def test_03_delete_network_monitor_and_verify_log(self):
        logger.info('delete network monitor and verify log...')
        flag = False
        systemlogObj.clear_log()
        networkMonitorObj.del_network_monitor(name='test_tc30', version=6)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Network Monitor Policy test_tc30 Deleted', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: delete network monitor and verify log failed")


class Test_10_Logging_IPv6_TP2480_tc_35(Test):
    uuid = "SOSAIOT-TC-55550"
    description= show_testcase_info(Parameter.TESTPLAN, '1529971', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529971')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ipv6_login_and_verify_log(self):
        logger.info('ipv6 login and verify log...')
        flag = False
        systemlogObj.clear_log()
        fw_ipv6.api_login()
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'admin via SonicOS API from {}'.format(Parameter.PC1_ETH1_v6), str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ipv6 login and verify log failed")


class Test_11_Logging_IPv6_TP2480_tc_4(Test):
    uuid = "SOSAIOT-TC-55553"
    description= show_testcase_info(Parameter.TESTPLAN, '1529975', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529975')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_icmpv6_log_event(self):
        logger.info('enable icmpv6 log event...')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 1255,
                        "name": "LAN ICMPv6 Allow",
                        "category": "Network",
                        "group": "ICMP",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    },
                    {
                        "id": 1431,
                        "name": "ICMPv6 Packets Received",
                        "category": "Network",
                        "group": "ICMP",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable icmpv6 log failed")

    def test_02_from_lan_ping6_lan_and_verify_log(self):
        logger.info('from lan ping6 lan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 -c 5 {}'.format(Parameter.X0_IPv6)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'ICMPv6 packet received', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan ping6 lan and verify log failed")


class Test_12_Logging_IPv6_TP2480_tc_5(Test):
    uuid = "SOSAIOT-TC-55557"
    description= show_testcase_info(Parameter.TESTPLAN, '1529980', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529980')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_from_lan_ping6_lan_and_verify_log(self):
        logger.info('from lan ping6 lan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 -c 5 {}'.format(Parameter.X0_IPv6)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'ICMPv6 packet from LAN allowed', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan ping6 lan and verify log failed")


class Test_13_Logging_IPv6_TP2480_tc_6(Test):
    uuid = "SOSAIOT-TC-55558"
    description= show_testcase_info(Parameter.TESTPLAN, '1529981', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529981')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_from_lan_ping6_wan_and_verify_log(self):
        logger.info('from lan ping6 wan and verify log...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'ping6 -c 5 {}'.format(IPv6_test)
        local_host.send_command(cmd)
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'ICMPv6 packet from LAN dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from lan ping6 wan and verify log failed")


class Test_14_Logging_IPv6_TP2480_tc_7(Test):
    uuid = "SOSAIOT-TC-55559"
    description= show_testcase_info(Parameter.TESTPLAN, '1529982', description=True)['title']
    jira = 'GEN8-5027'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529982')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ntp_log_event(self):
        logger.info('enable ntp log event...')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 1230,
                        "name": "NTP Update Failure",
                        "category": "System",
                        "group": "Time",
                        "priority_level": "notice",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {
                            "redundancy_interval": 60
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": True,
                        "alert_email": {}
                    },
                    {
                        "id": 1231,
                        "name": "NTP Update Successful",
                        "category": "System",
                        "group": "Time",
                        "priority_level": "notice",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {
                            "redundancy_interval": 60
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": True,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable ntp log event failed")

    def test_02_add_invalid_ntp_server(self):
        logger.info('add invalid ntp server...')
        opt = {
            "name": INVALID_NTP_SERVER,
            "no_auth": True
        }
        rc = timeObj.add_ntp_server(**opt)
        Assertion.assert_equal(rc, True, "ERR: add invalid ntp server failed")

    def test_03_config_ntp_setting_and_verify_log(self):
        logger.info('config ntp setting and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "time": {
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": True,
                "use_ntp": True,
                "ntp_update_interval": 5,
                "time_zone": "pacific-time"
            }
        }
        timeObj.set_time(**opt)
        sleep(300)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Response from NTP Server is either incomplete or invalid', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config ntp setting and verify log failed")


class Test_15_Logging_IPv6_TP2480_tc_8(Test):
    uuid = "SOSAIOT-TC-55560"
    description= show_testcase_info(Parameter.TESTPLAN, '1529983', description=True)['title']
    jira = 'GEN8-5027'


    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529983')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_invalid_ntp_server(self):
        logger.info('add invalid ntp server...')
        rc = timeObj.delete_ntp_server(name = INVALID_NTP_SERVER)
        Assertion.assert_equal(rc, True, "ERR: delete invalid ntp server failed")

    def test_02_add_valid_ntp_server(self):
        logger.info('add valid ntp server...')
        opt = {
            "name": VALID_NTP_SERVER,
            "no_auth": True
        }
        rc = timeObj.add_ntp_server(**opt)
        Assertion.assert_equal(rc, True, "ERR: add valid ntp server failed")

    def test_03_config_ntp_setting_and_verify_log(self):
        logger.info('config ntp setting and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "time": {
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": True,
                "ntp_update_interval": 5,
                "time_zone": "pacific-time"
            }
        }
        timeObj.set_time(**opt)
        sleep(300)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Time update from NTP server was successful', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config ntp setting and verify log failed")


class Test_16_Logging_IPv6_TP2480_tc_9(Test):
    uuid = "SOSAIOT-TC-55561"
    description= show_testcase_info(Parameter.TESTPLAN, '1529984', description=True)['title']
    jira = 'GEN8-5027'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529984')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ntp_sent_log_event(self):
        logger.info('enable ntp sent log event')
        opt = {
            "log": {
                "event": [
                    {
                        "id": 1232,
                        "name": "NTP Request Sent",
                        "category": "System",
                        "group": "Time",
                        "priority_level": "notice",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {
                            "redundancy_interval": 60
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": True,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**opt)
        Assertion.assert_equal(rc, True, "ERR: enable ntp sent log event failed")

    def test_02_config_ntp_setting_and_verify_log(self):
        logger.info('config ntp setting and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            "time": {
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": True,
                "ntp_update_interval": 5,
                "time_zone": "pacific-time"
            }
        }
        timeObj.set_time(**opt)
        sleep(300)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'NTP Request sent', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config ntp setting and verify log failed")


class Test_17_Logging_IPv6_TP2480_tc_2(Test):
    uuid = "SOSAIOT-TC-55544"
    description= show_testcase_info(Parameter.TESTPLAN, '1529957', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529957')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_6to4_interface(self):
        logger.info('add 6to4 interface...')
        opt = {
            'type': '6to4',
            "name": "6to4AutoTun",
            'zone': 'WAN',
            "ip": IP_6to4,
            "bound_to": {
                    "interface": "X1"
                },
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, "ERR: add 6to4 interface failed")

    def test_02_ping_6to4_interface_and_verify_log(self):
        logger.info('ping6 6to4 interface and verify log...')
        flag = False
        cmd = 'route -A inet6 add {}/64 gw {} dev eth1'.format(IP_6to4, Parameter.X0_IPv6)
        logger.info('add route on pc1:{}'.format(cmd))
        local_host.send_command(cmd)
        systemlogObj.clear_log()
        local_host.send_command('ping6 -c 5 {}'.format(IP_6to4))
        sleep(5)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'dst_int_\': \'6to4AutoTun.*ICMPv6 packet from LAN dropped', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping6 6to4 interface and verify log failed")


class Test_18_Logging_IPv6_TP2480_tc_37(Test):
    uuid = "SOSAIOT-TC-55551"
    description= show_testcase_info(Parameter.TESTPLAN, '1529972', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529972')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_on_fw_and_remote(self):
        logger.info('add address object on fw and remote...')
        # DUT object
        remote_l = {
            'name': 'remote_X1',
            'zone': 'WAN',
            'object_type': 'host',
            'value': Parameter.REMOTE_X1_v6,
        }
        #RemoteDUT object
        remote_r = {
            'name': 'remote_X2',
            'zone': 'WAN',
            'object_type': 'host',
            'value': Parameter.X2_IPv6
        }
        rc = LAddrOBJ.config_addressobject(**remote_l)
        rc &=RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, "ERR: add address object on fw and remote failed")

    def test_02_config_vpn_policy(self):
        logger.info('config vpn policy...')
        systemlogObj.clear_log()
        Lvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn_local',
            'enable'            : True,
            'auth_mode'         : 'shared_secret',
            'secret'            : '123456',
            'pri_gate'          : Parameter.REMOTE_X1_v6,
            'sec_gate'          : '0::0',
            'local_ike_type'    : 'ipv6',
            'peer_ike_type'     : 'ipv6',
            'local_ike_id'      : Parameter.X2_IPv6,
            'peer_ike_id'       : Parameter.REMOTE_X1_v6,
            'local_net_type'    : 'name',
            'remote_net_type'   : 'name',
            'local_net_name'    : "X2 IPv6 Primary Static Address",
            'remote_net_name'   : 'remote_X1',
            'ike_exchange'      : 'ikev2',
            'ike_encryption'    : 'triple-des',
            'ipsec_encryption'  : 'triple_des',
            'ike_lifetime'      : '28800',
            'ipsec_lifetime'    : '28800',
            'keep_alive'        : True,
            "bound_to"          : ['interface', 'X2'],
            # 'preempt_interval'  :'120',
            # 'suppress_trigger_packet' :True,
        }
        Rvpn = {
            'type'              : 'site_to_site',
            'name'              : 'vpn_remote',
            'enable'            : True,
            'auth_mode'         : 'shared_secret',
            'secret'            : '123456',
            'pri_gate'          :Parameter.X2_IPv6,
            'sec_gate'          : '0::0',
            'local_ike_type'    : 'ipv6',
            'peer_ike_type'     : 'ipv6',
            'local_ike_id'      : Parameter.REMOTE_X1_v6,
            'peer_ike_id'       : Parameter.X2_IPv6,
            'local_net_type'    : 'name',
            'remote_net_type'   : 'name',
            'local_net_name'    : "X1 IPv6 Primary Static Address",
            'remote_net_name'   : 'remote_X2',
            'ike_exchange'      : 'ikev2',
            'ike_encryption'    : 'triple-des',
            'ipsec_encryption'  : 'triple_des',
            'ike_lifetime'      : '28800',
            'ipsec_lifetime'    : '28800',
            'keep_alive'        : True,
            'bound_to'          : ['interface', 'X1'],
            # 'suppress_trigger_packet': True,

        }

        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_ipv6_vpn_policy(**Lvpn)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_ipv6_vpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_03_verify_ipv6_IKE_log(self):
        logger.info('verify ipv6 IKE log...')
        flag = False
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'IKEv2 Authentication successful', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify ipv6 IKE log failed")


class Test_19_Logging_IPv6_TP2480_tc_38(Test):
    uuid = "SOSAIOT-TC-55552"
    description= show_testcase_info(Parameter.TESTPLAN, '1529973', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529973')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_icmpv6_log_event(self):
        logger.info('disable icmpv6 log event')
        rc = logSettingObj.disable_event(event_id ='1431')
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: disable icmpv6 log event failed")

    def test_02_reenable_ipv6_IKE_and_verify_log(self):
        logger.info('re-enable ipv6 IKE policy and verify log...')
        flag = False
        opt = {
            'enable': False
        }
        Lvpn_obj.config_ipv6_vpn_policy(name='vpn_local', **opt)
        systemlogObj.clear_log()
        opt1 = {
            'enable': True
        }
        Lvpn_obj.config_ipv6_vpn_policy(name='vpn_local', **opt1)
        sleep(10)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'IPsec Tunnel status changed', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify ipv6 IKE log failed")


class Test_20_Logging_IPv6_TP2480_tc_40(Test):
    uuid = "SOSAIOT-TC-55554"
    description= show_testcase_info(Parameter.TESTPLAN, '1529976', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529976')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_reenable_ipv6_IKE_and_verify_log(self):
        logger.info('re-enable ipv6 IKE policy and verify log...')
        flag = False
        systemlogObj.clear_log()
        opt = {
            'enable': False
        }
        Lvpn_obj.config_ipv6_vpn_policy(name='vpn_local', **opt)
        opt1 = {
            'enable': True
        }
        Lvpn_obj.config_ipv6_vpn_policy(name='vpn_local', **opt1)
        sleep(10)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Accept IPsec SA Proposal', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify ipv6 IKE log failed")


class Test_21_Logging_IPv6_TP2480_tc_41(Test):
    uuid = "SOSAIOT-TC-55555"
    description= show_testcase_info(Parameter.TESTPLAN, '1529977', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529977')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_reenable_interface_x1_and_verify_log(self):
        logger.info('re-enable interface x1 and verify log...')
        flag = False
        systemlogObj.clear_log()
        interfaceObj.disable_interface(name= 'X1')
        sleep(30)
        interfaceObj.enable_interface(name= 'X1')
        sleep(30)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'src_ip\':\s\'2001::22.*WLB Resource is now available', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: re-enable interface x1 and verify log failed")


class Test_22_Logging_IPv6_TP2480_tc_43(Test):
    uuid = "SOSAIOT-TC-55556"
    description= show_testcase_info(Parameter.TESTPLAN, '1529979', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529979')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_clear_log_and_verify_log(self):
        logger.info('clear log and verify log...')
        flag = False
        systemlogObj.clear_log()
        sleep(10)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'Configuration succeeded: Clear All Log', str(output), re.M|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: clear log and verify log failed")
