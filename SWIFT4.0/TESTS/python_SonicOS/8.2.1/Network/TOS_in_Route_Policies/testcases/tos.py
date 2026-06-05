from definition.settings import *
from definition.utils import *


# Boudry test for Tos/Mask
class TestTOS_TC01(Test):
    uuid = "SOSAIOT-TC-58755"
    description = show_testcase_info(
        TESTPLAN, '1506052', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1506052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_tos_route_with_invalid_tos(self):
        tos_list =['0', '24', 'ff', '100', '-1']
        tag_list = []
        for tos in tos_list:
            pbr_update = {
                "name": 'test_tos',
                "tos": tos,
                "mask": "0xff",
            }
            pbr_dict = copy.deepcopy(initial_pbr_dict)
            pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
            logger.info(f'new is:{pbr_dict}')
            (pbrres, msg) = routepolicyapi.add_route_policy(msg=True, **pbr_dict)
            logger.info(msg)
            tag_list.append(pbrres)
        Assertion.assert_equal(any(tag_list), False, "ERR: check add tos route with invalid tos failed")

    def test_03_add_tos_route_with_invalid_mask(self):
        mask_list = ['00', 'FF', '100', 'AB']
        tag_list = []
        for mask in mask_list:
            pbr_update = {
                "name": 'test_tos',
                "tos": '0x36',
                "mask": mask,
            }
            pbr_dict = copy.deepcopy(initial_pbr_dict)
            pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
            logger.info(f'new is:{pbr_dict}')
            (pbrres, msg) = routepolicyapi.add_route_policy(msg=True, **pbr_dict)
            logger.info(msg)
            tag_list.append(pbrres)
        Assertion.assert_equal(any(tag_list), False, "ERR: check add tos route with invalid mask failed")


# multiple policy routes with identical Source-IP, Destination-IP, and Service values, but differing TOS/TOS Mask values
class TestTOS_TC02(Test):
    uuid = "SOSAIOT-TC-58756"
    description = show_testcase_info(
        TESTPLAN, '1506053', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1506053')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_tos_route(self):
        pbr_update = {
            "name": 'tos_route',
            "interface": 'X2',
            "gateway": {
                "name": "X2 Default Gateway"
            },
            "destination": {
                "name": "ipv4_host"
            },
            "tos": "0x14",
            "mask": "0x36",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        (pbrres, msg) = routepolicyapi.add_route_policy(msg=True, **pbr_dict)
        if pbrres is False:
            pbrres = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(pbrres, True, "ERR: Add route policy failed")

    def test_03_send_traffic_with_tos_and_check_packet(self):
        fwport = 'X2'
        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        icmp_dict_x2 = copy.deepcopy(icmp_dict)
        icmp_dict_x2['IP']['src'] = '192.168.168.68/30'

        option_icmp_x2 = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmp',
            'icmp_dict': icmp_dict_x2,
            'tos': '0x14'
        }
        exportres = fw_packet_monitor_run(**option_icmp_x2)
        checkres = check_packets(exportres, expectpkt)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")


#  Add route policy with TOS field using CLI
class TestTOS_TC31(Test):
    uuid = "SOSAIOT-TC-58758"
    description = show_testcase_info(
        TESTPLAN, '1506055', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1506055')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 to static failed")

    def test_03_add_tos_route_by_cli(self):
        cli_rt_dict = {
            "version": "ipv4",
            "if": "X3",
            "metric": 10,
            "gateway": 'name "X3 Default Gateway"',
            "destination": 'name "ipv4_host"',
            "name": "cli_ipv4",
            "tos": "0x07",
            "mask": "0xff"
        }
        pbrres = routecli.add_route_policy(**cli_rt_dict)
        Assertion.assert_equal(pbrres, True, "ERR: Add route policy failed")

    def test_04_send_traffic_with_tos_and_check_packet(self):
        fwport = 'X3'
        icmp_dict_tc31 = copy.deepcopy(icmp_dict)
        icmp_dict_tc31['IP']['src'] = '192.168.168.56/30'
        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        option_icmp_x3 = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmp',
            'icmp_dict': icmp_dict_tc31,
            'tos': '0x07'
        }
        exportres = fw_packet_monitor_run(**option_icmp_x3)
        checkres = check_packets(exportres, expectpkt)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_05_edit_pbr_from_cli(self):
        cli_new_rt_dict = {
            "tos-new": "0x05"
        }
        rtres = routecli.edit_route_policy_by_name(
            version='ipv4', name='cli_ipv4', **cli_new_rt_dict)
        Assertion.assert_equal(rtres, True, "ERR:edit route policy failed")

    def test_06_send_traffic_with_tos_and_check_packet(self):
        fwport = 'X3'
        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        icmp_dict_tc31 = copy.deepcopy(icmp_dict)
        icmp_dict_tc31['IP']['src'] = '192.168.168.52/30'
        option_icmp = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmp',
            'icmp_dict': icmp_dict_tc31,
            'tos': '0x05'
        }
        exportres = fw_packet_monitor_run(**option_icmp)
        checkres = check_packets(exportres, expectpkt)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_07_edit_pbr_from_gui(self):
        pbr_update = {
            "interface": 'X3',
            "gateway": {
                "name": "X3 Default Gateway"
            },
            "destination": {
                "name": "ipv4_host"
            },
            "tos": "0x96",
            "mask": "0xf7",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        rtres = routepolicyapi.edit_route_policy(name='cli_ipv4', version ='v4', **pbr_dict)
        routepolicyapi.get_route_policy_by_name("cli_ipv4")
        Assertion.assert_equal(rtres, True, "ERR:edit route policy failed")

    def test_08_send_traffic_with_tos_and_check_packet(self):
        fwport = 'X3'
        icmp_dict_tc31 = copy.deepcopy(icmp_dict)
        icmp_dict_tc31['IP']['src'] = '192.168.168.48/30'
        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        option_icmp_x3 = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmp',
            'icmp_dict': icmp_dict_tc31,
            'tos': '0x96'
        }
        exportres = fw_packet_monitor_run(**option_icmp_x3)
        checkres = check_packets(exportres, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR:the traffic is not as expected")


# Add a IPv6 TOS route policy
class TestTOS_TC28(Test):
    uuid = "SOSAIOT-TC-58757"
    description = show_testcase_info(
        TESTPLAN, '1506054', description=True)['title']
    jira = "GEN7-48560"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1506054')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 to static failed")

    def test_03_cp_files(self):
        logger.info('cp send_icmpv6.py ...')
        PC4_Login.send_command('cp -rf {} /tmp/'.format(defi_path + 'scripts/send_icmpv6.py'))
        result = PC4_Login.send_command('ls /tmp/')
        output = True if 'send_icmpv6.py' in str(result) else False
        PC4_Login.send_command(f'route -A inet6 add {Parameter.IPV6_DST_HOST} gw {Parameter.X3_IPV6} dev eth1')
        Assertion.assert_equal(output, True, "ERR: copy failed")

    def test_04_add_ipv6_ao_and_tos_route(self):
        pbr_update = {
            "name": 'ipv6_tos_route',
            "interface": 'X2',
            "gateway": {
                "name": "X2_GW_IPV6"
            },
            "destination": {
                "name": "ipv6_host"
            },
            "tos": "0x14",
            "mask": "0x36",
        }
        pbr_dict = copy.deepcopy(initial_ipv6_rt_dict)
        pbr_dict["route_policies"][0]["ipv6"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        (pbrres, msg) = routepolicyapi.add_route_policy(msg=True, **pbr_dict)
        if pbrres is False:
            pbrres = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(pbrres, True, "ERR: Add route policy failed ")

    def test_05_send_traffic_with_tos_and_check_packet(self):
        fwport = 'X2'
        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        option_icmpv6 = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmpv6',
            'pc4obj': PC4_Login,
            'tos': 20
        }

        exportres = fw_packet_monitor_run(**option_icmpv6)
        checkres = check_packets(exportres, ipv6_expect_pkt_dict)
        Assertion.assert_equal(checkres, True, "ERR:the traffic is not as expected")


#  Add a router without TOS/mask set
class TestTOS_TC05(Test):
    uuid = "SOSAIOT-TC-58759"
    description = show_testcase_info(
        TESTPLAN, '1506056', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1506056')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_tos_route(self):
        pbr_update = {
            "name": 'standard_route',
            "interface": 'X1',
            "gateway": {
                "name": "X1 Default Gateway"
            },
            "destination": {
                "name": "ipv4_host"
            },
            "tos": "0x00",
            "mask": "0x00",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        (pbrres, msg) = routepolicyapi.add_route_policy(msg=True, **pbr_dict)
        if pbrres is False:
            pbrres = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(pbrres, True, "ERR: Add route policy failed ")

    def test_03_send_traffic_without_tos_and_check_packet(self):
        fwport = 'X1'
        icmp_dict_no_tos = copy.deepcopy(icmp_dict)
        icmp_dict_no_tos['IP']['src'] = '192.168.168.64/30'

        expectpkt = copy.deepcopy(expect_pkt_dict)
        expectpkt['out'] = fwport
        option_icmp_no_tos = {
            'packetobj': pkgmonitorapi,
            'pc1obj': PC1_Login,
            'protocol': 'icmp',
            'icmp_dict': icmp_dict_no_tos,
            'tos': '0x00'
        }
        exportres = fw_packet_monitor_run(**option_icmp_no_tos)
        checkres = check_packets(exportres, expectpkt)

        Assertion.assert_equal(checkres, True, "ERR:the traffic is not as expected")