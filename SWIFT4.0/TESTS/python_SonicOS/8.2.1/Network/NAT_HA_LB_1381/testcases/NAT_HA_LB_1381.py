from definition.settings import *


class TestNAT_HA_LB_1(Test):
    uuid = "SOSAIOT-TC-58584"
    description= show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_log(self):
        log_set.logging_level(level='debug')
        time.sleep(2)
        ret = log_obj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_edit_nat_enable_probe(self):
        try:
            ret = natpolicy_obj.get_nat_policy(version='ipv4', name='my_nat_policy')
            logger.info('8' * 60)
            logger.info(ret)
            logger.info('8' * 60)
            probe_var = {
                'probe_type': {'icmp_ping': True},
                'probe_every': 5,
                'reply_timeout': 1,
                'deactivate_after': 3,
                'reactivate_after': 3
            }

            #ret['nat_policies'][0]['ipv4']['high_availability']['probing'] = probe_var
            ret['nat_policies'][0]['ipv4']['high_availability']['probing'].update(probe_var)
            logger.info('7' * 60)
            logger.info(ret)
            logger.info('7' * 60)
            output = natpolicy_obj.edit_nat_policy( **ret )
        except:
            logger.error("get nat policy failed {}".format(ret))
        Assertion.assert_equal(output, True, "ERR: Edit nat policy failed")

    @repeat_method(3)
    def test_03_verify_log(self):
        time.sleep(10) 
        flag = False
        rc5 = log_obj.show_log()
        logger.info('8' * 60)
        logger.info(rc5)
        logger.info('8' * 60)
        for log_entry in rc5:
            match = re.search(r'Network Monitor: Policy NAT PROBE\d+ status is UP', log_entry['message'], re.I)
            if match:
                flag = True
                break
            else:
                logger.info(f"Not found target log:{log_entry}")
        Assertion.assert_equal(flag, True, "ERR: Check log failed")

class TestNAT_HA_LB_2(Test):
    uuid = "SOSAIOT-TC-58596"
    description= show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_packet_monitor(self):
        rc = pm_obj.clear_packets()
        pkt_setting = {
            'monitor_filter':{
                'interfaces': 'X1',
                'ip_types': 'ICMP',
                'ether_types' :'IP',
            }
        }
        rc &= pm_obj.conf_packmon( **pkt_setting )
        rc &= pm_obj.start_capture()
        Assertion.assert_equal(rc, True, "ERR: configure packet monitor failed")

    def test_02_verify_packet(self):
        time.sleep(5)
        flag = False
        ret = pm_obj.stop_capture()
        output = pm_obj.export_captured_packets()
        packets = re.split('Packet number: \d+\*', output)
        pattern = 'out:X1\*.*?Src=\[{}].*?ICMP Type = 8\(ECHO_REQUEST\)'.format(X1_IP)
        for packet in packets:
            packet = packet.replace('\n','').replace('\r\n','')
            logger.info(packet)
            if re.search(r'' + pattern + '', packet, re.I):
                flag = True
                break
            else:
                continue
        Assertion.assert_equal(flag, True, "ERR: verify packet failed")

    def test_03_delete_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name( name = 'my_nat_policy')
        Assertion.assert_equal(rc, True, "ERR:delete nat policy failed")


class TestNAT_HA_LB_3(Test):
    uuid = "SOSAIOT-TC-58585"
    description= show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-8888-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "any",
                    "outbound": "any",
                    "source": {
                        "name": "lan_range"
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "wan_dst"
                    },
                    "translated_destination": {
                        "group": "wan_group"
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    },
                    'nat_method': 'round-robin',
                    'high_availability': {
                        'probing': {
                            'probe_type': {
                                'icmp_ping': True
                            },
                            'probe_every': 5,
                            'reply_timeout': 1,
                            'deactivate_after': 3,
                            'reactivate_after': 3
                        }
                    }
                }
            }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")

    def test_02_verify_packet_round_robin(self):
        flag = 0
        output, output1, output2, output3 = "", "", "", ""
        pm_obj.clear_packets()
        pkt_setting = {
            'monitor_filter':{
                'interfaces': 'X0,X1',
                'ip_types': 'ICMP',
                'ether_types' :'IP',
            }
        }
        pm_obj.conf_packmon( **pkt_setting )

        logger.info("1.get packet traffic from PC1, PC5, PC6!")
        for pc in [localhost, PC5_login, PC6_login]:
            pm_obj.clear_packets()
            pm_obj.start_capture()
            pc.send_command("ping {} -c 5".format(WAN_HOST))
            pm_obj.stop_capture()
            output = pm_obj.export_captured_packets() 
            print(1, '8'*60)
            logger.info(output)
            print(1, '8'*60)
            if pc is localhost:
                output1 = output
            elif pc is PC5_login:
                output2 = output
            elif pc is PC6_login:
                output3 = output

        logger.info("2.verify packets results!")
        pattern = ''
        pattern1 = f'Src=\[{PC1_ETH0_IP}\],.*?Dst=\[{PC3_ETH0_IP}\]'
        pattern2 = f'Src=\[{PC5_ETH0_IP}\],.*?Dst=\[{PC2_ETH0_IP}\]'
        pattern3 = f'Src=\[{PC6_ETH0_IP}\],.*?Dst=\[{PC3_ETH0_IP}\]'
        for output in [output1, output2, output3]:
           if output is output1:
               pattern = pattern1
           elif output is output2: 
               pattern = pattern2
           elif output is output3:
               pattern = pattern3
           packets = re.split('Packet number: \d+\*', output)
           logger.info(pattern)
           for packet in packets:
               packet = packet.replace('\n','').replace('\r\n','')
               logger.info(packet)
               if re.search(r'' + pattern + '', packet, re.I):
                   flag = flag + 1
                   break
               else:
                   continue
           else:
               logger.info(f"ERROR: verify traffic for pattern {pattern} failed")

        Assertion.assert_equal(flag, 3, "ERR: verify packet failed")

    def test_03_delete_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name( name = 'my_nat_policy')
        Assertion.assert_equal(rc, True, "ERR:delete nat policy failed")


