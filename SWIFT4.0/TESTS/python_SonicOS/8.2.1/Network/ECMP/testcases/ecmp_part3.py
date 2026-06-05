from definition.settings_part3 import *
from definition.utils_part2 import *


# Function test: GUI: Add an IPv4 ECMP PBR with gateway number 4
class TestECMPBase_v4_TC003(Test):
    uuid = "SOSAIOT-TC-55945"
    description = show_testcase_info(
        TESTPLAN, '1510362', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510362')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_IPv4_ECMP_PBR_with_4_gw_different_interface(self):
        ecmp_4gw_api_rt_dict = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "ecmp_4gw_api",
                        "comment": "",
                        "interface": "X1",
                        "metric": 10,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "GW1_IP"
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
                            "name": "GW2_IP"
                        },
                        "interface3": "X3",
                        "gateway3": {
                            "name": "GW3_IP"
                        },
                        "interface4": "X4",
                        "gateway4": {
                            "name": "GW4_IP"
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
        rc = routeapi.add_route_policy(**ecmp_4gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login,icmp_dict, protocol='icmp')
        icmp_filter = ('Protocol: ICMP',
                       'Type: 8 (Echo (ping) request)',
                       'Forwarded',
                       f'Destination: {Parameter.SERVER_PC}',
                       )
        res1 = check_packet(exportres, icmp_filter, fwports)
        Assertion.assert_equal(res1, True, "ERR:  Check Packet fail")

    def test_04_delete_route(self):
        delres = routeapi.del_route_policy_by_name('ecmp_4gw_api')
        logger.info('del route result: {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:delete ecmp failed")


# Edit an IPv4 ECMP PBR in CLI with 4 gateways, different outgoing interface, added in CLI
class TestECMPBase_v4_TC153(Test):
    uuid = "SOSAIOT-TC-55962"
    description = show_testcase_info(
        TESTPLAN, '1510397', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510397')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv4_ecmp_pbr_from_cli(self):
        ecmp_cli_rt_dict = {
            "version": "ipv4",
            "if": "X1",
            "metric": 10,
            "gateway": 'name "GW1_IP"',
            "destination": 'name "server_network"',
            "name": "ecmp_cli_ipv4",
            "nexthop-number": 4,
            "interface2": "X2",
            "gateway2": 'name "GW2_IP"',
            "interface3": "X3",
            "gateway3": 'name "GW3_IP"',
            "interface4": "X4",
            "gateway4": 'name "GW4_IP"'
        }
        rtres = routecli.add_route_policy(**ecmp_cli_rt_dict)
        logger.info(f"add ipv6 ecmp routing : {rtres}\n ")
        res = routecli.get_route_uuid_by_name('ipv4', 'ecmp_cli_ipv4')
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR:ADD ecmp failed")

    def test_03_edit_ipv4_ecmp_pbr_from_cli(self):
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_cli_ipv6_new",
            "interface4-new": 'X5',
            "gateway4-new": 'name "GW5_IP"'
        }
        rtres = routecli.edit_route_policy_by_name(
            version='ipv4', name='ecmp_cli_ipv4', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rtres, True, "ERR:edit ecmp failed")

    def test_04_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X5']
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp_dict, protocol='icmp')
        icmp_filter = ('Protocol: ICMP',
                       'Type: 8 (Echo (ping) request)',
                       'Forwarded',
                       f'Destination: {Parameter.SERVER_PC}',
                       )
        res1 = check_packet(exportres, icmp_filter, fwports)
        Assertion.assert_equal(res1, True, "ERR:  Check Packet fail")


# Function test: IPv4 ECMP PBR with 4 gateways, same outgoing interface, physical interface
class TestECMPBase_v6_TC068(Test):
    uuid = "SOSAIOT-TC-55952"
    description = show_testcase_info(
        TESTPLAN, '1510371', description=True)['title']
    res_for_GUI_ipv6 = ContextVar('res_for_GUI_ipv6')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510371')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_IPv6_ECMP_PBR_with_4_gw_diff_interface(self):
        ecmp_ipv6_4gw_api_rt_dict = {
            "route_policies": [{
                "ipv6": {
                    "name": "ecmp_ipv6_4gw_api",
                    "comment": "",
                    "interface": "X1",
                    "metric": 10,
                    "service": {
                        "any": True
                    },
                    "gateway": {
                        "name": "GW1_IPV6"
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
                        "name": "GW2_IPV6"
                    },
                    "interface3": "X3",
                    "gateway3": {
                        "name": "GW3_IPV6"
                    },
                    "interface4": "X4",
                    "gateway4": {
                        "name": "GW4_IPV6"
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

        rc = routeapi.add_route_policy(**ecmp_ipv6_4gw_api_rt_dict)
        self.res_for_GUI_ipv6.set(rc)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmpv6200_dict = copy.deepcopy(icmpv6_dict)
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6200_dict, protocol='icmpv6')
        icmpv6_filter = ('Type: Echo (ping) request (128)',
                         f'Dst: {Parameter.SERVER_PC_V6}')
        res = check_packet(exportres, icmpv6_filter, fwports)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# GUI: Add an IPv6 ECMP PBR with gateway number 4
class TestECMPBase_v6_TC006(Test):
    uuid = "SOSAIOT-TC-55946"
    description = show_testcase_info(
        TESTPLAN, '1510363', description=True)['title']
    res_for_GUI_ipv6 = ContextVar('res_for_GUI_ipv6')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510363')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_verify_GUI(self):
        res = TestECMPBase_v6_TC068.res_for_GUI_ipv6.get()
        Assertion.assert_equal(
            res, True, "ERR: Add an IPv6 ECMP PBR with gateway number 4 from GUI fail")


# Function test: IPv6 ECMP PBR, src: range, dst: network, service: any, 4 gateways
class TestECMPBase_v6_TC078(Test):
    uuid = "SOSAIOT-TC-55953"
    description = show_testcase_info(
        TESTPLAN, '1510373', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510373')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_function_test(self):
        res = TestECMPBase_v6_CLI_TC171.res_for_TC1510373.get()
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Function test: IPv6 ECMP PBR, src: network, dst: network, service: any, 4 gateways
class TestECMPBase_v6_TC081(Test):
    uuid = "SOSAIOT-TC-55954"
    description = show_testcase_info(
        TESTPLAN, '1510374', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510374')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_function_test(self):
        res = TestECMPBase_v6_CLI_TC177.res_for_TC1510374.get()
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Function test: IPv6 ECMP PBR, src: any, dst: network, service: any, 4 gateways
class TestECMPBase_v6_TC088(Test):
    uuid = "SOSAIOT-TC-55955"
    description = show_testcase_info(
        TESTPLAN, '1510375', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510375')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_function_test(self):
        res = TestECMPBase_v6_CLI_TC165.res_for_TC1510375.get()
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Add an IPv6 ECMP PBR in CLI with 4 gateways, different outgoing interface
class TestECMPBase_v6_CLI_TC165(Test):
    uuid = "SOSAIOT-TC-55966"
    description = show_testcase_info(
        TESTPLAN, '1510401', description=True)['title']
    res_for_TC1510375 = ContextVar('res_for_TC1510375')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510401')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_ipv6_ecmp_pbr_from_cli(self):
        ecmp_cli_rt_dict = {
            "version": "ipv6",
            "if": "X1",
            "metric": 10,
            "gateway": 'name "GW1_IPV6"',
            "destination": 'name "ipv6_network_dst"',
            "name": "ecmp_cli_ipv6",
            "nexthop-number": 4,
            "interface2": "X2",
            "gateway2": 'name "GW2_IPV6"',
            "interface3": "X3",
            "gateway3": 'name "GW3_IPV6"',
            "interface4": "X4",
            "gateway4": 'name "GW4_IPV6"'
        }
        rtres = routecli.add_route_policy(**ecmp_cli_rt_dict)
        logger.info(f"add ipv6 ecmp routing : {rtres}\n ")
        res = routecli.get_route_uuid_by_name('ipv6', 'ecmp_cli_ipv6')
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR:ADD ecmp failed")

    def test_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmpv6200_dict = copy.deepcopy(icmpv6_dict)
        icmpv6200_dict['IPv6']['dst'] = '2001:1000::200'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6200_dict, protocol='icmpv6')
        icmpv6_filter = ('Type: Echo (ping) request (128)',
                         f'Dst: 2001:1000::200',
                         )
        res = check_packet(exportres, icmpv6_filter, fwports)
        self.res_for_TC1510375.set(res)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Edit an IPv6 ECMP PBR in CLI with 4 gateways, different outgoing interface, added in CLI
class TestECMPBase_v6_CLI_TC171(Test):
    uuid = "SOSAIOT-TC-55968"
    description = show_testcase_info(
        TESTPLAN, '1510403', description=True)['title']
    res_for_TC1510373 = ContextVar('res_for_TC1510373')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510403')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_ipv6_ecmp_pbr_from_cli(self):
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_cli_ipv6_new",
            "source-new": 'name "ipv6_range_source"',
        }
        rtres = routecli.edit_route_policy_by_name(
            version='ipv6', name='ecmp_cli_ipv6', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rtres, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmpv6300_dict = copy.deepcopy(icmpv6_dict)
        icmpv6300_dict['IPv6']['dst'] = '2001:1000::300'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6300_dict, protocol='icmpv6')
        icmp_filter = ('Type: Echo (ping) request (128)',
                       'Dst: 2001:1000::300'
                       )
        res = check_packet(exportres, icmp_filter, fwports)
        self.res_for_TC1510373.set(res)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Edit an IPv6 ECMP PBR in CLI with 4 gateways, different outgoing interface, added on GUI
class TestECMPBase_v6_CLI_TC177(Test):
    uuid = "SOSAIOT-TC-55970"
    description = show_testcase_info(
        TESTPLAN, '1510405', description=True)['title']
    res_for_TC1510374 = ContextVar('res_for_TC1510374')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510405')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_ipv6_ecmp_pbr_from_cli(self):
        ecmp_cli_new_rt_dict = {
            "name-new": "ecmp_ipv6_4gw_api_edit_by_cli",
            "source-new": 'name "ipv6_network_source"',
        }
        rc1 = routecli.edit_route_policy_by_name(
            version='ipv6', name='ecmp_ipv6_4gw_api', **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rc1, True, "ERR:edit ecmp failed")

    def test_03_send_icmp_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmpv6400_dict = copy.deepcopy(icmpv6_dict)
        icmpv6400_dict['IPv6']['dst'] = '2001:1000::400'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6400_dict, protocol='icmpv6')
        icmp_filter = ('Type: Echo (ping) request (128)',
                       'Dst: 2001:1000::400'
                       )
        res = check_packet(exportres, icmp_filter, fwports)
        self.res_for_TC1510374.set(res)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")


# Delete an IPv6 ECMP PBR in CLI, which is added on GUI
class TestECMPBase_v6_CLI_TC181(Test):
    uuid = "SOSAIOT-TC-55972"
    description = show_testcase_info(
        TESTPLAN, '1510407', description=True)['title']
    res_for_TC1510374 = ContextVar('res_for_TC1510374')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510404')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Delete_IPv6_ECMP_PBR_via_CLI(self):
        rc = routecli.del_route_policy_by_name(
            version='ipv6', name="ecmp_ipv6_4gw_api_edit_by_cli")
        Assertion.assert_equal(rc, True, "ERR:del ecmp failed")


# Prefs export
class TestECMPBase_exp_TC220(Test):
    uuid = "SOSAIOT-TC-55974"
    description = show_testcase_info(
        TESTPLAN, '1510414', description=True)['title']
    res_for_rtcount = ContextVar('res_for_rtcount')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510414')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_export_exp(self):
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_03_check_custom_route(self):
        res = routecli.show_route_policies('custom')
        rtcount = str(res).count('route-policy')
        logger.info(f'custom policies number is {rtcount}')
        self.res_for_rtcount.set(rtcount)
        Assertion.assert_equal(True, True, "ERR: export exp file failed")

    def test_04_check_exp_file(self):
        output = PC1_Login.send_command('ls -la /tmp')
        Assertion.assert_regular(
            str(output), 'test.exp', "ERR: check downloaded exp file failed")


# Prefs import
class TestECMPBase_exp_TC221(Test):
    uuid = "SOSAIOT-TC-55975"
    description = show_testcase_info(
        TESTPLAN, '1510415', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510415')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_import_exp(self):
        res = settingapi.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_03_check_custom_route(self):
        res = routecli.show_route_policies('custom')
        rtcount = str(res).count('route-policy')
        logger.info(f'custom policies number is {rtcount}')
        flag = True if rtcount == TestECMPBase_exp_TC220.res_for_rtcount.get() else False
        Assertion.assert_equal(
            flag, True, "ERR: check imported exp file failed")

    def test_04_send_v4_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X5']
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmp_dict, protocol='icmp')
        icmp_filter = ('Protocol: ICMP',
                       'Type: 8 (Echo (ping) request)',
                       'Forwarded',
                       f'Destination: {Parameter.SERVER_PC}',
                       )
        res1 = check_packet(exportres, icmp_filter, fwports)
        Assertion.assert_equal(res1, True, "ERR:  Check Packet fail")

    def test_05_send_icmp_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmpv6400_dict = copy.deepcopy(icmpv6_dict)
        icmpv6400_dict['IPv6']['dst'] = '2001:1000::400'
        exportres = fw_packet_monitor_run(pkgapi, PC1_Login, icmpv6400_dict, protocol='icmpv6')
        icmp_filter = ('Type: Echo (ping) request (128)',
                       'Dst: 2001:1000::400'
                       )
        res = check_packet(exportres, icmp_filter, fwports)
        Assertion.assert_equal(res, True, "ERR:  Check Packet fail")

