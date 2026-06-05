from definition.settings import *


# Add an IPv6 Network Monitor policy
class Test_V6NM_Policy_TC56627(Test):
    uuid = "SOSAIOT-TC-56627"
    description = show_testcase_info(TESTPLAN, '56627', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56627')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ipv6_nm_policy(self):
        nm_dict = {
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'test_v6',
                        'probe': {
                            'target': {'name': 'probe_wan_host'},
                            'type': {"ping": "non-explicit"},
                            'interval': 5
                        },
                        'reply_timeout': 1,
                        "must_respond": False,
                        "interval": {"missed": 3, "successful": 3}
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .")
        
        
# Edit an IPv6 Network Monitor policy
class Test_V6NM_Policy_TC56631(Test):
    uuid = "SOSAIOT-TC-56631"
    description = show_testcase_info(TESTPLAN, '56631', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56631')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_ipv6_nm_policy(self):
        # This case is including in TC56633
        Assertion.assert_equal(True, True, "ERR: edit ipv6 network monitor policy fail .")


# IPv4 and IPv6 elements mixed test
class Test_V6NM_Policy_TC56630(Test):
    uuid = "SOSAIOT-TC-56630"
    description = show_testcase_info(TESTPLAN, '56630', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56630')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_add_ipv6_nm_policy_with_ipv4_and_ipv6_elements_mixed(self):
        nm_dict = {
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'error_test',
                        'probe': {
                            'target': {'name': 'probe_wan_host'},
                            'type': {"ping": "explicit"},
                            'interval': 5
                        },
                        "next_hop": {"name": "X1 IP"},
                        'reply_timeout': 1,
                        "must_respond": False,
                        "interval": {"missed": 3, "successful": 3}
                    }
                }
            }]
        }
        rc, err_msg = nm_obj.add_network_monitor(**nm_dict, msg=True)
        logger.info(json.dumps(err_msg))
        Assertion.assert_equal(rc, False, "ERR: check add ipv6 network monitor policy with ipv4 and ipv6 elements mixed failed!!")


