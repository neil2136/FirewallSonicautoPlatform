from definition.settings import *
from definition.utils import *


# Expect: Verify that it can add NAT64 Policy successfullly
class Test_NAT64_TC2(Test):
    uuid = "SOSAIOT-TC-58557"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_policy(self):
        nat64_dict = {
            "name": "tc2",
            "pref64": "Well-Known Pref64",
            "src": {"any": True},
            "translated_src": "X1 IP"
        }
        res = nat64_api.add_nat64_policy(**nat64_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: Add NAT64 policy failed!\033[0m')


# Expect: Verify that it can edit NAT64 Policy successfully
class Test_NAT64_TC7(Test):
    uuid = "SOSAIOT-TC-58567"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_policy(self):
        nat64_dict = {
            "source": {"name": "X0 IPv6 Primary Static Address Subnet"},
        }
        res = nat64_api.edit_nat64_policy_by_name(name='tc2', **nat64_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: edit NAT64 policy failed!\033[0m')


# Expect: Verify the traffic works when configure network /address size of original source and translated source to
# be many-to-one
class Test_NAT64_TC15(Test):
    uuid = "SOSAIOT-TC-58554"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_traffic(self):
        init_packet_capture()
        out = pc1_login.send_command(f'ping6 {Parameter.X1_NAT64_IP} -c 5')
        sleep(3)
        stop_res = pkt_api.stop_capture()
        logger.info(f'\033[1;31mstop packet capture result: " {stop_res}\033[0m')
        Assertion.assert_not_regular(out, '100% packet loss',
                                     '\033[1;31mERR: verify many to one traffic failed!\033[0m')


# Expect: Verify the embedded IPv4 address from IPv4-converted IPv6 address can be recognized and translated when
# n=32/40/48/56/64/96 for Pref64::/n network
class Test_NAT64_TC18(Test):
    uuid = "SOSAIOT-TC-58555"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_pref64_ao(self):
        for pref_len in ('32', '40', '48', '56', '64'):
            pref_ao = {
                'object_type': 'network',
                'name': f"3000::/{pref_len}",
                'zone': 'WAN',
                'subnet': '3000::',
                'mask': f'/{pref_len}'
            }
            res = ao_api.config_ipv6_addressobject(**pref_ao)
            if not res:
                logger.error(f'033[1;31madd {pref_len} addr object failed!!033[0m')
                break
        Assertion.assert_equal(res, True, '\033[1;31mERR: add pref64 addr objects failed!\033[0m')

    def test_02_add_policy(self):
        for pref_len in ('32', '40', '48', '56', '64'):
            nat64_dict = {
                "name": "tc18",
                "pref64":  f"3000::/{pref_len}",
                "src": {"any": True},
                "translated_src": "X1 IP"
            }
            res = nat64_api.add_nat64_policy(**nat64_dict)
            if not res:
                logger.error(f'\033[1;31madd {pref_len} nat64 policy failed!!\033[0m')
                break
        Assertion.assert_equal(res, True, '\033[1;31mERR: Add NAT64 policy failed!\033[0m')

    @repeat_method(3)
    def test_03_test_traffic(self):
        dst_dict = {
            'dst_32': '3000:0:c0c:1a9::',
            'dst_40': '3000:0:c:c01:a9::',
            'dst_48': '3000::c0c:1:a900:0:0',
            'dst_56': '3000::c:c:1a9:0:0',
            'dst_64': '3000::c:c01:a900:0'
        }
        for pref_len in ('32', '40', '48', '56', '64'):
            out = pc1_login.send_command(f'ping6 {dst_dict.get(f"dst_{pref_len}")} -c 5')
            res = '100% packet loss' not in out
            if not res:
                logger.error(f'\033[1;31mcheck {pref_len} nat64 policy traffic failed\033[0m')
                break
        Assertion.assert_equal(res, True,
                               '\033[1;31mERR: verify the traffic when n=32/40/48/56/64/96 for Pref64::/n network failed!\033[0m')


# Expect: Verify the IP header field from IPv6 to IPv4 can translated successfully when no fragmentation happen
class Test_NAT64_TC19(Test):
    uuid = "SOSAIOT-TC-58556"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_IP_header(self):
        res = check_ip_header_from_packet(version='6_to_4')
        Assertion.assert_equal(res, True,
                               "\033[1;31mERR: check IP header field translated from IPv6 to IPv4 failed!\033[0m")


# Expect: Verify the IP header field from IPv4 to IPv6 can translated successfully when no fragmentation happen
class Test_NAT64_TC20(Test):
    uuid = "SOSAIOT-TC-58558"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_check_IP_header(self):
        res = check_ip_header_from_packet(version='4_to_6')
        Assertion.assert_equal(res, True, "\033[1;31mERR: check IP header translated from IPv4 to IPv6 failed!\033[0m")


# Expect: Verify the IP header field from IPv6 to IPv4 can translated successfully when fragmentation happen
class Test_NAT64_TC21(Test):
    uuid = "SOSAIOT-TC-58559"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat64_policy(self):
        nat64_dict = {
            "name": "tc21",
            "pref64": "Well-Known Pref64",
            "src": {"any": True},
            "translated_src": "X1 IP"
        }
        res = nat64_api.add_nat64_policy(**nat64_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: Add NAT64 policy failed!\033[0m')

    def test_02_verify_fragment_ipv6_packet(self):
        res = check_packet(traffic_type='icmpv6_f')
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify fragment ipv6 packet failed!\033[0m')


# Expect: Verify that fragmented UDP traffic can translate successfully from ipv6 host
class Test_NAT64_TC79(Test):
    uuid = "SOSAIOT-TC-58571"
    description = show_testcase_info(TESTPLAN, '79', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '79')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_fragment_udp_packet(self):
        res = check_packet(traffic_type='udp_f')
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify fragment udp packet failed!\033[0m')


# Expect: Verify that fragmented TCP traffic can translate successfully from ipv6 host
class Test_NAT64_TC80(Test):
    uuid = "SOSAIOT-TC-58572"
    description = show_testcase_info(TESTPLAN, '80', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '80')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_fragment_tcp_packet(self):
        res = check_packet(traffic_type='tcp_f')
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify fragment tcp packet failed!\033[0m')


# Expect: Verify that it translate successfully and traffic is reachable when it match NAT64 policy from WAN->LAN /DMZ
class Test_NAT64_TC50(Test):
    uuid = "SOSAIOT-TC-58561"
    description = show_testcase_info(TESTPLAN, '50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_pref64_ao(self):
        pref_ao = {
            'object_type': 'network',
            'name': "64:9999::/96",
            'zone': 'WAN',
            'subnet': '64:9999::',
            'mask': '96'
        }
        res = ao_api.config_ipv6_addressobject(**pref_ao)
        Assertion.assert_equal(res, True, '\033[1;31mERR: Add pref64 addr object failed!\033[0m')

    def test_02_add_nat64_policy(self):
        nat64_dict = {
            "name": "tc50",
            "pref64": "64:9999::/96",
            "src": {"any": True},
            "translated_src": "X1 IP"
        }
        res = nat64_api.add_nat64_policy(**nat64_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: Add NAT64 policy failed!\033[0m')

    def test_02_test_wan_to_dmz_traffic(self):
        out = pc2_login.send_command('ping6 64:9999::c0c:1a9 -c 5')
        Assertion.assert_not_regular(out, '100% packet loss', "\033[1;31mERR: test nat64 traffic from WAN to DMZ "
                                                              "failed!!\033[0m")


# Expect:  Verify that the Translated IPv6 packet will include IPV6 fragment header when ipv4 packet is fragment and DF=0
class Test_NAT64_TC87(Test):
    uuid = "SOSAIOT-TC-58573"
    description = show_testcase_info(TESTPLAN, '87', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '87')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_packet(self):
        res = check_packet(traffic_type='icmpv6_from_wan')
        Assertion.assert_equal(res, True, '\033[1;31mERR: not get the IPv6 fragment header!\033[0m')


# Expect: Verify that it translate successfully and traffic is reachable when it match NAT64 policy from LAN /DMZ/WLAN->WAN
class Test_NAT64_TC51(Test):
    uuid = "SOSAIOT-TC-58562"
    description = show_testcase_info(TESTPLAN, '51', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_test_traffic_from_DMZ_to_WAN(self):
        out = pc3_login.send_command(f'ping6 {Parameter.X1_NAT64_IP} -c 5')
        Assertion.assert_not_regular(out, '100% packet loss',
                                     '\033[1;31mERR: verify many to one traffic failed!\033[0m')


# Expect: Verify that it can translate unicast ICMP traffic successfully
class Test_NAT64_TC56(Test):
    uuid = "SOSAIOT-TC-58563"
    description = show_testcase_info(TESTPLAN, '56', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_icmp_traffic(self):
        Test_NAT64_TC51().test_01_test_traffic_from_DMZ_to_WAN()


# Expect: Verify that it can translate unicast UDP traffic successfully
class Test_NAT64_TC57(Test):
    uuid = "SOSAIOT-TC-58564"
    description = show_testcase_info(TESTPLAN, '57', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_udp_traffic(self):
        res = check_packet(traffic_type='udp', fragment=False)
        Assertion.assert_equal(res, True, "\033[1;31mERR: check udp traffic failed!\033[0m")


# Expect: Verify that it can translate unicast TCP traffic successfully
class Test_NAT64_TC58(Test):
    uuid = "SOSAIOT-TC-58565"
    description = show_testcase_info(TESTPLAN, '58', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_test_tcp_traffic(self):
        res = check_packet(traffic_type='tcp', fragment=False)
        Assertion.assert_equal(res, True, "\033[1;31mERR: check tcp traffic failed!\033[0m")


# Expect: Verify FTP (active/passive) traffic works with NAT64
class Test_NAT64_TC61(Test):
    uuid = "SOSAIOT-TC-58566"
    description = show_testcase_info(TESTPLAN, '61', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '61')

    def test_01_run_ftp_traffic(self):
        res = check_packet(traffic_type='ftp', fragment=False)
        Assertion.assert_equal(res, True, "\033[1;31mERR: check ftp traffic failed!\033[0m")


# Expect: Verify HTTPS traffic works with NAT64 translation
class Test_NAT64_TC71(Test):
    uuid = "SOSAIOT-TC-58568"
    description = show_testcase_info(TESTPLAN, '71', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_test_http_traffic(self):
        out = pc1_login.send_command(f'curl http://[{Parameter.X1_NAT64_IP}]')
        Assertion.assert_regular(out, 'test for nat64', "\033[1;31mERR: test https traffic failed!\033[0m")


# Expect: Verify that NAT64 policy works for the traffic initiated by Sonicwall box
class Test_NAT64_TC73(Test):
    uuid = "SOSAIOT-TC-58569"
    description = show_testcase_info(TESTPLAN, '73', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '73')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_traffic_initiated_by_dut(self):
        diag_api.diag_ping(Parameter.X1_NAT64_IP)
        sleep(3)
        out = diag_api.get_Ping_Result()
        Assertion.assert_regular(json.dumps(out), f'{Parameter.X1_NAT64_IP}.* is alive',
                                 '\033[1;31mERR: test traffic init by sonicwall failed!\033[0m')


# Expect: Log test for NAT64
class Test_NAT64_TC74(Test):
    uuid = "SOSAIOT-TC-58570"
    description = show_testcase_info(TESTPLAN, '74', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '74')
        Assertion.assert_equal(True, True, "\033[1;31mERR: show testcase info failed!\033[0m")

    def test_01_edit_log_setting_for_NAT_mapping(self):
        log_dict = {
            "log": {
                "event": [
                    {
                        "id": 1197,
                        "name": "Connection NAT Mapping",
                        "category": "Network",
                        "group": "NAT",
                        "priority_level": "inform",
                        "log_monitor": {"redundancy_interval": 0},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {"syslog_server_profile": 0},
                        "log_digest": False,
                        "trap": {},
                        "alert_email": {}
                    }
                ]
            }
        }
        res = log_set_api.edit_event(event_id='1197', **log_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: enable GUI for NAT mapping failed!\033[0m')

    def test_02_check_log(self):
        res = False
        cls_res = log_mon_api.clear_log()
        logger.info(f'clear log monitor result: {cls_res}')
        pc1_login.send_command(f'ping6 {Parameter.X1_NAT64_IP} -c 5')
        sleep(5)
        log = log_mon_api.get_log(id=1197)
        if log:
            res = 'Source: 12.12.1.168' in str(log)
        else:
            logger.error('\033[1;31mnot found NAT mapping log about NAT64!\033[0m')
        Assertion.assert_equal(res, True, '\033[1;31mERR: log test for NAT64 failed!\033[0m')


# Expect: Verify that it can ping a Sonicwall box with the IPv4-converted IPv6 address successfully
class Test_NAT64_TC88(Test):
    uuid = "SOSAIOT-TC-58574"
    description = show_testcase_info(TESTPLAN, '88', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '88')

    def test_01_test_traffic(self):
        out = pc1_login.send_command('ping6 64:ff9b::c0c:101 -c 5')
        Assertion.assert_not_regular(out, '100% packet loss', '\033[1;31mERR: test traffic failed!\033[0m')


# Expect: Verify that it can delete NAT64 Policy successfully
class Test_NAT64_TC3(Test):
    uuid = "SOSAIOT-TC-58560"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')

    def test_01_del_nat64_policy(self):
        res = nat64_api.del_nat_policy(name='tc18', version='nat64')
        Assertion.assert_equal(res, True, '\033[1;31mERR: del nat64 policy failed!\033[0m')


# Expect: Verify that the NAT64 policies keep intact and still work after restart DUT
class Test_NAT64_TC92(Test):
    uuid = "SOSAIOT-TC-58575"
    description = show_testcase_info(TESTPLAN, '92', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '92')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_restart_fw(self):
        res = restart_api.restart_now()
        Assertion.assert_equal(res, True, "ERR: restart firewall failed")

    def test_03_check_settings(self):
        res = False
        resp = nat64_api.get_nat64_policy()
        policies = ('tc2', 'tc21', 'tc50')
        try:
            for policy in resp['nat_policies']:
                if policy['nat64'].get('name') not in policies:
                    logger.error(f"{policy['nat64'].get('name')} disappear after restart firewall")
                    res = False
                    break
            else:
                res = True
        except Exception as e:
            logger.error(f'\011[1;31m{repr(e)}\033[0m')
        Assertion.assert_equal(res, True, '\033[1;31mERR: check nat64 settings after restart firewall failed!\033[0m')

    def test_04_test_fun(self):
        Test_NAT64_TC15().test_01_verify_traffic()
        Test_NAT64_TC50().test_02_test_wan_to_dmz_traffic()
