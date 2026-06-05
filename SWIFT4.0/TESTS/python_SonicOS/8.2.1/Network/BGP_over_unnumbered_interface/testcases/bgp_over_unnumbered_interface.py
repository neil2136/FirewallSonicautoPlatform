import json
import re
import ipaddress

from csv import DictReader
from io import StringIO
from definition.settings import *
from definition.utils import *


# Expected:ibgp over unnumbered vpn works well
class TestTC01_ibgp_over_unnumbered_vpn_can_established(Test):
    uuid = "SOSAIOT-TC-55814"
    description = show_testcase_info(TESTPLAN, 'tc01', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_bgp_on_local_dut(self):
        opt = {
            'advanced': True,
            'BGP': True
        }
        res1 = dynamicroutingapi.set_BGP(**opt)
        res2 = r_dynamicroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res1 & res2, True, "ERR: enable BGP failed")

    def test_03_configure_bgp_in_cli_on_local_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.X0_REMOTE_IP} remote-as 10',
                f'neighbor {Parameter.X0_REMOTE_IP} update-source {Parameter.X0_IP}',
                ]
        res, confoutput = routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on local dut failed")

    def test_04_configure_bgp_in_cli_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.X0_IP} remote-as 10',
                f'neighbor {Parameter.X0_IP} update-source {Parameter.X0_REMOTE_IP}'
                ]
        res, confoutput = r_routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on remote dut failed")

    def test_05_add_static_route_with_tunnel_interface_on_local_dut(self):
        res = routepolicyapi.add_route_policy(**pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True,
                               "ERR: add static route based VPN on unnumbered interface on local dut failed")

    def test_06_add_static_route_with_tunnel_interface_on_remote_dut(self):
        r_pbr_dict = copy.deepcopy(pbr_dict)
        r_pbr_dict["route_policies"][0]["ipv4"]["interface"] = Parameter.REMOTE_VPN_NAME
        res = r_routepolicyapi.add_route_policy(**r_pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True,
                               "ERR: add static route based VPN on unnumbered interface on remote dut failed")

    @repeat_method(3)
    def test_07_check_bgp_summary_window(self):
        time.sleep(50)
        bgpoutput = dynamicroutingapi.get_bgp_summary()
        logger.info(f'bgp summay output is :{bgpoutput}')
        bgpoutput_new = str(bgpoutput).replace('&nbsp;', ' ')
        logger.info(f'bgpoutput_new is :{bgpoutput_new}')
        checklist = [f'neighbor is {Parameter.X0_REMOTE_IP}', 'BGP state = Established']
        checkres = [i in bgpoutput_new for i in checklist]
        logger.info(f'checkres is :{checkres}')
        ParamCases.TC01test07 = all(checkres)
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp summary window info failed")


# Expected: ebgp over unnumbered vpn works well
class TestTC02_ebgp_over_unnumbered_vpn_can_established(Test):
    uuid = "SOSAIOT-TC-55815"
    description = show_testcase_info(TESTPLAN, 'tc02', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_router_bgp_process_on_remote_dut(self):
        res, output = r_routecli.delete_router_bgp('10')
        Assertion.assert_equal(res, True, "ERR: delete router bgp process on remote dut failed")

    def test_03_configure_bgp_in_cli_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.X0_IP} remote-as 10',
                f'neighbor {Parameter.X0_IP} ebgp-multihop 255',
                f'neighbor {Parameter.X0_IP} update-source {Parameter.X0_REMOTE_IP}'
                ]
        res, confoutput = r_routecli.config_router_bgp(cmds, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on remote dut failed")

    def test_04_modify_router_bgp_settings_on_local_dut(self):
        logger.info(" {} ".center(20, '-').format('modify Local Settings for BGP'))
        cmds = [f'no neighbor {Parameter.X0_REMOTE_IP} remote-as 10',
                f'neighbor {Parameter.X0_REMOTE_IP} remote-as 20',
                f'neighbor {Parameter.X0_REMOTE_IP} ebgp-multihop 255',
                f'neighbor {Parameter.X0_REMOTE_IP} update-source {Parameter.X0_IP}'
                ]
        res, confoutput = routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds.pop(0)]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: modify bgp settings in cli on local dut failed")

    @repeat_method(2)
    def test_05_check_bgp_neighbor(self):
        time.sleep(20)
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        Assertion.assert_regular(showoutput, 'Established', "ERR: check bgp summary window info failed")


