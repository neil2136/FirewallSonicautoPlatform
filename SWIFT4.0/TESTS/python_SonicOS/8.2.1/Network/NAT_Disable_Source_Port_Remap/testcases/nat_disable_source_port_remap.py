from definition.settings import *
from definition.utils import *


# Expect: [GUI]Verify the checkbox "disable source port remap" is added in the advanced tab for nat policy and disabled as default
class TestNatPortRemap_TC1(Test):
    uuid = "SOSAIOT-TC-58577"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_new_nat_policy(self):
        res = False
        base_dict = {
            'name': 'test_for_case_1',
            "translated_source": {
                "name": "X1 IP"
            }
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        (addres, msg) = natpolicyapi.add_nat_policy(**nat_dict, msg=True)
        if addres:
            resp = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(resp) else False
        else:
            logger.error(f'add nat policy failed. \nfailed resson: {msg}')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed.')

    def test_02_check_option_default_status(self):
        resp = natpolicyapi.get_nat_policy(name='test_for_case_1')
        Assertion.assert_regular(json.dumps(resp), '"source_port_remap": true',
                                 'verify default status of Source Port Remap option failed')


# Expect: [GUI]Verify the checkbox "disable source port remap" cannot be selected (grey out) in the advanced tab if the "Translated Source" is "Original"
class TestNatPortRemap_TC2(Test):
    uuid = "SOSAIOT-TC-58580"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_new_nat_policy(self):
        res = False
        base_dict = {
            "name": "test_for_case_2",
            "destination": {
                "name": "X0 IP"
            },
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        (addres, msg) = natpolicyapi.add_nat_policy(**nat_dict, msg=True)
        if addres:
            resp = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(resp) else False
        else:
            logger.error(f'add nat policy failed. \nfailed resson: {msg}')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed.')

    def test_02_verify_option_cannot_be_edited(self):
        edit_dict = {
            "name": "test_for_case_2",
            "destination": {
                "name": "X0 IP"
            },
            "source_port_remap": True
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(edit_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        (editres, msg) = natpolicyapi.edit_nat_policy(**nat_dict, msg=True)
        logger.info(f'edit result: {editres}')
        logger.info(f'failed reason: {msg}')
        Assertion.assert_equal(
            editres, False, 'verify option cannot be edited failed.')


# Expect: [GUI]Verify the checkbox "disable source port remap" can be enabled for both IPv4 and IPv6 NAT policy
class TestNatPortRemap_TC3(Test):
    uuid = "SOSAIOT-TC-58581"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_option_for_v4nat(self):
        res = False
        edit_dict = {
            'name': 'test_for_case_1',
            "translated_source": {
                "name": "X1 IP"
            },
            "source_port_remap": False
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(edit_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        (editres, msg) = natpolicyapi.edit_nat_policy(**nat_dict, msg=True)
        if editres:
            resp = natpolicyapi.get_nat_policy(name=edit_dict['name'])
            res = True if '"source_port_remap": false' in json.dumps(
                resp) else False
        else:
            logger.error(
                f'disable source port remap failed. \nfailed reson:{msg}')
        Assertion.assert_equal(
            res, True, 'disable option for v4 nat policy failed.')

    def test_02_add_v6_nat_policy(self):
        res = False
        base_v6_dict = {
            "name": "test_v6",
            "source": {"name": "X0 IPv6 Primary Static Address Subnet"},
            "translated_source": {"name": "X1 IPv6 Primary Static Address"},
            "source_port_remap": False
        }
        nat_base_new = copy.deepcopy(nat_v6_base_dict)
        nat_base_new.update(base_v6_dict)
        nat_v6_dict = {"nat_policies": [{"ipv6": nat_base_new}]}
        (addres, msg) = natpolicyapi.add_nat_policy(**nat_v6_dict, msg=True)
        if addres:
            resp = natpolicyapi.get_nat_policy(
                version='ipv6', name=base_v6_dict['name'])
            res = True if base_v6_dict['name'] in str(resp) else False
        else:
            logger.error(f'add v6 nat policy failed. \nfailed resson: {msg}')
        Assertion.assert_equal(res, True, 'ERR: add v6 nat policy failed.')


# Expect:[FUN]Verify the checkbox "disable source port remap" works for IPv4 NAT policy
class TestNatPortRemap_TC5(Test):
    uuid = "SOSAIOT-TC-58582"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_new_nat_policy(self):
        res = False
        base_dict = {
            "name": "test_for_case_5",
            "source": {"name": "X0 Subnet"},
            "translated_source": {"name": 'X1 IP'},
            "source_port_remap": False
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        (addres, msg) = natpolicyapi.add_nat_policy(**nat_dict, msg=True)
        if addres:
            resp = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(resp) else False
        else:
            logger.error(f'add nat policy failed. \nfailed reason: {msg}')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed.')

    @repeat_method(3)
    def test_02_verfiy_v4_option_function(self):
        fw_config_capture_monitor()
        pc_send_tcp_packets(PC1_ETH1_IP, PC2_ETH1_IP)
        time.sleep(3)
        packetapi.stop_capture()
        packets = packetapi.export_captured_packets()
        src_port, dst_port = get_tcp_packet_port_number(packets, PC1_ETH1_IP, PC2_ETH1_IP)
        tsl_src_port, tsl_dst_port = get_tcp_packet_port_number(packets, Parameter.X1_IP, PC2_ETH1_IP)
        Assertion.assert_equal(
            (src_port, dst_port) == (tsl_src_port, tsl_dst_port), True, 'ERR: verfiy disable source port remap option v4 failed')


# Expect:[FUN]Verify the checkbox "disable source port remap" works for IPv6 NAT policy
class TestNatPortRemap_TC6(Test):
    uuid = "SOSAIOT-TC-58583"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_02_verfiy_option_function(self):
        res = False
        fw_config_capture_monitor()
        # 2000::100 ,2001::100
        # cmd = f'python3 {script_path} -src_ip {PC1_ETH1_IPv6} -dst_ip {PC2_ETH1_IPv6} -src_port 22222 -dst_port 44444'
        cmd = 'python3 %s -src_ip %s -dst_ip %s -src_port %d -dst_port %d' % (
            script_file, PC1_ETH1_IPv6, PC2_ETH1_IPv6, 22222, 44444)
        pc1_login.send_command(cmd)
        time.sleep(3)
        packetapi.stop_capture()
        packets = packetapi.export_captured_packets()
        src_port, dst_port = get_tcp_packet_port_number(
            packets, PC1_ETH1_IPv6, PC2_ETH1_IPv6)  # 2000::100', '2001::100'
        tls_src_port, tls_dst_port = get_tcp_packet_port_number(
            packets, Parameter.X1_V6_IP, PC2_ETH1_IPv6)  # '2001::168', '2001::100'
        Assertion.assert_equal(
            (src_port, dst_port)==(tls_src_port, tls_dst_port), True, 'ERR: verfiy disable source port remap option v6 failed')


# Expect: [FUN]Verify the checkbox "disable source port remap" works for ICMP traffic(IPv4 /IPv6)
class TestNatPortRemap_TC11(Test):
    uuid = "SOSAIOT-TC-58578"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_02_verify_v4_icmp(self):
        res = False
        fw_config_capture_monitor()
        pc1_login.ping_from_eth(
            ip=PC2_ETH1_IP, eth='eth1', num=2)  # '12.12.1.169'
        time.sleep(3)
        packetapi.stop_capture()
        packetapi.export_captured_packets_pcapng(
            filepath='/tmp/packet-c_v4.pcapng')
        cmd = 'tshark -r /tmp/packet-c_v4.pcapng > /tmp/packets_v4.txt'
        pc1_login.send_command(cmd)
        src_id = get_icmp_identifer('/tmp/packets_v4.txt', PC1_ETH1_IP, PC2_ETH1_IP)  # 192.168.168.169, 12.12.1.169
        logger.info(f'src_id: {src_id}')
        translated_id = get_icmp_identifer('/tmp/packets_v4.txt',Parameter.X1_IP, PC2_ETH1_IP)
        logger.info(f'translated_id: {translated_id}')
        if src_id:
            res = src_id == translated_id
            logger.info(f"result: {res}")
        Assertion.assert_equal(res, True, 'verify v4 icmp failed.')

    @repeat_method(3)
    def test_03_verify_v6_icmp(self):
        res = False
        fw_config_capture_monitor()
        pc1_login.send_command(f'ping6 -c 2 {PC2_ETH1_IPv6}')  # 2001::100
        time.sleep(10)
        packetapi.stop_capture()
        packetapi.export_captured_packets_pcapng(
            filepath='/tmp/packet-c_v6.pcapng')
        cmd = 'tshark -r /tmp/packet-c_v6.pcapng > /tmp/packets_v6.txt'
        pc1_login.send_command(cmd)
        src_id = get_icmp_identifer(
            '/tmp/packets_v6.txt', PC1_ETH1_IPv6, PC2_ETH1_IPv6, 'ipv6')  # 2000::100, 2001::100
        translated_id = get_icmp_identifer(
            '/tmp/packets_v6.txt', Parameter.X1_V6_IP, PC2_ETH1_IPv6, 'ipv6')  # 2001::168, 2001::100
        Assertion.assert_equal(src_id == translated_id, True, 'verify icmpv6 failed.')


# Expect: [FUN]Verify the option value is kept intact and function is still working after a reboot
class TestNatPortRemap_TC16(Test):
    uuid = "SOSAIOT-TC-58579"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_reboot_fw(self):
        res = settingsapi.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot FW failed")

    def test_02_check_settings(self):
        resp_v4 = natpolicyapi.get_nat_policy(name='test_for_case_1')
        res_v4 = True if '"source_port_remap": false' in json.dumps(
            resp_v4) else False
        resp_v6 = natpolicyapi.get_nat_policy(version='ipv6', name='test_v6')
        res_v6 = True if '"source_port_remap": false' in json.dumps(
            resp_v6) else False
        Assertion.assert_equal(res_v4 & res_v6, True,
                               'check settings after reboot failed')

    @repeat_method(3)
    def test_03_check_v4_fun(self):
        res = False
        fw_config_capture_monitor()
        pc1_login.ping_from_eth(
            ip=PC2_ETH1_IP, eth='eth1', num=2)  # '12.12.1.169'
        time.sleep(3)
        packetapi.stop_capture()
        packetapi.export_captured_packets_pcapng(
            filepath='/tmp/packet-c_v4_2.pcapng')
        cmd = 'tshark -r /tmp/packet-c_v4_2.pcapng > /tmp/packets_v4_2.txt'
        pc1_login.send_command(cmd)
        src_id = get_icmp_identifer('/tmp/packets_v4_2.txt', PC1_ETH1_IP, PC2_ETH1_IP)  # 192.168.168.169, 12.12.1.169
        translated_id = get_icmp_identifer('/tmp/packets_v4_2.txt',Parameter.X1_IP, PC2_ETH1_IP)
        Assertion.assert_equal((src_id==translated_id), True, 'verify v4 icmp failed.')

    @repeat_method(3)
    def test_04_check_v6_fun(self):
        res = False
        fw_config_capture_monitor()
        pc1_login.send_command(f'ping6 -c 2 {PC2_ETH1_IPv6}')  # 2001::100
        time.sleep(10)
        packetapi.stop_capture()
        packetapi.export_captured_packets_pcapng(
            filepath='/tmp/packet-c_v6_2.pcapng')
        cmd = 'tshark -r /tmp/packet-c_v6_2.pcapng > /tmp/packets_v6_2.txt'
        pc1_login.send_command(cmd)
        src_id = get_icmp_identifer('/tmp/packets_v6_2.txt', PC1_ETH1_IPv6, PC2_ETH1_IPv6, 'ipv6')  # 2000::100, 2001::10
        translated_id = get_icmp_identifer('/tmp/packets_v6_2.txt', Parameter.X1_V6_IP, PC2_ETH1_IPv6, 'ipv6')  # 2001::168, 2001::100
        Assertion.assert_equal(src_id == translated_id, True, 'verify icmpv6 failed.')
