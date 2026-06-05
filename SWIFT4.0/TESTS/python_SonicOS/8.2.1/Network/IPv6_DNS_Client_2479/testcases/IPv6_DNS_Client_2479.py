from definition.init_param import *


class Test_01_IPv6_DNS_Client_2479_tc_2(Test):
    uuid = "SOSAIOT-TC-51390"
    description= show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_DNS_Server1_can_inherit_ipv6_dns_setting_from_primary_wan_interface(self):
        logger.info('verify DNS server1 can inherit ipv6 dns setting from primary wan interface...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+1:\s+{}".format(WAN_host), str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify DNS server1 can inherit \
                                ipv6 dns setting from primary wan interface failed")


class Test_02_IPv6_DNS_Client_2479_tc_5(Test):
    uuid = "SOSAIOT-TC-51391"
    description= show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']
    jira = 'GEN7-37458'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            "dns": {
                "primary": WAN_host,
                "secondary": bogus_dns1,
                "tertiary": "::"
            },
            'adv_pref': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x1_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X1 ipv6 Failed!")
 
    def test_02_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2_opt_v4 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip':Parameter.X2_IP,
        }
        rc = interface_obj.config_interface(**x2_opt_v4)
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_IPv6,
            'adv_pref': True,
        }
        rc &= interface_ipv6_obj.config_interface_ipv6( **x2_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X2 ipv6 Failed!")
 
    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+1:\s+{}".format(WAN_host), str(output), re.S|re.I|re.M) and \
            re.search(r"IPv6\s+DNS\s+Server\s+2:\s+{}".format(bogus_dns1), str(output), re.S|re.I|re.M) and \
            re.search(r"IPv6\s+DNS\s+Server\s+3:\s+::", str(output), re.S|re.I|re.M)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")

    def test_04_switch_x2_to_primary_WAN_interface(self):
        logger.info('switch x2 to primary WAN interface...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group IPv6",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: switch x2 to primary WAN interface failed")

    def test_05_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+1:\s+{}".format(WAN_host), str(output), re.S|re.I|re.M) and \
            re.search(r"IPv6\s+DNS\s+Server\s+2:\s+{}".format(bogus_dns1), str(output), re.S|re.I|re.M) and \
            re.search(r"IPv6\s+DNS\s+Server\s+3:\s+::", str(output), re.S|re.I|re.M)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")

    def test_06_switch_x1_to_primary_WAN_interface(self):
        logger.info('switch x1 to primary WAN interface...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group IPv6",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: switch x1 to primary WAN interface failed")


class Test_03_IPv6_DNS_Client_2479_tc_7(Test):
    uuid = "SOSAIOT-TC-51392"
    description= show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            "dns": {
                "primary": WAN_host,
                "secondary": "::",
                "tertiary": "::"
            },
            'adv_pref': True,
            'router_adv': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x1_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X1 ipv6 Failed!")
 
    def test_02_specify_ipv6_dns_server1_manually(self):
        logger.info('specify ipv6 dns server1 manually...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": bogus_dns1,
                            "secondary": "::",
                            "tertiary": "::"
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")
 
    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+1:\s+{}".format(bogus_dns1), str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")


class Test_04_IPv6_DNS_Client_2479_tc_10(Test):
    uuid = "SOSAIOT-TC-51388"
    description= show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server1_manually(self):
        logger.info('specify ipv6 dns server1 manually...')
        flag = False
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": invalid_dns6,
                            "secondary": "::",
                            "tertiary": "::"
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        output = dnsObj.set_dns_msg( **dns_opt)
        logger.info(output)
        if re.search(r"DNS server IPv6 address 1: Using this IPv6 address as DNS server is invalid", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: specify ipv6 dns server1 manually Failed!")
 
    def test_02_specify_ipv6_dns_server2_manually(self):
        logger.info('specify ipv6 dns server2 manually...')
        flag = False
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": invalid_dns6,
                            "tertiary": "::"
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        output = dnsObj.set_dns_msg( **dns_opt)
        logger.info(output)
        if re.search(r"DNS server IPv6 address 2: Using this IPv6 address as DNS server is invalid", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: specify ipv6 dns server2 manually Failed!")
 
    def test_03_specify_ipv6_dns_server3_manually(self):
        logger.info('specify ipv6 dns server3 manually...')
        flag = False
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": "::",
                            "tertiary": invalid_dns6
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        output = dnsObj.set_dns_msg( **dns_opt)
        logger.info(output)
        if re.search(r"DNS server IPv6 address 3: Using this IPv6 address as DNS server is invalid", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: specify ipv6 dns server3 manually Failed!")

    def test_04_specify_ipv6_dns_server1_manually_jira(self):
        logger.info('specify ipv6 dns server1 manually jira...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": jira_dns6,
                            "secondary": "::",
                            "tertiary": "::"
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    def test_05_specify_ipv6_dns_server2_manually_jira(self):
        logger.info('specify ipv6 dns server2 manually jira...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": jira_dns6,
                            "tertiary": "::"
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server2 manually Failed!")

    def test_06_specify_ipv6_dns_server3_manually_jira(self):
        logger.info('specify ipv6 dns server3 manually jira...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": "::",
                            "tertiary": jira_dns6
                        },
                        "preferred": False
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server3 manually Failed!")

class Test_05_IPv6_DNS_Client_2479_tc_11(Test):
    uuid = "SOSAIOT-TC-51389"
    description= show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server1_manually(self):
        logger.info('specify ipv6 dns server1 manually...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": WAN_host,
                            "secondary": "::",
                            "tertiary": "::"
                        },
                        "preferred": True
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")
 
    @repeat_method(3)
    def test_02_verify_domain_name_resolved_to_correct_ipv6_address(self):
        logger.info('verify domain name is resolved to correct ipv6 address...')
        flag = False
        sleep(10)
        dns_lookup = {
            'version': 'ipv6',
            'type': 'system',
            'domain_name': domain_url,
            'ipv6-dns1': WAN_host,
        }
        systemObj.diag_dns_lookup_name_by_api(**dns_lookup)
        output =systemObj.get_name_lookup_Result()
        logger.info(output)
        resolve_ip = '2000::1'
        try:
            resolve_ip = output['data']['resolvedAddrs']
        except:
            logger.info('can\'t get resolved addrs')
        logger.info(resolve_ip)
        if resolve_ip == resolveIP +';':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify domain name is resolved to correct ipv6 address Failed!")

    def test_03_specify_ipv6_dns_server2_manually(self):
        logger.info('specify ipv6 dns server2 manually...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": WAN_host,
                            "tertiary": "::"
                        },
                        "preferred": True
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    @repeat_method(3)
    def test_04_verify_domain_name_resolved_to_correct_ipv6_address(self):
        logger.info('verify domain name is resolved to correct ipv6 address...')
        flag = False
        sleep(10)
        dns_lookup = {
            'version': 'ipv6',
            'type': 'system',
            'domain_name': domain_url,
            'ipv6-dns2': WAN_host,
        }
        systemObj.diag_dns_lookup_name_by_api(**dns_lookup)
        output =systemObj.get_name_lookup_Result()
        logger.info(output)
        resolve_ip = '2000::1'
        try:
            resolve_ip = output['data']['resolvedAddrs']
        except:
            logger.info('can\'t get resolved addrs')
        logger.info(resolve_ip)
        if resolve_ip == resolveIP +';':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify domain name is resolved to correct ipv6 address Failed!")

    def test_05_specify_ipv6_dns_server3_manually(self):
        logger.info('specify ipv6 dns server3 manually...')
        dns_opt = {
            "dns": {
                "server": {
                    "inherit": True,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": "::",
                            "secondary": "::",
                            "tertiary": WAN_host,
                        },
                        "preferred": True
                    }
                },
                "rebinding": {
                    "enable": False,
                    "action": "log-attack-only",
                    "allowed_domains": {}
                },
                "fqdn_binding": False,
                "split_servers": True,
                "fqdn_over_tcp_dns": False
            }
        }
        rc = dnsObj.set_dns( **dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    @repeat_method(3)
    def test_06_verify_domain_name_resolved_to_correct_ipv6_address(self):
        logger.info('verify domain name is resolved to correct ipv6 address...')
        flag = False
        sleep(10)
        dns_lookup = {
            'version': 'ipv6',
            'type': 'system',
            'domain_name': domain_url,
            'ipv6-dns3': WAN_host,
        }
        systemObj.diag_dns_lookup_name_by_api(**dns_lookup)
        output =systemObj.get_name_lookup_Result()
        logger.info(output)
        resolve_ip = '2000::1'
        try:
            resolve_ip = output['data']['resolvedAddrs']
        except:
            logger.info('can\'t get resolved addrs')
        logger.info(resolve_ip)
        if resolve_ip == resolveIP +';':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify domain name is resolved to correct ipv6 address Failed!")