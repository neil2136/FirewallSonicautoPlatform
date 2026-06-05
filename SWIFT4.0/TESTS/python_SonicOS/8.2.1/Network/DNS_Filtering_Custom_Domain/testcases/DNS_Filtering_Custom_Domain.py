from definition.settings import *
from testcases import check_action


class TestDNS_Filtering_Custom_Domain_01(Test):
    uuid = "SOSAIOT-TC-51539"
    description= show_testcase_info(Parameter.TESTPLAN, '1521002', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1521002')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_domain(self):
        add_domain = {
            "dns_security": {
                "dns_filtering": {
                    "custom_domain": [{
                        "domain": domain1,
                        "category": "1. Adult"
                    }]
                }
            }
        }
        rc = dnssec_obj.add_dns_custom_domain(**add_domain)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_custom_domain failed")

    def test_02_verify_custom_domain(self):
        flag = False
        rc = dnssec_obj.show_dns_custom_domain()
        if domain1 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_02_verify_custom_domain failed")


class TestDNS_Filtering_Custom_Domain_02(Test):
    uuid = "SOSAIOT-TC-51551"
    description= show_testcase_info(Parameter.TESTPLAN, '1521015', description=True)['title']
    goto_teardown = True
    jira = 'Gen7-44568'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1521015')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_domain(self):
        add_domain = {
            "dns_security": {
                "dns_filtering": {
                    "custom_domain": [{
                        "domain": domain2,
                        "category": "4. Malware"
                    }]
                }
            }
        }
        rc = dnssec_obj.add_dns_custom_domain(**add_domain)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_custom_domain failed")

    def test_02_create_dns_rule(self):
        add_rule = {
            "dns_policies": [{
                "name": "Test",
                "priority": {
                    "manual": 1
                },
                "enable": True,
                "service": {
                    "name": "DNS (Name Service) UDP"
                },
                "from": "X0",
                "schedule": {
                    "always_on": True
                },
                "action": {
                    "filter_profile": "Default Profile"
                }
            }]
        }
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")
    
    def test_03_set_log_level_to_inform(self):
        rc = log_cata.logging_level(level='inform')
        Assertion.assert_equal(rc, True, "ERR: Set_log_level_to_inform failed")

    def test_04_enable_DNS_Packet_Allowed(self):
        eventid = [1549,1550,1593,1594,1684,1685,1686,1687,1688,1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683]
        for i in eventid:
            log = {
                "log": {
                    "event": [
                        {
                            "id": i,
                            "category": "Network",
                            "group": "DNS Security",
                            "priority_level": "inform",
                            "log_monitor": {
                                "redundancy_interval": 0
                            },
                            "email_alert": {
                                "redundancy_interval": 0
                            },
                            "syslog": {
                                "redundancy_interval": 0
                            },
                            "event_profile": {
                                "syslog_server_profile": 0
                            }
                        }
                    ]
                }
            }
            rc = log_set.edit_event(event_id=str(i), **log)
        Assertion.assert_equal(rc, True, "ERR: Enable_DNS_Packet_Allowed failed")

    def test_05_set_Display_Events_in_Log_Monitor_to_0_seconds(self):
        set_log_monitor = {
            "log": {
                "category": [
                    {
                        "name": "Network",
                        "log_monitor": {
                            "type": "mixed",
                            "redundancy_interval": {}
                        }           
                    }
                ]
            }
        }
        rc = log_cata.edit_log_categories_by_name('Network', **set_log_monitor)
        Assertion.assert_equal(rc, True, "ERR: Set_Display_Events_in_Log_Monitor_to_0_seconds failed")

    def test_06_config_packet_monitor(self):
        logger.info('Config packect monitor to just display dropped packet')
        config = {
            "packet_monitor": {
                "monitor_filter": {
                    "ether_types": "ip",
                    "ip_types": "udp",
                    "destination_ports": "53",
                },
                "display_filter": {
                    "status": {
                        "forwarded": False,
                        "generated": False,
                        "consumed": False,
                    }
                }
            }
        }
        rc = packet_obj.config_packetmoni(**config)
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    def test_07_do_dig_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query(domain2)
        output = True if ('SERVFAIL' in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig test.com successfully.")

    def test_08_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:DNS Reply from Neustar is dropped by DUT failed")


class TestDNS_Filtering_Custom_Domain_03(Test):
    uuid = "SOSAIOT-TC-51552"
    description= show_testcase_info(Parameter.TESTPLAN, '1521016', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1521016')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_domain(self):
        add_domain = {
            "dns_security": {
                "dns_filtering": {
                    "custom_domain": [{
                        "domain": domain3,
                        "category": "4. Malware"
                    }]
                }
            }
        }
        rc = dnssec_obj.add_dns_custom_domain(**add_domain)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_custom_domain failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    def test_03_do_dig_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query(domain3)
        output = True if ('SERVFAIL' in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig www.ea.com successfully.")

    def test_04_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:DNS Reply from Neustar is dropped by DUT failed.")


class TestDNS_Filtering_Custom_Domain_04(Test):
    uuid = "SOSAIOT-TC-51553"
    description= show_testcase_info(Parameter.TESTPLAN, '1521017', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1521017')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_custom_domain(self):
        rc = dnssec_obj.del_custom_domain(domain3)
        Assertion.assert_equal(rc, True, "ERR: test_01_delete_custom_domain failed")

    def test_02_do_dig_to_verify_DNS_query(self):
        flag = False
        time.sleep(10)
        rc = check_action.do_dig_verify_DNS_query(domain3)
        logger.info(rc)
        if 'CNAME' in rc and 'SERVFAIL' not in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR:  DNS Reply from Neustar is forwarded to Client PC failed")
         



