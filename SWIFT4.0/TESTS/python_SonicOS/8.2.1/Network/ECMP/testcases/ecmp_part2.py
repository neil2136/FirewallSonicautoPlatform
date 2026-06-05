from definition.settings_part2 import *
from definition.utils_part2 import *


# Function test: IPv4 ECMP PBR with 4 gateways, same outgoing interface,physical interface
class TestECMPBase_v4_TC038(Test):
    uuid = "SOSAIOT-TC-55947"
    description = show_testcase_info(
        TESTPLAN, '1510364', description=True)['title']
    res_for_icmp = ContextVar('res_for_icmp')
    mac_list = [Parameter.X2_GW1_MAC, Parameter.X2_GW2_MAC, Parameter.X2_GW3_MAC, Parameter.X2_GW4_MAC]

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510364')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_IPv4_ECMP_PBR_with_4_gw_same_interface(self):
        ecmp_1gw_api_rt_dict = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "ecmp_1gw_api",
                        "comment": "",
                        "interface": "X2",
                        "metric": 10,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X2_GW1_IP"
                        },
                        "nexthop_number": 4,
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "server_pc"
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "interface2": "X2",
                        "gateway2": {
                            "name": "X2_GW2_IP"
                        },
                        "interface3": "X2",
                        "gateway3": {
                            "name": "X2_GW3_IP"
                        },
                        "interface4": "X2",
                        "gateway4": {
                            "name": "X2_GW4_IP"
                        },
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "multi-path"
                    }
                }
            ]
        }

        rc = routeapi.add_route_policy(**ecmp_1gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp_dict, protocol='icmp')
        icmp_filter = ('Protocol: ICMP',
                       'Type: 8 (Echo (ping) request)',
                       'Forwarded',
                       f'Source: {Parameter.X2_IP}',
                       f'Destination: {Parameter.SERVER_PC}',
                       'out:X2')
        res1 = check_packet(exportres, icmp_filter, self.mac_list)
        icmp_filter = ('Protocol: ICMP',
                       'Type: 0 (Echo (ping) reply)',
                       f'Source: {Parameter.SERVER_PC}',
                       f'Destination: {Parameter.X2_IP}',
                       'in:X2')
        res2 = check_packet(exportres, icmp_filter, self.mac_list)
        self.res_for_icmp.set(res1 & res2)
        Assertion.assert_equal(res1 & res2, True, "ERR:  Check Packet fail")