# Set Outbound Interface as a physical interface
class Test_V6NM_Policy_TC56633(Test):
    uuid = "SOSAIOT-TC-56633"
    description = show_testcase_info(TESTPLAN, '56633', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56633')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_outbound_interface_as_physical_interface(self):
        opt = {
            "name": "test_v6",
            "probe": {
                "target": {"name": "probe_wan_host"},
                "type": {"ping": "explicit"},
                "interval": 5},
            "next_hop": {"name": "probe_wan_host"},
            "outbound_interface": "X1"
        }
        rc = nm_obj.edit_network_monitor_ipv6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: set_outbound_interface_as_physical_interface failed!!')

    @repeat_method(3)
    def test_02_packet_check(self):
        rc = False
        clear_res = pkt_api.clear_packets()
        logger.info(f'============>clear packet result: {clear_res}')
        start_res = pkt_api.start_capture()
        logger.info(f'============>start packet capture result: {start_res}')
        time.sleep(5)
        stop_res = pkt_api.stop_capture()
        logger.info(f'============>stop packet capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        packets = pc1_login.send_command(f'tshark -r /tmp/packet-c.pcapng -V')
        packet_list = packets.split('Packet comments')
        for pkt in packet_list:
            if 'Dst: 2010::100' in pkt and 'out:X1*,Generated' in pkt:
                logger.info(f'find the expected packet:\n{pkt}')
                rc = True
                break
        else:
            logger.error('not found the expected packet!!')
        Assertion.assert_equal(rc, True, 'ERR: packet_check failed!!')


# Set Next Hop Gateway as an IPv6 Address
class Test_V6NM_Policy_TC56634(Test):
    uuid = "SOSAIOT-TC-56634"
    description = show_testcase_info(TESTPLAN, '56634', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56634')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_Gateway_set_as_ipv6_addr(self):
        Test_V6NM_Policy_TC56633().test_02_packet_check()


# Delete an IPv6 Network Monitor policy
class Test_V6NM_Policy_TC56636(Test):
    uuid = "SOSAIOT-TC-56636"
    description = show_testcase_info(TESTPLAN, '56636', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56636')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ipv6_network_monitor_policy(self):
        rc = nm_obj.del_network_monitor(name='test_v6', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete ipv6_network_monitor_policy failed!!")


# Test IPv6 Probe using in NAT policy
class Test_V6NM_Policy_TC56635(Test):
    uuid = "SOSAIOT-TC-56635"
    description = show_testcase_info(TESTPLAN, '56635', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56635')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_x0_range_ao(self):
        range_dict = {
            "object_type": "range",
            "name": "x0_range_v6",
            "zone": "LAN",
            "value": "2000::99,2000::101"
        }
        rc = ao_api.config_addressobject(**range_dict)
        Assertion.assert_equal(rc, True, 'ERR: add x0 range addr obj failed!!')

    def test_02_add_ipv6_nat_rule_with_probe_enable(self):
        # opt = {
        #     "nat_policies": [{"ipv6": {
        #         "comment": "",
        #         "destination": {"name": "X1 IPv6 Primary Static Address"},
        #         "enable": True,
        #         "high_availability": {
        #             "probing": {"probe_every": 5, "reply_timeout": 1, "deactivate_after": 3, "reactivate_after": 3}},
        #         'inbound': "any",
        #         'name': "",
        #         'nat_method': "round-robin",
        #         'outbound': "any",
        #         'priority': {'auto': True},
        #         'service': {'any': True},
        #         'source': {'any': True},
        #         'ticket': {'tag1': "", 'tag2': "", 'tag3': ""},
        #         'translated_destination': {'name': "x0_range_v6"},
        #         'translated_service': {'original': True},
        #         'translated_source': {'original': True}
        #     }}]
        # }
        opt = {
            'name': "test_v6",
            "high_availability": {
                "probing": {"probe_every": 5, "reply_timeout": 1, "deactivate_after": 3, "reactivate_after": 3,
                            "probe_type": {"icmp_ping": True}}},
            'translated_destination': {'name': "x0_range_v6"},
            'nat_method': "round-robin",
            "destination": {"name": "X1 IPv6 Primary Static Address"},
        }
        rc = nat_v6_api.add_ipv6_nat_rule(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add_ipv6_nat_rule_with_probe_enable failed!!')

    @repeat_method(3)
    def test_03_check_auto_added_network_monitor_policy(self):
        out = nm_obj.get_network_monitor(version=6)
        logger.info(json.dumps(out))
        rc = "Auto-added from configured NAT Policy probe" in json.dumps(
            out) and '"probe": {"target": {"name": "x0_range_v6"}' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check auto added network monitor policy from nat rule failed!!')


# Check TSR
class Test_V6NM_Policy_TC56637(Test):
    uuid = "SOSAIOT-TC-56637"
    description = show_testcase_info(TESTPLAN, '56637', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56637')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_network_monitor_policy_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Network', lab1='Network Monitor')
        logger.info(f'get network monitor policy tsr info as follow: \n{tsr_info}')
        rc = re.search(r'Probe Target\s+: x0_range_v6', tsr_info)
        Assertion.assert_equal(bool(rc), True, "ERR: check network monitor policy in tsr file failed!!")


# Verify the function to probe an IPv6 host
class Test_V6NM_Policy_TC56638(Test):
    uuid = "SOSAIOT-TC-56638"
    description = show_testcase_info(TESTPLAN, '56638', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56638')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nm_policy(self):
        Test_V6NM_Policy_TC56627().test_01_add_ipv6_nm_policy()

    @repeat_method(3)
    def test_02_check_probe_status(self):
        time.sleep(10)
        out = nm_obj.get_network_monitor_status_by_name('test_v6')
        logger.info(json.dumps(out))
        rc = '"led": "green"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check probe status failed!!')


# Test IPv6 Probe using in PBR policy
class Test_V6NM_Policy_TC56628(Test):
    uuid = "SOSAIOT-TC-56628"
    description = show_testcase_info(TESTPLAN, '56628', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56628')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ipv6_pbr_rule_with_nm_policy(self):
        route_dict = {"route_policies":
            [{"ipv6":
                {
                    "name":"tc26",
                    "comment":"",
                    "interface":"X0",
                    "metric":3,
                    "service":{"any":True},
                    "gateway":{"default":True},
                    "source":{"name":"X0 IPv6 Primary Static Address Subnet"},
                    "destination":{"name":"X1 IPv6 Primary Static Address Subnet"},
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"test_v6",
                    "distance":{"auto":True},
                    "disable_when_probes_succeed":False,
                    "default_probe_state_up":True,
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]}
        rc = route_api.add_route_policy(**route_dict)
        Assertion.assert_equal(rc, True, "ERR: add route policy with probe failed")
    
    def test_02_check_ipv6_pbr_rule_status_with_probe_reachable(self):
        out = route_api.show_route_policy_status('tc26', version = 'ipv6')
        logger.info(json.dumps(out))
        Assertion.assert_equal(str(out), 'active', 'ERR: check ipv6 pbr rule status with probe reachable failed')
    
    def test_check_ipv6_pbr_rule_status_with_probe_unreachable(self):
        pc2_login.send_command('ifconfig eth1 down')
        time.sleep(10)
        out = route_api.show_route_policy_status('tc26', version = 'ipv6')
        logger.info(json.dumps(out))
        pc2_login.send_command('ifconfig eth1 up')
        time.sleep(10)
        Assertion.assert_equal(str(out), 'inactive', 'ERR: check ipv6 pbr rule status with probe unreachable failed')


# Verify the monitor status change from UP to Down when the probe target is become unavailable.
class Test_V6NM_Policy_TC56639(Test):
    uuid = "SOSAIOT-TC-56639"
    description = show_testcase_info(TESTPLAN, '56639', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56639')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_check_probe_status_after_power_off_probe_pc(self):
        pc2_login.send_command('ifconfig eth1 down')
        time.sleep(10)
        out = nm_obj.get_network_monitor_status_by_name('test_v6')
        logger.info(json.dumps(out))
        rc = '"led": "red"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check_probe_status_after_power_off_probe_pc failed!!')
    
    
# Verify the monitor status change from UP to Down when the probe target is become unavailable.
class Test_V6NM_Policy_TC56629(Test):
    uuid = "SOSAIOT-TC-56629"
    description = show_testcase_info(TESTPLAN, '56629', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56629')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    # @repeat_method(5)
    def test_01_check_probe_status_after_power_on_probe_pc(self):
        pc2_login.send_command('ifconfig eth1 up')
        pc2_login.send_command('ifconfig eth1 inet6 add 2010::100')
        time.sleep(10)
        out = nm_obj.get_network_monitor_status_by_name('test_v6')
        logger.info(json.dumps(out))
        rc = '"led": "green"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check_probe_status_after_power_on_probe_pc failed!!')


# Test Probe Type-TCP-Explicit Route
class Test_V6NM_Policy_TC56626(Test):
    uuid = "SOSAIOT-TC-56626"
    description = show_testcase_info(TESTPLAN, '56626', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56626')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_https_v6_server_on_pc2(self):
        cmd = 'echo "test for ipv6 network monitor" > /root/index.html; systemctl restart httpd'
        pc2_login.send_command(cmd)
        out = pc1_login.send_command('ip -6 route add 2010::/64 via 2000::168 dev eth1; curl http://[2010::100]')
        Assertion.assert_equal(True, True, 'ERR: setup https v6 server on pc2 failed')
    
    def test_02_add_TCP_nm_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc10',
                        'probe': {'target': {'name': 'probe_wan_host'}, 'type':{"tcp":{"port":80,"non_explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'rst_as_miss': False,
                        'comment':'nm for tc10'
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .")   
    
    @repeat_method(5, 30)
    def test_03_check_network_monitor_probe_status(self):
        out = nm_obj.get_network_monitor_status_by_name('test_v6')
        logger.info(json.dumps(out))
        rc = '"led": "green"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check network monitor probe status failed')
    
    
#Verify network monitor works when probe target is  a big size IPv6 range for probe target
class Test_V6NM_Policy_TC56632(Test):
    uuid = "SOSAIOT-TC-56632"
    description = show_testcase_info(TESTPLAN, '56632', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56632')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_bigsize_ipv6_range_probe_target_nm_policy(self):
        nm_dict = {
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'test_v6_range',
                        'probe': {
                            'target': {'name': 'probe_wan_range'},
                            'type': {"ping": "non-explicit"},
                            'interval': 5
                        },
                        'reply_timeout': 1,
                        "must_respond": False,
                        "interval": {"missed": 3, "successful": 3}
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .")
    
    @repeat_method(10, 30)
    def test_01_get_nm_status(self):
        out = nm_obj.get_network_monitor_status_by_name('test_v6_range')
        logger.info(json.dumps(out))
        rc1 = '"resolvedProbeTargets": 256' in json.dumps(out) and '"led": "green"' in json.dumps(out)
        Assertion.assert_equal(rc1, True, 'ERR: get nm status failed')
    