class TestNAT_HA_LB_4(Test):
    uuid = "SOSAIOT-TC-58588"
    description= show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-7777-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "any",
                    "outbound": "any",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "wan_dst"
                    },
                    "translated_destination": {
                        "group": "lan_group"
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    },
                    'nat_method': 'sticky-ip',
                    'high_availability': {
                        'probing': {
                            'probe_type': {
                                'icmp_ping': True
                            },
                            'probe_every': 5,
                            'reply_timeout': 1,
                            'deactivate_after': 3,
                            'reactivate_after': 3
                        }
                    }
                }
            }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")
 
    def test_02_allow_wan_to_lan_access_rule(self):
        access_rules = {
            "name": "my_rule",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "name": "wan_range"
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "any": True
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rule_obj.config_accessrule(**access_rules)
        Assertion.assert_equal(rc, True, "ERR: add access rule failed")

    def test_03_config_packet_monitor(self):
        rc = pm_obj.clear_packets()
        pkt_setting = {
            'monitor_filter':{
                'interfaces': 'X0,X1',
                'ip_types': 'ICMP',
                'ether_types' :'IP',
            }
        }
        rc &= pm_obj.conf_packmon( **pkt_setting )
        rc &= pm_obj.start_capture()
        Assertion.assert_equal(rc, True, "ERR: configure packet monitor failed")

    def test_04_verify_packet(self):
        flag = 0
        logger.info("1.get packet traffic from PC2 PC3!")
        output, output2, output3 = "", "", ""
        for pc in [PC2_login, PC3_login]:
            logger.info(pc)
            pm_obj.clear_packets()
            pm_obj.start_capture()
            pc.send_command("ping {} -c 5".format(WAN_HOST))
            pm_obj.stop_capture()
            output = pm_obj.export_captured_packets() 
            print(2, '8'*60)
            logger.info(output)
            print(2, '8'*60)
            if pc is PC2_login:
                output2 = output
            elif pc is PC3_login:
                output3 = output

        logger.info("2.verify packets results!")
        packet2 = re.split('Packet number: \d+\*', output2)
        pattern2 = f'Src=\[{PC2_ETH0_IP}\],.*?Dst=\[{PC6_ETH0_IP}\]' 
        logger.info(pattern2)
        for packet in packet2:
            packet = packet.replace('\n','').replace('\r\n','')
            logger.info(packet)
            if re.search(r'' + pattern2 + '', packet, re.I):
                flag += 1
                break
            else:
                continue
        else:
            logger.info(f"ERROR: verify traffic from {PC2_ETH0_IP} failed")

        packet3 = re.split('Packet number: \d+\*', output3)
        pattern3 = f'Src=\[{PC3_ETH0_IP}\],.*Dst=\[{PC1_ETH0_IP}\]' 
        logger.info(pattern3)
        for packet in packet3:
            packet = packet.replace('\n','').replace('\r\n','')
            logger.info(packet)
            if re.search(r'' + pattern3 + '', packet, re.I):
                flag += 1
                break
            else:
                continue
        else:
            logger.info(f"ERROR: verify traffic from {PC3_ETH0_IP} failed")

        Assertion.assert_equal(flag, 2, "ERR: verify packet failed")

    def test_05_delete_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name( name = 'my_nat_policy')
        Assertion.assert_equal(rc, True, "ERR:delete nat policy failed")

    def test_06_delete_access_rule(self):
        rc = access_rule_obj.delete_accessrule_by_name(name='my_rule')
        Assertion.assert_equal(rc, True, "ERR: del access rule failed")