# Expected:BGP establishes session on unnumbered interface and can learn route from peer
class TestTC03_verify_route_for_advertised_network_prefix_is_added_in_gui_and_nsm(Test):
    uuid = "SOSAIOT-TC-55816"
    description = show_testcase_info(TESTPLAN, 'tc03', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_advertise_network_prefix_on_remote_dut(self):
        cmd = f'network {Parameter.NETWORKPREFIX_1}/24'
        res, confoutput = r_routecli.config_router_bgp(cmd, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'network {Parameter.NETWORKPREFIX_1}' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: advertise network prefix on remote dut failed")

    @repeat_method(2)
    def test_03_check_learned_bgp_routes_through_unnumbered_vpn_in_route_policy_table_of_gui(self):
        time.sleep(40)
        check_dict = {
            'gw': Parameter.R_TI_IP,
            'd_protocol': 'ebgp',
            'interface': Parameter.LOCAL_VPN_NAME,
            'route': [f'{Parameter.NETWORKPREFIX_1}/24']
        }
        reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
        logger.info(f'reslist is :{reslist}')
        is_valid = bool(reslist) and all(reslist)
        Assertion.assert_equal(is_valid, True, "ERR: check rip routes learned via tunnel interface failed")

    def test_04_check_learned_bgp_route_in_cli_of_nsm(self):
        flag = False
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        if 'Established' in showoutput:
            output = routecli.show_nsm_database()
            logger.info(f'output is:{output}')
            if f"B    *> {Parameter.NETWORKPREFIX_1}/24 [20/0] via {Parameter.X0_REMOTE_IP}" in output:
                flag = True
        else:
            logger.info(f"bgp doesn't establish up")
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via unnumbered vpn in cli failed")


# Expected:ZebOS commands "show ip BGP ipv4 unicast"  can display routing information
class TestTC04_check_routing_information_by_zebos_command(Test):
    uuid = "SOSAIOT-TC-55817"
    description = show_testcase_info(TESTPLAN, 'tc04', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_routing_information_by_zebos_command(self):
        res, showoutput = routecli.show_in_routing_bgp('show  ip bgp ipv4 unicast')
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'*> {Parameter.NETWORKPREFIX_1}/24' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: check routing information by zebos command failed")


# Expected:The show BGP Summary popup window can show BGP Status Summary,neighbor info about established connection.
class TestTC05_check_bgp_summary_on_gui(Test):
    uuid = "SOSAIOT-TC-55818"
    description = show_testcase_info(TESTPLAN, 'tc05', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(2)
    def test_02_check_bgp_summary_window(self):
        time.sleep(20)
        bgpoutput = dynamicroutingapi.get_bgp_summary()
        logger.info(f'bgp summay output is :{bgpoutput}')
        bgpoutput_new = str(bgpoutput).replace('&nbsp;', ' ')
        logger.info(f'bgpoutput_new is :{bgpoutput_new}')
        checklist = [f'neighbor is {Parameter.X0_REMOTE_IP}', 'BGP state = Established']
        checkres = [i in bgpoutput_new for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp summary window info failed")


# Expected:traffic between DUT and the network prefix advertised by BGP over unnumbered interface is reachable
class TestTC08_verify_traffic_between_dut_and_network_learned_from_bgp_over_unnumbered_interface(Test):
    uuid = "SOSAIOT-TC-55819"
    description = show_testcase_info(TESTPLAN, 'tc08', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_redistribute_connected_on_remote_dut(self):
        cmd = [f'no network {Parameter.NETWORKPREFIX_1}/24', 'redistribute connected']
        res, confoutput = r_routecli.config_router_bgp(cmd, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'network {Parameter.NETWORKPREFIX_1}' not in showoutput and 'redistribute connected' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: redistribute connected on remote dut failed")

    def test_03_redistribute_connected_on_local_dut(self):
        res, confoutput = routecli.config_router_bgp('redistribute connected', '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if 'redistribute connected' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: redistribute connected on local dut failed")

    def test_04_add_allow_access_rule_from_lan_x3_subnet_to_vpn_remote_x3_subnet_on_local_dut(self):
        res = accessruleapi.add_accessrule(**accessrule_dict)
        Assertion.assert_equal(res, True, "ERR: add lan to vpn access rule on local dut failed")

    def test_05_add_allow_access_rule_from_vpn_remote_x3_subnet_to_lan_x3_subnet_on_local_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["from"] = "VPN"
        rule_dict["access_rules"][0]["ipv4"]["to"] = "LAN"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "l_vpn_to_lan"
        rule_dict["access_rules"][0]["ipv4"]["source"]["address"] = {"name": "remote_x3_subnet"}
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "X3 Subnet"}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on local dut failed")

    def test_06_add_allow_access_rule_from_vpn_remote_x3_subnet_to_lan_x3_subnet_on_remote_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["from"] = "VPN"
        rule_dict["access_rules"][0]["ipv4"]["to"] = "LAN"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "r_vpn_to_lan"
        rule_dict["access_rules"][0]["ipv4"]["source"]["address"] = {"name": "remote_x3_subnet"}
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "X3 Subnet"}
        res = r_accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on remote dut failed")

    def test_07_add_allow_access_rule_from_lan_x3_subnet_to_vpn_remote_x3_subnet_on_remote_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["name"] = "r_lan_to_vpn"
        res = r_accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add lan to vpn access rule on remote dut failed")

    @repeat_method(2)
    def test_08_verify_icmp_traffic_between_local_x2_subnet_and_remote_x2_subnet(self):
        time.sleep(20)
        res1 = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        res2 = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'res1 is {res1},res2 is :{res2}')
        if "100% packet loss" not in res1 and "100% packet loss" not in res2:
            flag = True
        else:
            flag = False
            logger.info('traffic failed,check routing table on local and remote dut........')
            routecli.show_nsm_database()
            r_routecli.show_nsm_database()
            PC2_Login.send_command('ip -4 r')
            PC3_Login.send_command('ip -4 r')
        Assertion.assert_equal(flag, True, "ERR: traffic between local x3 subnet and remote x3 subnet failed")


# Expected:connected networks can be advertised via BGP over unnumbered tunnel interface
class TestTC13_verify_connected_networks_can_be_advertised_via_bgp_over_unnumbered_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-55821"
    description = show_testcase_info(TESTPLAN, 'tc13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_routes_on_local_dut_after_connected_networks_advertised_via_bgp_over_unnumbered_tunnel_interface(
            self):
        checklist = [f'*> {Parameter.X3_REMOTE_NET}',
                     f'*> {Parameter.X4_REMOTE_NET}',
                     ]
        resoutput = routecli.show_BGP(mode='unicast')
        reslist = [i in resoutput for i in checklist]
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: check routing table on local dut failed")

    def test_03_check_routes_on_remote_dut_after_connected_networks_advertised_via_bgp_over_unnumbered_tunnel_interface(
            self):
        checklist = [f'*> {Parameter.X3_SUBNET}',
                     f'*> {Parameter.X4_SUBNET}',
                     ]
        resoutput = r_routecli.show_BGP(mode='unicast')
        reslist = [i in resoutput for i in checklist]
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: check routing table on remote dut failed")


# Expected:static networks can be advertised via BGP over unnumbered tunnel interface
class TestTC11_verify_static_networks_can_be_advertised_via_bgp_over_unnumbered_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-55820"
    description = show_testcase_info(TESTPLAN, 'tc11', description=True)['title']
    dest_network = '100.1.1.0'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_static_route_on_remote_dut(self):
        dest_network = {
            'name': self.dest_network,
            'zone': 'WAN',
            'object_type': 'network',
            'value': f'{self.dest_network},{Parameter.MASK}',
        }
        res1 = r_addressobjectsapi.config_addressobject(**dest_network)
        res2 = r_routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: add static route on remote dut failed")

    def test_03_redistribute_static_route_on_remote_dut(self):
        cmd = ['no redistribute connected', 'redistribute static']
        res, confoutput = r_routecli.config_router_bgp(cmd, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if 'redistribute static' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: redistribute static route on remote dut failed")

    def test_04_redistribute_static_on_local_dut(self):
        cmds = ['no redistribute connected', 'redistribute static']
        res, confoutput = routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if 'redistribute static' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: redistribute static route on remote dut failed")

    def test_05_check_learned_bgp_routes_through_unnumbered_vpn_in_route_policy_table_of_gui(self):
        time.sleep(20)
        droutoutput = routepolicyapi.get_dynamic_route_policy()
        logger.info(f'drouteoutput is:{droutoutput}')
        time.sleep(20)
        check_dict = {
            'gw': Parameter.R_TI_IP,
            'd_protocol': 'ebgp',
            'interface': Parameter.LOCAL_VPN_NAME,
            'route': [f'{self.dest_network}/24']
        }
        reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
        logger.info(f'reslist is :{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: check bgp routes learned via tunnel interface failed")

    @repeat_method(2)
    def test_06_check_learned_bgp_route_in_cli_of_nsm(self):
        time.sleep(20)
        flag = False
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        if 'Established' in showoutput:
            output = routecli.show_nsm_database()
            logger.info(f'output is:{output}')
            if f"B    *> {self.dest_network}/24 [20/20] via {Parameter.X0_REMOTE_IP}" in output:
                flag = True
        else:
            logger.info(f"bgp doesn't establish up")
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via unnumbered vpn in cli failed")

    def test_07_add_learned_route_ao_on_local_dut(self):
        remote_x0_subnet = {
            'name': '100.1.1.0',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{self.dest_network},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x0_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    def test_08_add_allow_access_rule_from_lan_x3_subnet_to_learned_subnet_on_local_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["name"] = "l_lan_to_vpn_100_1_1_0"
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "100.1.1.0"}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on local dut failed")

    def test_09_send_traffic_to_learned_bgp_route_and_check_if_hit_the_route_policy(self):
        flag = False
        # get hit time in tsr before send traffic
        tsrrouting = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        hittimebefore = get_dynamic_route_hit_time_in_tsr(tsrrouting, self.dest_network)
        logger.info(f'hittimebefore is :{hittimebefore}')
        PC2_Login.send_command(f'ping -I eth1 -c 5 100.1.1.100')
        # get hit time in tsr after send traffic
        tsrrouting_1 = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        hittimeafter = get_dynamic_route_hit_time_in_tsr(tsrrouting_1, self.dest_network)
        logger.info(f'hittimeafter is {hittimeafter}')
        logger.info(f'hittimebefore is {hittimebefore}')
        if hittimeafter != hittimebefore:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check hit bgp route over unnumbered tunnel interface failed")

    def test_10_delete_static_route_on_remote_dut(self):
        res = r_routepolicyapi.del_route_policy_by_name(self.dest_network, version='v4')
        Assertion.assert_equal(res, True, "ERR: delete static route on remote dut failed")

    @repeat_method(2)
    def test_11_check_learned_bgp_route_in_cli_of_nsm_after_delete_static_route_on_remote_dut(self):
        time.sleep(20)
        flag = False
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        if 'Established' in showoutput:
            output = routecli.show_nsm_database()
            logger.info(f'output is:{output}')
            if f"B    *> {self.dest_network}/24 [20/20] via {Parameter.X0_REMOTE_IP}" not in output:
                flag = True
        else:
            logger.info(f"bgp doesn't establish up")
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via unnumbered vpn in cli failed")

    def test_12_check_learned_bgp_routes_through_unnumbered_vpn_in_route_policy_table_of_gui_after_delete_static_route_on_remote_dut(
            self):
        time.sleep(20)
        check_dict = {
            'gw': Parameter.R_TI_IP,
            'd_protocol': 'ebgp',
            'interface': Parameter.LOCAL_VPN_NAME,
            'route': [f'{self.dest_network}/24']
        }
        reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
        logger.info(f'reslist is :{reslist}')
        flag = True if (reslist.count(False) == 4 or len(reslist) == 0) else False
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via tunnel interface failed")

    def test_13_no_redistribute_static_on_local_and_remote_dut(self):
        res1, confoutput1 = routecli.config_router_bgp('no redistribute static', '10')
        res2, confoutput2 = r_routecli.config_router_bgp('no redistribute static', '20')
        Assertion.assert_equal(res1 & res2, True, "ERR: no redistribute static on local and remote dut failed")


# Expected: it can redistribute ospf routes via BGP over unnumbered tunnel interface
class TestTC15_verify_redistribute_ospf_routes_via_bgp_over_unnumbered_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-55822"
    description = show_testcase_info(TESTPLAN, 'tc15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_ospf_remote_dut_x3(self):
        default_ospf2 = {
            'interface': 'X3',
            'mode': 'enable',
            'dead_interval': '40',
            'hello_interval': '10',
            'auth': 'disable',
            'area': '0',
            'area_type': 'normal',
            'auto': 'on',
            'priority': '1',
            'mtu': 'off',
        }
        res = r_dynamicroutingapi.set_ospf2(**default_ospf2)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: Failed to enable ospf")

    @repeat_method(3)
    def test_03_check_learned_ospf_route_from_pc4_on_remote_dut(self):
        time.sleep(30)
        is_valid = False
        ospfstatus_dict = {'interface': 'X3',
                           }
        ospfnboutput = r_dynamicroutingapi.get_interface_ospfv2_status(**ospfstatus_dict)
        logger.info(f'ospfnboutput is :{ospfnboutput}')
        if 'Full' in str(ospfnboutput):
            time.sleep(20)
            check_dict = {
                'gw': '172.17.1.50',
                'd_protocol': 'ospfv2',
                'interface': 'X3',
                'route': [f'{Parameter.LEARNEDROUTE}/24']
            }
            reslist = check_droute_learned_from_ti_in_route_policy(r_routepolicyapi, **check_dict)
            logger.info(f'reslist is :{reslist}')
            # check if reslist is not empty list and is all True value
            is_valid = bool(reslist) and all(reslist)
        else:
            logger.info(f'******** ospf neighbor is down,please check.......')
        Assertion.assert_equal(is_valid, True, "ERR: check ospf routes learned from PC4 on remote dut failed")

    def test_04_redistribute_ospf_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmd = 'redistribute ospf'
        res, confoutput = r_routecli.config_router_bgp(cmd, '20')
        logger.info(f'res is :{res},confoutput is :{confoutput}')
        Assertion.assert_equal(res, True, "ERR: redistribute ospf on remote dut failed")

    @repeat_method(2)
    def test_05_check_bgp_routes_in_route_policy_table_of_gui_on_local_dut(self):
        time.sleep(20)
        check_dict = {
            'd_protocol': 'ebgp',
            'interface': 'none',
            'route': [f'{Parameter.LEARNEDROUTE}/24']
        }
        reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
        is_valid = bool(reslist) and all(reslist)
        logger.info(f'reslist is :{reslist}')
        Assertion.assert_equal(is_valid, True, "ERR: check bgp routes learned from remote on local dut failed")

    def test_06_check_learned_bgp_route_in_cli_of_nsm_on_local_dut(self):
        output = routecli.show_nsm_database()
        logger.info(f'output is:{output}')
        flag = True if f"B    *> {Parameter.LEARNEDROUTE}/24 [20/20] via {Parameter.X0_REMOTE_IP}" in output else False
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via unnumbered vpn in cli failed")

    def test_07_check_routing_information_by_zebos_command(self):
        res, showoutput = routecli.show_in_routing_bgp('show  ip bgp ipv4 unicast')
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'*> {Parameter.LEARNEDROUTE}/24' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: check routing information by zebos command failed")


# Expected:it can advertise a route via Network command over unnumbered tunnel interface
class TestTC19_verify_advertise_route_via_network_command_over_unnumbered_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-55823"
    description = show_testcase_info(TESTPLAN, 'tc19', description=True)['title']
    lnetworkprefix = '193.1.1.0'
    rnetworkprefix = '173.1.1.0'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_advertise_route_via_network_command_on_local_dut(self):
        cmd = f'network {self.lnetworkprefix}/24'
        res, confoutput = routecli.config_router_bgp(cmd, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'network {self.lnetworkprefix}' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: advertise network prefix on remote dut failed")

    def test_03_advertise_route_via_network_command_on_remote_dut(self):
        cmd = f'network {self.rnetworkprefix}/24'
        res, confoutput = r_routecli.config_router_bgp(cmd, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'network {self.rnetworkprefix}' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: advertise network prefix on remote dut failed")

    def test_04_check_routing_information_by_zebos_command_on_local_dut(self):
        time.sleep(20)
        res, showoutput = routecli.show_in_routing_bgp('show  ip bgp ipv4 unicast')
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'*> {self.rnetworkprefix}' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: check routing information by zebos command on local dut failed")

    def test_05_check_routing_information_by_zebos_command_on_remote_dut(self):
        time.sleep(20)
        res, showoutput = routecli.show_in_routing_bgp('show ip bgp ipv4 unicast')
        logger.info(f'showoutput is:{showoutput}')
        flag = True if f'*> {self.lnetworkprefix}' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: check routing information by zebos command on remote dut failed")

    def test_06_add_learned_route_ao_on_local_dut(self):
        remote_x0_subnet = {
            'name': self.rnetworkprefix,
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{self.rnetworkprefix},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x0_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    def test_07_add_allow_access_rule_from_lan_x3_subnet_to_learned_subnet_on_local_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["name"] = "l_lan_to_vpn_173_1_1_0"
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": self.rnetworkprefix}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add lan to vpn access rule on local dut failed")

    # check if can hit dynamic route that advertised by network command
    def test_06_send_traffic_to_learned_bgp_route_and_check_if_hit_the_route_policy(self):
        flag = False
        # get hit time in tsr before send traffic
        tsrrouting = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        hittimebefore = get_dynamic_route_hit_time_in_tsr(tsrrouting, self.rnetworkprefix)
        logger.info(f'hittimebefore is :{hittimebefore}')
        PC2_Login.send_command(f'ping -I eth1 -c 5 173.1.1.100')
        # get hit time in tsr after send traffic
        tsrrouting_1 = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        hittimeafter = get_dynamic_route_hit_time_in_tsr(tsrrouting_1, self.rnetworkprefix)
        logger.info(f'hittimeafter is {hittimeafter}')
        logger.info(f'hittimebefore is {hittimebefore}')
        if hittimeafter != hittimebefore:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check hit bgp route over unnumbered tunnel interface failed")


# Expected: after VPN policy name being changed,the BGP related routes interface name also changed
class TestTC22_verify_bgp_routes_interface_name_change_after_vpn_policy_name_changed(Test):
    uuid = "SOSAIOT-TC-55824"
    description = show_testcase_info(TESTPLAN, 'tc22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_vpn_policy_name(self):
        modify_vpn_dict = {
            'type': 'tunnel_interface',
            'name': Parameter.LOCAL_VPN_NAME,
            'new_name': 'localtunnelvpn_test',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '',
            'peer_ike_id': '',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            'ike_auth': 'sha-1',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            'ipsec_pfs': False,
            'keep_alive': True,
        }
        res = vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: change vpn policy name failed")

    def test_03_check_name_of_static_route_for_unnumbered_interface_in_router_policy_page(self):
        flag = False
        output = routepolicyapi.get_route_policy_by_name('pbr_vpn')
        logger.info(f'output is:{output}')
        routelist = output['route_policies']
        for routes in routelist:
            if "'name': 'remote_x0_subnet'" in str(routes) and "'interface': 'localtunnelvpn_test'" in str(routes):
                flag = True
                break
        Assertion.assert_equal(flag, True,
                               "ERR: check name of the added static routing for unnumbered interface changed failed")

    def test_04_check_bgp_learned_routes_interface(self):
        time.sleep(20)
        routepolres = routepolicyapi.get_route_pol_list()
        logger.info(f'routepolres is :{routepolres}')
        res = get_d_route_interface(routepolres, f'{Parameter.LEARNEDROUTE}/24')
        logger.info(f'get interface is:{res}')
        flag = True if res == 'localtunnelvpn_test' else False
        Assertion.assert_equal(flag, True,
                               "ERR: check name of bgp routes learned from unnumbered interface changed failed")


# Expected: BGP over unnumbered tunnel interface can be re-established afer disable and enable the VPN policy
class TestTC23_Verify_bgp_over_unnumbered_tunnel_interface_can_be_re_established(Test):
    uuid = "SOSAIOT-TC-55825"
    description = show_testcase_info(TESTPLAN, 'tc23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(2)
    def test_02_check_bgp_status_after_disable_vpn_policy(self):
        flag = False
        modify_vpn_dict = {
            'type': 'tunnel_interface',
            'name': 'localtunnelvpn_test',
            'enable': False,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '',
            'peer_ike_id': '',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            'ike_auth': 'sha-1',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            'ipsec_pfs': False,
            'keep_alive': True,
        }
        showoutput = routecli.show_BGP('neighbor')
        if 'Established' in showoutput:
            res = vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
            logger.info(f'res is:{res}')
            time.sleep(30)
            showoutput1 = routecli.show_BGP('neighbor')
            if 'Established' not in showoutput1:
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check bgp status failed")

    def test_03_check_bgp_over_unnumbered_tunnel_interface_re_established_after_enable_vpn_policy(self):
        flag = False
        modify_vpn_dict = {
            'type': 'tunnel_interface',
            'name': 'localtunnelvpn_test',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '',
            'peer_ike_id': '',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            'ike_auth': 'sha-1',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            'ipsec_pfs': False,
            'keep_alive': True,
        }
        res = vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is:{res}')
        time.sleep(30)
        (res1, msg) = vpnbasesettingapi.get_vpn_status('localtunnelvpn_test')
        logger.info(f'get vpn status res is: {res1},msg is: {msg}')
        if msg == 'up':
            for i in range(0, 4):
                time.sleep(30)
                showoutput = routecli.show_BGP('neighbor')
                if 'Established' in showoutput:
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check bgp status failed")


# Expected: All BGP over unnumbered tunnel interface related settings are intact after FW restart.
class TestTC28_check_settings_intact_after_fw_restart(Test):
    uuid = "SOSAIOT-TC-55826"
    description = show_testcase_info(TESTPLAN, 'tc28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_03_check_bgp_settings_after_restart_dut(self):
        check_list = ['router bgp 10',
                      'network 193.1.1.0/24',
                      f'neighbor {Parameter.X0_REMOTE_IP} remote-as 20',
                      f'neighbor {Parameter.X0_REMOTE_IP} ebgp-multihop 255',
                      f'neighbor {Parameter.X0_REMOTE_IP} update-source {Parameter.X0_IP}']
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in check_list]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp settings after restart failed")

    @repeat_method(2)
    def test_04_check_if_bgp_neighbor_is_established_after_restart(self):
        time.sleep(50)
        res, showoutput = routecli.show_in_routing_bgp(f'show ip bgp neighbor {Parameter.X0_REMOTE_IP}')
        logger.info(f'showoutput is:{showoutput}')
        flag = True if 'Established' in showoutput else False
        Assertion.assert_equal(flag, True, "ERR: check bgp neighbor after restart failed")


# Expected:All BGP over unnumbered tunnel interface related settings and current BGP route info should be included in
# the exported TSR.
class TestTC30_check_tsr(Test):
    uuid = "SOSAIOT-TC-55828"
    description = show_testcase_info(TESTPLAN, 'tc30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_bgp_in_tsr(self):
        tsrres = diagnosticapi.get_tsr_dynamic_routing_protocol_setting('BGP')
        logger.info(f'tsrres is:{tsrres}')
        check_list = ['router bgp 10',
                      'network 193.1.1.0/24',
                      f'neighbor {Parameter.X0_REMOTE_IP} remote-as 20',
                      f'neighbor {Parameter.X0_REMOTE_IP} ebgp-multihop 255',
                      f'neighbor {Parameter.X0_REMOTE_IP} update-source {Parameter.X0_IP}']
        checkres = [i in tsrres for i in check_list]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp settings in tsr failed")

    def test_03_check_bgp_route_in_tsr(self):
        flag = False
        tsrrouting = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        route_sp = tsrrouting.split('\n\n\n')
        for route in route_sp:
            if f'rangeBegin: {Parameter.LEARNEDROUTE}' in route:
                logger.info(f'bgp route is :{route}')
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check bgp route in tsr failed")


# Expected:  BGP over unnumber tunnel interface works when update source interface is VLAN interface
class TestTC38_verify_bgp_over_unnumbered_tunnel_interface_when_update_source_interface_is_vlan_interface(Test):
    uuid = "SOSAIOT-TC-55829"
    description = show_testcase_info(TESTPLAN, 'tc38', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc38')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_bgp_settings_with_vlan_interface_as_update_source_on_local_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        l_cmds = [
            f'neighbor {Parameter.X0_REMOTE_VLAN_IP} remote-as 20',
            f'neighbor {Parameter.X0_REMOTE_VLAN_IP} ebgp-multihop 255',
            f'neighbor {Parameter.X0_REMOTE_VLAN_IP} update-source {Parameter.X0_VLAN_IP}',
        ]
        res, confoutput = routecli.config_router_bgp(l_cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        Assertion.assert_equal(res, True, "ERR: configure bgp in cli on local dut failed")

    def test_03_configure_bgp_settings_with_vlan_interface_as_update_source_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Remote Settings for BGP'))
        r_cmds = [
            f'neighbor {Parameter.X0_VLAN_IP} remote-as 10',
            f'neighbor {Parameter.X0_VLAN_IP} ebgp-multihop 255',
            f'neighbor {Parameter.X0_VLAN_IP} update-source {Parameter.X0_REMOTE_VLAN_IP}',
        ]
        res, confoutput = r_routecli.config_router_bgp(r_cmds, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        Assertion.assert_equal(res, True, "ERR: configure bgp in cli on remote dut failed")

    def test_04_add_static_route_to_remote_x0_vlan_subnet_with_tunnel_interface_on_local_dut(self):
        l_pbr_dict = copy.deepcopy(pbr_dict)
        update_dict = {
            "name": "pbr_vpn_vlan",
            "interface": Parameter.LOCAL_VPN_NAME_MODIFIED,
            "destination": {
                "name": "remote_x0_vlan_subnet"
            },
        }
        l_pbr_dict["route_policies"][0]["ipv4"].update(update_dict)
        logger.info(f'l_pbr_vlan_dict is:{l_pbr_dict}')
        res = routepolicyapi.add_route_policy(**l_pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: add static route based VPN on unnumbered interface on local dut failed")

    def test_05_add_static_route_to_remote_x0_vlan_subnet_with_tunnel_interface_on_remote_dut(self):
        r_pbr_dict = copy.deepcopy(pbr_dict)
        update_dict = {
            "name": "pbr_vpn_vlan",
            "interface": Parameter.REMOTE_VPN_NAME,
            "destination": {
                "name": "remote_x0_vlan_subnet"
            },
        }
        r_pbr_dict["route_policies"][0]["ipv4"].update(update_dict)
        res = r_routepolicyapi.add_route_policy(**r_pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True,
                               "ERR: add static route based VPN on unnumbered interface on remote dut failed")

    @repeat_method(3)
    def test_06_check_if_bgp_neighbor_is_established(self):
        time.sleep(30)
        res, showoutput = routecli.show_in_routing_bgp(f'show ip bgp neighbor {Parameter.X0_REMOTE_VLAN_IP}')
        logger.info(f'showoutput is:{showoutput}')
        Assertion.assert_regular(showoutput, 'Established', "ERR: check bgp neighbor failed")


# Expected: BGP works well when have both BGP over numbered interface and BGP over unnumber interface configured
class TestTC40_verify_bgp_works_well_when_both_bgp_over_numbered_and_unnumbered_interfaces_configured(Test):
    uuid = "SOSAIOT-TC-55830"
    description = show_testcase_info(TESTPLAN, 'tc40', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc40')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_tunnel_vpn_policy_on_local_dut(self):
        lvpn_dict = copy.deepcopy(vpn_policy_dict)
        lvpn_dict.update(
            {'name': 'localtunnelvpn_1', 'pri_gate': Parameter.X2_REMOTE_IP, 'bound_to': ['interface', 'X2']})
        res = vpnbasesettingapi.add_vpn_policy(**lvpn_dict)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'localtunnelvpn_1', "ERR: Add local tunnel vpn policy failed.")

    def test_03_add_tunnel_vpn_policy_on_remote_dut(self):
        rvpn_dict = copy.deepcopy(vpn_policy_dict)
        rvpn_dict.update({'name': 'remotetunnelvpn_1', 'pri_gate': Parameter.X2_IP, 'bound_to': ['interface', 'X2']})
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn_dict)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotetunnelvpn_1', "ERR: Add remote tunnel vpn policy failed.")

    def test_04_create_vpn_tunnel_interface_local_and_remote_dut(self):
        l_ti_dict = copy.deepcopy(tunnel_interface_dict)
        l_ti_dict.update({'ip': Parameter.L_TI_IP, 'vpn_policy': 'localtunnelvpn_1'})
        r_ti_dict = copy.deepcopy(tunnel_interface_dict)
        r_ti_dict.update({'ip': Parameter.R_TI_IP, 'vpn_policy': 'remotetunnelvpn_1'})
        res1 = interfacev4api.add_interface(**l_ti_dict)
        res2 = r_interfacev4api.add_interface(**r_ti_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: create tunnel interface on local and remote dut failed")

    def test_05_configure_bgp_in_cli_on_local_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.R_TI_IP} remote-as 20',
                f'neighbor {Parameter.R_TI_IP} ebgp-multihop 255',
                ]
        res, confoutput = routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on local dut failed")

    def test_06_configure_bgp_in_cli_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.L_TI_IP} remote-as 10',
                f'neighbor {Parameter.L_TI_IP} ebgp-multihop 255',
                ]
        res, confoutput = r_routecli.config_router_bgp(cmds, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on remote dut failed")

    def test_07_check_bgp_neighbors(self):
        time.sleep(20)
        res1, showoutput_1 = routecli.show_in_routing_bgp(f'show ip bgp neighbor {Parameter.R_TI_IP}')
        res2, showoutput_2 = routecli.show_in_routing_bgp(f'show ip bgp neighbor {Parameter.X0_REMOTE_IP}')
        num = (showoutput_1 + showoutput_2).count('Established')
        Assertion.assert_equal(num, 2, "ERR: check bgp neighbors failed")


# Expected:distant neighbors can be established
class TestTC43_verify_bgp_can_establishes_over_unnumbered_interface_between_distant_duts(Test):
    uuid = "SOSAIOT-TC-55831"
    description = show_testcase_info(TESTPLAN, 'tc43', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc43')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_establish_bgp_over_unnumbered_interface_between_distant_duts(self):
        # the devices are connected to each other via switches in the network topology,so pass this case
        Assertion.assert_equal(ParamCases.TC01test07, True, "ERR: establishing bgp over unnumbered interface between "
                                                            "distant dut failed")


# Expected:All BGP over unnumbered tunnel interface related settings are intact after import prefs file.
class TestTC29_export_and_import_prefs_file(Test):
    uuid = "SOSAIOT-TC-55827"
    description = show_testcase_info(TESTPLAN, 'tc29', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc29')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_bgp_settings(self):
        cmd = ['redistribute connected', 'redistribute static']
        res, confoutput = routecli.config_router_bgp(cmd, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        flag = True if ('redistribute static' in showoutput and 'redistribute connected' in showoutput) else False
        Assertion.assert_equal(flag, True, "ERR: add bgp settings failed")

    def test_03_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/jlian_bgp_over_unnumbered_interface_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_04_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_05_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/jlian_bgp_over_unnumbered_interface_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_06_check_bgp_settings_after_import_prefs(self):
        check_list = ['router bgp 10',
                      'redistribute connected',
                      'redistribute static',
                      'network 193.1.1.0/24',
                      f'neighbor {Parameter.X0_REMOTE_IP} remote-as 20',
                      f'neighbor {Parameter.X0_REMOTE_IP} ebgp-multihop 255',
                      f'neighbor {Parameter.X0_REMOTE_IP} update-source {Parameter.X0_IP}',
                      f'neighbor {Parameter.R_TI_IP} remote-as 20',
                      f'neighbor {Parameter.R_TI_IP} ebgp-multihop 255',
                      f'neighbor {Parameter.X0_REMOTE_VLAN_IP} remote-as 20',
                      f'neighbor {Parameter.X0_REMOTE_VLAN_IP} ebgp-multihop 255',
                      f'neighbor {Parameter.X0_REMOTE_VLAN_IP} update-source {Parameter.X0_VLAN_IP}',
                      ]
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in check_list]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp settings after restart failed")

    @repeat_method(2)
    def test_07_check_if_bgp_neighbor_is_established_after_restart(self):
        time.sleep(20)
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        num = showoutput.count("Established")
        Assertion.assert_equal(num, 3, "ERR: check bgp neighbor after restart failed")
