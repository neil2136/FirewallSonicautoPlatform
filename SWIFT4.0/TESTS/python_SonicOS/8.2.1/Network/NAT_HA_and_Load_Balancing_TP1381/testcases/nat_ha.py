from definition.settings import *
from definition.utils import *


# Expect: Enable Probe
class Test_NAT_HA_TC01(Test):
    uuid = "SOSAIOT-TC-58584"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_with_probe_enable(self):
        init_dict = deepcopy(nat_base)
        edit_dict = {
            'name': 'tc01',
            "destination": {"name": 'X1_NAT'},
            "translated_destination": {"name": "X0_range"}
        }
        init_dict.update(edit_dict)
        nat_json = {"nat_policies": [{"ipv4": init_dict}]}
        res = nat_api.add_nat_policy(**nat_json)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add nat policy with probe enable failed!\033[0m')

    def test_02_verify_probe_is_sent(self):
        res = check_probe_packet()
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify probe is sent failed.\033[0m')


# Expect: Probe type ping
class Test_NAT_HA_TC03(Test):
    uuid = "SOSAIOT-TC-58596"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_test_icmp_traffic_is_sent(self):
        Test_NAT_HA_TC01().test_02_verify_probe_is_sent()


# Expect: Probe type TCP
class Test_NAT_HA_TC04(Test):
    uuid = "SOSAIOT-TC-58600"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_probe_type_to_tcp(self):
        edit_dict = {
            "high_availability": {
                "probing": {
                    "probe_type": {"tcp": 80}
                }
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: updat probe type for nat rule failed!\033[0m')

    def test_02_verify_probe_pkt_is_sent(self):
        res = check_probe_packet(pro_type='tcp')
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify probe is sent failed.\033[0m')


# Expect: Probe port
class Test_NAT_HA_TC05(Test):
    uuid = "SOSAIOT-TC-58603"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_probe_port(self):
        edit_dict = {
            "high_availability": {
                "probing": {
                    "probe_type": {"tcp": 443}
                }
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: disable probe option for nat rule failed!\033[0m')

    def test_02_verify_probe_pkt(self):
        res = check_probe_packet(pro_type='tcp_port')
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify probe port in packet failed.\033[0m')


# Expect: Probe interval
class Test_NAT_HA_TC07(Test):
    uuid = "SOSAIOT-TC-58604"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_probe_interval(self):
        edit_dict = {
            "high_availability": {
                "probing": {
                    "probe_type": {"icmp_ping": True},
                    "probe_every": 10
                }
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: update probe interval for nat rule failed!\033[0m')

    @repeat_method(3)
    def test_02_verify_probe_pkt_interval(self):
        init_packet_capture()
        sleep(23)
        stop_res = pkt_api.stop_capture()
        logger.info(f'stop capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng')
        # m = re.findall(r'(\d+\.\d+)\s+192.168.168.168 -> 192.168.168.169 ICMP 76 Echo \(ping\) request', pkts)
        m = re.findall(r'(\d+\.\d+)\s+192.168.168.168 -> 192.168.168.169 ICMP.*request', pkts)
        logger.info(m)
        res = 9.5 <= float(m[1]) - float(m[0]) < 11 if len(m) >= 2 else False
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify probe port in packet failed.\033[0m')


# Expect: Test probing in DMZ
class Test_NAT_HA_TC48(Test):
    uuid = "SOSAIOT-TC-58601"
    description = show_testcase_info(TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_rule_map_for_x2(self):
        init_dict = deepcopy(nat_base)
        edit_dict = {
            'name': 'tc48',
            "destination": {"name": 'X1_NAT'},
            "translated_destination": {"name": "X2_range"}
        }
        init_dict.update(edit_dict)
        nat_json = {"nat_policies": [{"ipv4": init_dict}]}
        res = nat_api.add_nat_policy(**nat_json)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add nat policy with probe enable failed!\033[0m')

    def test_02_verify_probe_sent_from_x2(self):
        res = check_probe_packet(iface=Parameter.X2_IP)
        Assertion.assert_equal(res, True, '\033[1;31mERR: verify probe is sent from X2 failed.\033[0m')


# Expect: Probing enabled and change translated destination to a single target
class Test_NAT_HA_TC49(Test):
    uuid = "SOSAIOT-TC-58602"
    description = show_testcase_info(TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_translated_dst_to_host(self):
        edit_dict = {
            "translated_destination": {"name": "X0 IP"}
        }
        res, _ = nat_api.edit_nat_policy_by_name(name='tc48', **edit_dict, msg=True)
        Assertion.assert_equal(res, False, '\033[1;31mERR: update nat policy translated dst to host failed!\033[0m')

    def test_03_del_nat_rule_map_for_x2(self):
        res = nat_api.del_nat_policy_by_name(name='tc48')
        Assertion.assert_equal(res, True, '\033[1;31mERR: del nat rule map for X2.\033[0m')


# Expect:NAT Method Round Robin- source ANY to pool with Address Object containing hosts
class Test_NAT_HA_TC14(Test):
    uuid = "SOSAIOT-TC-58585"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_nat_method_round_robin(self):
        edit_dict = {
            "nat_method": "round-robin",
            "high_availability": {
                "probing": {
                    "probe_type": {"icmp_ping": True},
                    "probe_every": 5
                }
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: set nat method to round robin failed!\033[0m')

    @repeat_method(3)
    def test_02_test_traffic(self):
        src_1 = get_dst_ip_from_packet(pc2_login)
        src_2 = get_dst_ip_from_packet(pc4_login)
        rc = src_1 != src_2 if src_1 else False
        Assertion.assert_equal(rc, True, '\033[1;31mERR: test traffic failed!\033[0m')


# Expect: Round Robin missed probes - resource down
class Test_NAT_HA_TC17(Test):
    uuid = "SOSAIOT-TC-58586"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_down_pc3_and_check_log(self):
        cls_res = log_api.clear_log()
        logger.info(f'clear log monitor result: {cls_res}')
        pc3_login.send_command('ifconfig eth1 up')
        sleep(30)
        pc3_login.send_command('ifconfig eth1 down')
        sleep(30)
        log = log_api.get_log(id=706)
        logger.info(log)
        Assertion.assert_equal(bool(log), True, '\033[1;31mERR: verify log message when resource down failed!\033[0m')

    @repeat_method(3)
    def test_02_test_traffic(self):
        src_1 = get_dst_ip_from_packet(pc2_login)
        src_2 = get_dst_ip_from_packet(pc4_login)
        rc = src_1 == src_2 if src_1 else False
        Assertion.assert_equal(rc, True,
                               '\033[1;31mERR: verify traffic is devided between remain services failed!\033[0m')


# Expect: Round Robin missed probes - resource restore
class Test_NAT_HA_TC18(Test):
    uuid = "SOSAIOT-TC-58587"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_up_pc3_and_check_log(self):
        cls_res = log_api.clear_log()
        logger.info(f'clear log monitor result: {cls_res}')
        pc3_login.send_command('ifconfig eth1 down')
        sleep(30)
        pc3_login.send_command('ifconfig eth1 up')
        sleep(30)
        log = log_api.get_log(id=707)
        logger.info(log)
        Assertion.assert_equal(bool(log), True, '\033[1;31mERR: verify log message when resource up failed!\033[0m')

    @repeat_method(3)
    def test_02_verify_traffic(self):
        Test_NAT_HA_TC14().test_02_test_traffic()


# Expect: NAT Method Sticky IP- source ANY to pool with Address Object containing hosts
class Test_NAT_HA_TC19(Test):
    uuid = "SOSAIOT-TC-58588"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_nat_method_sticky_ip(self):
        edit_dict = {
            "nat_method": "sticky-ip"
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: set nat method to sticky ip failed!\033[0m')

    @repeat_method(3)
    def test_01_verify_traffic(self):
        Test_NAT_HA_TC14().test_02_test_traffic()


# Expect: Sticky IP missed probes - resource down
class Test_NAT_HA_TC22(Test):
    uuid = "SOSAIOT-TC-58590"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_down_resource(self):
        Test_NAT_HA_TC17().test_01_down_pc3_and_check_log()
        Test_NAT_HA_TC17().test_02_test_traffic()


# Expect: Sticky IP successful probes - resource restored
class Test_NAT_HA_TC23(Test):
    uuid = "SOSAIOT-TC-58591"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_up_resource(self):
        Test_NAT_HA_TC18().test_01_up_pc3_and_check_log()
        Test_NAT_HA_TC14().test_02_test_traffic()


# Expect: NAT Method Block remapping - source Network to pool with Address Object containing range
class Test_NAT_HA_TC25(Test):
    uuid = "SOSAIOT-TC-58592"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_nat_method_sticky_ip(self):
        edit_dict = {
            "source": {"name": "x1_net"},
            "nat_method": "block-remap"
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: set nat method to block remap failed!\033[0m')

    @repeat_method(3)
    def test_02_test_traffic(self):
        Test_NAT_HA_TC17().test_02_test_traffic()


# Expect: Block remapping missed probes - resource down
class Test_NAT_HA_TC26(Test):
    uuid = "SOSAIOT-TC-58593"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_down_resource(self):
        Test_NAT_HA_TC17().test_01_down_pc3_and_check_log()
        Test_NAT_HA_TC17().test_02_test_traffic()


# Expect: Block remapping successful probes - resource restored
class Test_NAT_HA_TC27(Test):
    uuid = "SOSAIOT-TC-58594"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_up_resource(self):
        Test_NAT_HA_TC18().test_01_up_pc3_and_check_log()
        Test_NAT_HA_TC17().test_02_test_traffic()


# Expect: Disable Probe
class Test_NAT_HA_TC02(Test):
    uuid = "SOSAIOT-TC-58589"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_probe_of_nat_rule(self):
        edit_dict = {
            "high_availability": {
                "probing": {}
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: disable probe for nat rule failed!\033[0m')

    def test_02_verify_probe_is_not_sent(self):
        res = check_probe_packet()
        Assertion.assert_equal(res, False, '\033[1;31mERR: verify probe is not sent failed.\033[0m')


# Expect:NAT Method Symmetrical Mapping - source Network to pool with Address Object containing Network
class Test_NAT_HA_TC29(Test):
    uuid = "SOSAIOT-TC-58595"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_nat_method_symmetrical_remap(self):
        edit_dict = {
            "translated_destination": {"name": "x0_net"},
            "nat_method": "symmetrical-remap"
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: set nat method to block remap failed!\033[0m')

    @repeat_method(3)
    def test_02_test_traffic(self):
        Test_NAT_HA_TC14().test_02_test_traffic()


# Expect:  NAT Method Random distribution- source ANY to pool with Address Object containing hosts
class Test_NAT_HA_TC32(Test):
    uuid = "SOSAIOT-TC-58597"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_nat_method_Random_Distribution(self):
        edit_dict = {
            "nat_method": "random-distribution",
            "translated_destination": {"name": "X0_range"},
            "high_availability": {
                "probing":
                    {
                        "deactivate_after": 3,
                        "probe_every": 10,
                        "probe_type": {"icmp_ping": True},
                        "reactivate_after": 3,
                        "reply_timeout": 2
                    }
            }
        }
        res = nat_api.edit_nat_policy_by_name(name='tc01', **edit_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: set nat method to block remap failed!\033[0m')

    @repeat_method(3)
    def test_02_test_traffic(self):
        out1 = get_dst_ip_from_packet(pc2_login)
        out2 = get_dst_ip_from_packet(pc4_login)
        Assertion.assert_equal(bool(out1) & bool(out2), True,
                               '\033[1;31mERR: set verify traffic for random method failed!\033[0m')


# Expect: Random distribution missed probes - resource down
class Test_NAT_HA_TC35(Test):
    uuid = "SOSAIOT-TC-58598"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_down_resource(self):
        Test_NAT_HA_TC17().test_01_down_pc3_and_check_log()
        Test_NAT_HA_TC32().test_02_test_traffic()


# Expect:  Random distribution successful probes - resource restored
class Test_NAT_HA_TC36(Test):
    uuid = "SOSAIOT-TC-58599"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_test_up_resource(self):
        Test_NAT_HA_TC18().test_01_up_pc3_and_check_log()
        Test_NAT_HA_TC32().test_02_test_traffic()