# Function test when has 4 gateways,same outgoing interface, running TFTP/FTP/ICMP/http/https/ssh/telnet/UDP traffic
class TestECMPBase_v4_TC127(Test):
    uuid = "SOSAIOT-TC-55958"
    description = show_testcase_info(
        TESTPLAN, '1510389', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510389')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_send_udp_traffic_and_check_packet(self):
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, udp_dict, protocol='udp')
        udp_filter = (
            'Protocol: UDP',
            'Forwarded',
            f'Source: {Parameter.X2_IP}',
            f'Destination: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, udp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_03_send_tftp_traffic_and_check_packet(self):
        tftp_dict = copy.deepcopy(udp_dict)
        tftp_dict['UDP']['dport'] = '69'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, tftp_dict, protocol='udp')
        tftp_filter = (
            'Protocol: UDP',
            'Destination port: tftp (69)',
            'Forwarded',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, tftp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_04_send_ftp_traffic_and_check_packet(self):
        ftp_dict = copy.deepcopy(tcp_dict)
        ftp_dict['TCP']['dport'] = '21'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, ftp_dict, protocol='tcp')
        ftp_filter = (
            'Protocol: TCP (6)',
            'Forwarded',
            'Destination port: ftp (21)',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, ftp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_05_send_ssh_traffic_and_check_packet(self):
        ssh_dict = copy.deepcopy(tcp_dict)
        ssh_dict['TCP']['dport'] = '22'
        exportres = fw_packet_monitor_run(pkgapi,  PC1_Login, ssh_dict, protocol='tcp')
        ssh_filter = (
            'Protocol: TCP (6)',
            'Forwarded',
            'Destination port: ssh (22)',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, ssh_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_06_send_telnet_traffic_and_check_packet(self):
        telnet_dict = copy.deepcopy(tcp_dict)
        telnet_dict['TCP']['dport'] = '23'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, telnet_dict, protocol='tcp')
        telnet_filter = (
            'Protocol: TCP (6)',
            'Forwarded',
            'Destination port: telnet (23)',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, telnet_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_07_send_http_traffic_and_check_packet(self):
        http_dict = copy.deepcopy(tcp_dict)
        http_dict['TCP']['dport'] = '80'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, http_dict, protocol='tcp')
        http_filter = (
            'Protocol: TCP (6)',
            'Forwarded',
            'Destination port: http (80)',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, http_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    def test_08_send_https_traffic_and_check_packet(self):
        https_dict = copy.deepcopy(tcp_dict)
        https_dict['TCP']['dport'] = '443'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, https_dict, protocol='tcp')
        https_filter = (
            'Protocol: TCP (6)',
            'Forwarded',
            'Destination port: https (443)',
            f'Source: {Parameter.X2_IP}',
            f'Dst: {Parameter.SERVER_PC}',
            'out:X2')
        res = check_packet(exportres, https_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

    # which verify in TCTC038
    def test_09_send_icmp_traffic_and_check_packet(self):
        res = TestECMPBase_v4_TC038.res_for_icmp.get()
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Add an IPv4 ECMP PBR in CLI with 4 gateways, same outgoing interface
class TestECMPBase_v4_CLI_TC144(Test):
    uuid = "SOSAIOT-TC-55959"
    description = show_testcase_info(
        TESTPLAN, '1510394', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510364')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv4_ecmp_pbr_from_cli(self):
        dst_range_ao_dict = {
            "object_type": "range",
            "name": "dst_range",
            "zone": "LAN",
            "value": "100.100.10.161,100.100.10.191"
        }
        aorc = aoapi.config_addressobject(**dst_range_ao_dict)
        logger.info(f"add dst range ao : {aorc}\n ")
        ecmp_cli_rt_dict = {
            "version": "ipv4",
            "if": "X2",
            "metric": 10,
            "gateway": 'name "X2_GW1_IP"',
            "destination": 'name "dst_range"',
            "name": "ecmp_cli",
            "nexthop-number": 4,
            "interface2": "X2",
            "gateway2": 'name "X2_GW2_IP"',
            "interface3": "X2",
            "gateway3": 'name "X2_GW3_IP"',
            "interface4": "X2",
            "gateway4": 'name "X2_GW4_IP"'
        }
        rc = routecli.add_route_policy(**ecmp_cli_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        icmp180_dict = copy.deepcopy(icmp_dict)
        icmp180_dict['IP']['dst'] = '100.100.10.180'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp180_dict, protocol='icmp')
        # mark -- ip ???
        icmp_filter = (
            'icmp',
            f'Dst: 100.100.10.180',
            'out:X2')
        res = check_packet(exportres, icmp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


 # Edit an IPv4 ECMP PBR in CLI with 4 gateways, same outgoing interface, added in CLI
class TestECMPBase_v4_CLI_TC150(Test):
    uuid = "SOSAIOT-TC-55961"
    description = show_testcase_info(
        TESTPLAN, '1510396', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510396')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Edit_IPv4_ECMP_PBR_via_CLI(self):
        dst_range_ao_new_dict = {
            "object_type": "range",
            "name": "dst_range_new",
            "zone": "LAN",
            "value": "100.100.10.100,100.100.10.120"
        }
        aorc = aoapi.config_addressobject(**dst_range_ao_new_dict)
        logger.info(f"add new dst range ao : {aorc}\n ")
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_cli_new",
            "destination-new": 'name "dst_range_new"',
        }
        rc = routecli.edit_route_policy_by_name(
            version='ipv4', name='ecmp_cli', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        icmp110_dict = copy.deepcopy(icmp_dict)
        icmp110_dict['IP']['dst'] = '100.100.10.110'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp110_dict, protocol='icmp')
        icmp_filter = (
            'icmp',
            f'Dst: 100.100.10.110',
            'out:X2')
        res = check_packet(exportres, icmp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Edit an IPv4 ECMP PBR in CLI with 4 gateways, same outgoing interface,added on GUI
class TestECMPBase_v4_CLI_TC156(Test):
    uuid = "SOSAIOT-TC-55963"
    description = show_testcase_info(
        TESTPLAN, '1510398', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510398')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Edit_IPv4_ECMP_PBR_via_CLI(self):
        dst_range_ao_new_dict = {
            "object_type": "range",
            "name": "ecmp_1gw_edit_by_cli",
            "zone": "LAN",
            "value": "100.100.10.121,100.100.10.139"
        }
        aorc = aoapi.config_addressobject(**dst_range_ao_new_dict)
        logger.info(f"add new dst range ao : {aorc}\n ")
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_1gw_api_edit_by_cli",
            "destination-new": 'name "ecmp_1gw_edit_by_cli"',
        }
        rc = routecli.edit_route_policy_by_name(
            version='ipv4', name='ecmp_1gw_api', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        icmp128_dict = copy.deepcopy(icmp_dict)
        icmp128_dict['IP']['dst'] = '100.100.10.128'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp128_dict, protocol='icmp')
        icmp_filter = (
            'icmp',
            f'Dst: 100.100.10.128',
            'out:X2')
        res = check_packet(exportres, icmp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Function test: IPv6 ECMP PBR with 4 gateways, same outgoing interface, physical interface
class TestECMPBase_v6_TC067(Test):
    uuid = "SOSAIOT-TC-55951"
    description = show_testcase_info(
        TESTPLAN, '1510370', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510370')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_IPv6_ECMP_PBR_with_the_same_interface(self):
        ecmp_1gw_api_rt_dict = {
            "route_policies": [{
                "ipv6": {
                    "name": "ecmp_ipv6_1gw_api",
                    "comment": "",
                    "interface": "X2",
                    "metric": 10,
                    "service": {
                        "any": True
                    },
                    "gateway": {
                        "name": "X2_GW1_IPV6"
                    },
                    "nexthop_number": 4,
                    "source": {
                        "any": True
                    },
                    "destination": {
                        "name": "server_pc_v6"
                    },
                    "disable_on_interface_down": True,
                    "vpn_precedence": False,
                    "probe": "",
                    "interface2": "X2",
                    "gateway2": {
                        "name": "X2_GW2_IPV6"
                    },
                    "interface3": "X2",
                    "gateway3": {
                        "name": "X2_GW3_IPV6"
                    },
                    "interface4": "X2",
                    "gateway4": {
                        "name": "X2_GW4_IPV6"
                    },
                    "distance": {
                        "auto": True
                    },
                    "tos": "0x00",
                    "mask": "0x00",
                    "type": "multi-path"
                }
            }]
        }

        rc = routeapi.add_route_policy(**ecmp_1gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6_dict, protocol='icmpv6')
        icmpv6_filter = ('Type: Echo (ping) request (128)',
                         f'Dst: {Parameter.SERVER_PC_V6}',
                         'out:X2')
        res = check_packet(exportres, icmpv6_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Add an IPv6 ECMP PBR in CLI with 4 gateways, same outgoing interface
class TestECMPBase_v6_CLI_TC162(Test):
    uuid = "SOSAIOT-TC-55965"
    description = show_testcase_info(
        TESTPLAN, '1510400', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510400')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv6_ecmp_pbr_from_cli(self):
        ipv6_range_ao_dict = {
            "object_type": "range",
            "name": "ipv6_range",
            "zone": "LAN",
            "begin": "2001:1000:1000:1000::200",
            "end": "2001:1000:1000:1000::299"
        }
        aores = aoapi.config_ipv6_addressobject(**ipv6_range_ao_dict)
        logger.info(f"add ipv6 range ao : {aores}\n ")

        ecmp_cli_rt_dict = {
            "version": "ipv6",
            "if": "X2",
            "metric": 10,
            "gateway": 'name "X2_GW1_IPV6"',
            "destination": 'name "ipv6_range"',
            "name": "ecmp_cli_ipv6",
            "nexthop-number": 4,
            "interface2": "X2",
            "gateway2": 'name "X2_GW2_IPV6"',
            "interface3": "X2",
            "gateway3": 'name "X2_GW3_IPV6"',
            "interface4": "X2",
            "gateway4": 'name "X2_GW4_IPV6"'
        }
        rtres = routecli.add_route_policy(**ecmp_cli_rt_dict)
        logger.info(f"add ipv6 ecmp routing : {rtres}\n ")
        res = routecli.get_route_uuid_by_name('ipv6', 'ecmp_cli_ipv6')
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        icmpv6200_dict = copy.deepcopy(icmpv6_dict)
        icmpv6200_dict['IPv6']['dst'] = '2001:1000:1000:1000::200'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6200_dict, protocol='icmpv6')
        icmpv6_filter = ('Type: Echo (ping) request (128)',
                         f'Dst: 2001:1000:1000:1000::200',
                         'out:X2')
        res = check_packet(exportres, icmpv6_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Edit an IPv6 ECMP PBR in CLI with 4 gateways, same outgoing interface, added in CLI
class TestECMPBase_v6_CLI_TC168(Test):
    uuid = "SOSAIOT-TC-55967"
    description = show_testcase_info(
        TESTPLAN, '1510402', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510402')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv6_ecmp_pbr_from_cli(self):
        ipv6_range_new_ao_dict = {
            "object_type": "range",
            "name": "ipv6_range_new",
            "zone": "LAN",
            "begin": "2001:1000:1000:1000::300",
            "end": "2001:1000:1000:1000::399"
        }
        aores = aoapi.config_ipv6_addressobject(**ipv6_range_new_ao_dict)
        logger.info(f"add ipv6 range ao : {aores}\n ")
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_cli_ipv6_new",
            "destination-new": 'name "ipv6_range_new"',
        }
        rtres = routecli.edit_route_policy_by_name(
            version='ipv6', name='ecmp_cli_ipv6', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rtres, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        icmpv6300_dict = copy.deepcopy(icmpv6_dict)
        icmpv6300_dict['IPv6']['dst'] = '2001:1000:1000:1000::300'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6300_dict, protocol='icmpv6')
        icmp_filter = ('Type: Echo (ping) request (128)',
                       f'Dst: 2001:1000:1000:1000::300',
                       'out:X2')
        res = check_packet(exportres, icmp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Edit an IPv6 ECMP PBR in CLI with 4 gateways, same outgoing interface, added on GUI
class TestECMPBase_v6_CLI_TC174(Test):
    uuid = "SOSAIOT-TC-55969"
    description = show_testcase_info(
        TESTPLAN, '1510404', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510404')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv6_ecmp_pbr_from_cli(self):
        ipv6_range_new_ao_dict = {
            "object_type": "range",
            "name": "ipv6_range_edit_by_cli",
            "zone": "LAN",
            "begin": "2001:1000:1000:1000::400",
            "end": "2001:1000:1000:1000::499"
        }
        rc = aoapi.config_ipv6_addressobject(**ipv6_range_new_ao_dict)
        logger.info(f"add ipv6 range ao : {rc}\n ")
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_ipv6_1gw_api_edit_by_cli",
            "destination-new": 'name "ipv6_range_edit_by_cli"',
        }
        rc1 = routecli.edit_route_policy_by_name(
            version='ipv6', name='ecmp_ipv6_1gw_api', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rc1, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        icmpv6400_dict = copy.deepcopy(icmpv6_dict)
        icmpv6400_dict['IPv6']['dst'] = '2001:1000:1000:1000::400'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6400_dict, protocol='icmpv6')
        icmp_filter = ('Type: Echo (ping) request (128)',
                       f'Dst: 2001:1000:1000:1000::400',
                       'out:X2')
        res = check_packet(exportres, icmp_filter, TestECMPBase_v4_TC038.mac_list)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")