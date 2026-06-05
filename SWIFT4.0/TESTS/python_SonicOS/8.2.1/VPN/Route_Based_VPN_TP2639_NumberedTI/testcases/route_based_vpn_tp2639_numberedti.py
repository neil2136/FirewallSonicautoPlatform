import json
import re
import ipaddress
from definition.settings import *
from definition.utils import *


# Expected: cnfigured tunnel interface will be displayed on the Network > Interfaces page of the firewall.
class TestTC08_tunnel_interface_is_shown_on_network_interfaces_page(Test):
    uuid = "SOSAIOT-TC-54159"
    description = show_testcase_info(TESTPLAN, 'tc08', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_tunnle_vpn_policy_on_local_dut(self):
        lvpn_dict = copy.deepcopy(vpn_policy_dict)
        lvpn_dict.update({'name': Parameter.LOCAL_VPN_NAME, 'pri_gate': Parameter.X1_REMOTE_IP})
        res = vpnbasesettingapi.add_vpn_policy(**lvpn_dict)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), Parameter.LOCAL_VPN_NAME, "ERR: Add local tunnel vpn policy failed.")

    def test_03_create_vpn_tunnel_interface_local(self):
        l_ti_dict = copy.deepcopy(tunnel_interface_dict)
        l_ti_dict.update({'ip': Parameter.L_TI_IP, 'vpn_policy': Parameter.LOCAL_VPN_NAME})
        res = interfacev4api.add_interface(**l_ti_dict)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on local dut failed")

    def test_04_check_tunnel_interface_displayed_in_network_interface_page(self):
        output = interfacev4api.get_tunnel_interface_status(name=Parameter.TUNNEL_INTERFACE, type='vpn')
        logger.info(f'output is:{output}')
        flag = True if f"'name': '{Parameter.TUNNEL_INTERFACE}'" in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: check tunnel interface displayed in network->interface page failed")


# Expected: tunnel_interface is shown on the Network > Routing page along with physical interfaces
class TestTC12_tunnel_interface_is_shown_in_dynamic_routing_page(Test):
    uuid = "SOSAIOT-TC-54142"
    description = show_testcase_info(TESTPLAN, 'tc12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_tunnel_interface_and_status_in_dynamic_routing_page(self):
        ospfv2info, ripinfo, ospfv3info, ripnginfo = get_dynamic_protocol_status_on_ti(dynamicroutingapi, 'Ni')
        res = True if 'disabled' in str(ripinfo) and 'disabled' in str(ospfv2info) and 'disabled' in str(ripnginfo) \
                      and 'disabled' in str(ospfv3info) else False
        Assertion.assert_equal(res, True, "ERR: check tunnel interface displayed in dynamic->routing page and display "
                                          "status failed")


# Expected: Default route for the TI interface is deleted from the Route Policies table on the Network > Routing page.
class TestTC20_defaut_route_for_tunnel_interface_is_deleted_after_delete_ti(Test):
    uuid = "SOSAIOT-TC-54143"
    description = show_testcase_info(TESTPLAN, 'tc20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_default_route_for_tunnel_interfac_in_route_policy_page(self):
        output = routepolicyapi.get_route_policy()
        logger.info(f'output is :{output}')
        flag = True if '"destination": {"name": "Ni Subnet"}' in json.dumps(output) else False
        Assertion.assert_equal(flag, True, "ERR: check default route for tunnel interface in route policy page failed")

    def test_03_delete_tunnel_interface(self):
        res = interfacev4api.del_tunnel_interface_by_name(Parameter.TUNNEL_INTERFACE)
        Assertion.assert_equal(res, True, "ERR: delete tunnel interface failed")

    def test_04_check_default_route_for_tunnel_interfac_in_route_policy_page_after_delete_tunnel_interface(self):
        output = routepolicyapi.get_route_policy()
        logger.info(f'output is :{output}')
        flag = True if '"destination": {"name": "Ni Subnet"}' not in json.dumps(output) else False
        Assertion.assert_equal(flag, True, "ERR: check default route for tunnel interface in route policy page failed")


# Expected: OSPF Enabled is shown for the TIn (VPN) interface on the Network > Routing page.
class TestTC30_configure_ospf_on_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54145"
    description = show_testcase_info(TESTPLAN, 'tc30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_vpn_tunnel_interface_local(self):
        l_ti_dict = copy.deepcopy(tunnel_interface_dict)
        l_ti_dict.update({'ip': Parameter.L_TI_IP, 'vpn_policy': Parameter.LOCAL_VPN_NAME})
        res = interfacev4api.add_interface(**l_ti_dict)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on local dut failed")

    def test_03_enable_ospfv2_for_tunnel_interface_on_local_dut(self):
        l_default_ospfv2 = copy.deepcopy(default_ospf2)
        l_default_ospfv2.update({'num_id': '1'})
        res = dynamicroutingapi.set_ospf2(**l_default_ospfv2)
        logger.info(f'res is : {res}')
        Assertion.assert_equal(res, True, "ERR: enable ospfv2 on tunnel interface failed")

    def test_04_check_tunnel_interface_status_in_dynamic_routing_ospfv2_tab(self):
        ospfv2info = get_dynamic_protocol_status_on_ti(dynamicroutingapi, 'Ni', 'ospfv2')
        flag = True if 'enabled' in str(ospfv2info) else False
        Assertion.assert_equal(flag, True, "ERR: ospfv2 is shown enabled for tunnel interface failed")


# Expected: OSPF can establishes session on tunnel interface and can learn routes through tunnel interface
class TestTC31_establish_ospf_through_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54146"
    description = show_testcase_info(TESTPLAN, 'tc31', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_redistribute_connected_on_local_ospf_setting(self):
        ospf_setting_dict = {
            'router_id': '10.10.10.10',
            'connect_network': 'on',
        }
        res = dynamicroutingapi.ospf2_config(**ospf_setting_dict)
        Assertion.assert_equal(res, True, "ERR: redistribute connected route on local ospf setting failed")

    def test_03_add_tunnle_vpn_policy_on_remote_dut(self):
        rvpn_dict = copy.deepcopy(vpn_policy_dict)
        rvpn_dict.update({'name': Parameter.REMOTE_VPN_NAME, 'pri_gate': Parameter.X1_IP})
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn_dict)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), Parameter.REMOTE_VPN_NAME, "ERR: Add remote tunnel vpn policy failed.")

    def test_04_create_vpn_tunnel_interface_on_remote_dut(self):
        r_ti_dict = copy.deepcopy(tunnel_interface_dict)
        r_ti_dict.update({'ip': Parameter.R_TI_IP, 'vpn_policy': Parameter.REMOTE_VPN_NAME})
        res = r_interfacev4api.add_interface(**r_ti_dict)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on remote dut failed")

    def test_05_enable_ospfv2_for_tunnel_interface_on_remote_dut(self):
        flag = True
        r_default_ospfv2 = copy.deepcopy(default_ospf2)
        r_default_ospfv2.update({'num_id': '0'})
        res = r_dynamicroutingapi.set_ospf2(**r_default_ospfv2)
        logger.info(f'res is : {res}')
        if res:
            ospfv2info = get_dynamic_protocol_status_on_ti(r_dynamicroutingapi, 'Ni', 'ospfv2')
            flag = True if 'enabled' in str(ospfv2info) else False
        Assertion.assert_equal(flag, True, "ERR: enable ospfv2 on tunnel interface failed")

    def test_06_enable_redistribute_connected_on_remote_ospf_setting(self):
        ospf_setting_dict = {
            'router_id': '20.20.20.20',
            'connect_network': 'on',
        }
        res = r_dynamicroutingapi.ospf2_config(**ospf_setting_dict)
        Assertion.assert_equal(res, True, "ERR: redistribute connected route on remote ospf setting failed")

    @repeat_method(2)
    def test_07_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status(Parameter.LOCAL_VPN_NAME)
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    def test_08_check_tunnel_interface_status_on_local_and_remote_dut(self):
        l_status = get_interface_status(interfacev4api, Parameter.TUNNEL_INTERFACE)
        r_status = get_interface_status(r_interfacev4api, Parameter.TUNNEL_INTERFACE)
        logger.info(f'l_status is:{l_status},r_status is:{r_status}')
        flag = True if (l_status == 'Interface Up' and r_status == 'Interface Up') else False
        Assertion.assert_equal(flag, True, "ERR: check tunnel interface status failed")

    @repeat_method(3)
    def test_09_check_ospf_routes_learned_through_tunnel_interface(self):
        time.sleep(60)
        ospfstatus_dict = {'interface': Parameter.TUNNEL_INTERFACE,
                           'type': 'TI',
                           'num_id': 1
                           }
        ospfnboutput = dynamicroutingapi.get_interface_ospfv2_status(**ospfstatus_dict)
        logger.info(f'ospfnboutput is :{ospfnboutput}')
        if 'Full' in str(ospfnboutput):
            time.sleep(20)
            check_dict = {
                'gw': Parameter.R_TI_IP,
                'd_protocol': 'ospfv2',
                'interface': 'Ni',
                'route': ['12.12.3.0/24', '172.16.1.0/24']
            }
            reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
            logger.info(f'reslist is :{reslist}')
        else:
            logger.info(f'ospf neighbor is down')
        Assertion.assert_equal(all(reslist), True, "ERR: check ospf routes learned via tunnel interface failed")


# Expected: traffic succeeds between local and remote networks when manual access rules have been added.
class TestTC32_verify_ospf_traffic_over_tunnel_interface_after_add_access_rule(Test):
    uuid = "SOSAIOT-TC-54147"
    description = show_testcase_info(TESTPLAN, 'tc32', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_allow_access_rule_from_lan_x2_subnet_to_vpn_remote_x3_subnet_on_local_dut(self):
        res = accessruleapi.add_accessrule(**accessrule_dict)
        Assertion.assert_equal(res, True, "ERR: add lan to vpn access rule on local dut failed")

    def test_03_add_allow_access_rule_from_vpn_remote_x3_subnet_to_lan_x2_subnet_on_local_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["from"] = "VPN"
        rule_dict["access_rules"][0]["ipv4"]["to"] = "LAN"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "l_vpn_to_lan"
        rule_dict["access_rules"][0]["ipv4"]["source"]["address"] = {"name": "remote_x3_subnet"}
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "X2 Subnet"}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on local dut failed")

    def test_04_add_allow_access_rule_from_vpn_remote_x2_subnet_to_lan_x3_subnet_on_remote_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["from"] = "VPN"
        rule_dict["access_rules"][0]["ipv4"]["to"] = "LAN"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "r_vpn_to_lan"
        rule_dict["access_rules"][0]["ipv4"]["source"]["address"] = {"name": "remote_x2_subnet"}
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "X3 Subnet"}
        res = r_accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on remote dut failed")

    def test_05_add_allow_access_rule_from_lan_x3_subnet_to_vpn_remote_x2_subnet_on_remote_dut(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["name"] = "r_lan_to_vpn"
        rule_dict["access_rules"][0]["ipv4"]["source"]["address"] = {"name": "X3 Subnet"}
        rule_dict["access_rules"][0]["ipv4"]["destination"]["address"] = {"name": "remote_x2_subnet"}
        res = r_accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add vpn to lan access rule on remote dut failed")

    def test_06_verify_icmp_traffic_between_local_x2_subnet_and_remote_x3_subnet(self):
        res1 = PC2_Login.ping_from_eth(PC3_ETH1_IP, 'eth1')
        res2 = PC3_Login.ping_from_eth(PC2_ETH1_IP, 'eth1')
        logger.info(f'res1 is {res1},res2 is :{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: traffic between local x2 subnet and remote x3 subnet failed")


# Expected: dynamic routes advertised by OSPF on tunnel interface will be deleted from the Route Policies table when OSPF on tunnel interface gets disabled.
class TestTC35_disable_ospf_on_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54148"
    description = show_testcase_info(TESTPLAN, 'tc35', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc35')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_disable_ospfv2_for_tunnel_interface_on_local_and_remote_dut(self):
        l_default_ospfv2 = copy.deepcopy(default_ospf2)
        r_default_ospfv2 = copy.deepcopy(default_ospf2)
        l_default_ospfv2.update({'mode': 'disable', 'num_id': '1'})
        r_default_ospfv2.update({'mode': 'disable', 'num_id': '0'})
        res1 = dynamicroutingapi.set_ospf2(**l_default_ospfv2)
        res2 = r_dynamicroutingapi.set_ospf2(**r_default_ospfv2)
        logger.info(f'res1 is : {res1},res2 is :{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: disable ospfv2 on tunnel interface failed")

    @repeat_method(2)
    def test_03_check_ospf_routes_learned_through_tunnel_interface_on_local_dut(self):
        time.sleep(30)
        output = routepolicyapi.get_dynamic_route_policy()
        logger.info(f'output is:{output}')
        flag = True if '12.12.3.0/24' not in str(output) and '172.16.1.0/24' not in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: check ospf routes learned via tunnel interface is deleted failed")

    @repeat_method(2)
    def test_04_check_ospf_routes_learned_through_tunnel_interface_on_local_dut(self):
        time.sleep(30)
        output = r_routepolicyapi.get_dynamic_route_policy()
        logger.info(f'output is:{output}')
        flag = True if '192.168.168.0/24' not in str(output) and '193.168.1.0/24' not in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: check ospf routes learned via tunnel interface is deleted failed")


# Expected: remote firewall’s route are displayed in local Route Policies table.
class TestTC24_learn_rip_route_through_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54144"
    description = show_testcase_info(TESTPLAN, 'tc24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_rip_for_tunnel_interface_on_local_and_remote_dut(self):
        l_rip = copy.deepcopy(default_rip_dict)
        r_rip = copy.deepcopy(default_rip_dict)
        l_rip.update({'num_id': '1'})
        r_rip.update({'num_id': '0'})
        res1 = dynamicroutingapi.set_rip(**l_rip)
        res2 = r_dynamicroutingapi.set_rip(**r_rip)
        logger.info(f"config rip on dut: {res1},{res2}")
        Assertion.assert_equal(res1 & res2, True, "ERR: enable rip on local and remote dut failed")

    def test_03_enable_redistribute_connected_on_local_and_remote_rip_setting(self):
        rip_setting_dict = {
            'RedistributeConnectedNetworks': 'on',
            'StaticsMetric': '1'
        }
        res1 = dynamicroutingapi.rip_config(**rip_setting_dict)
        res2 = r_dynamicroutingapi.rip_config(**rip_setting_dict)
        logger.info(f'res1 is {res1},res2 is {res2}')
        Assertion.assert_equal(res1 & res2, True,
                               "ERR: redistribute connected route on local and remote ospf setting failed")

    def test_04_check_rip_routes_learned_through_tunnel_interface(self):
        time.sleep(60)
        droutoutput = routepolicyapi.get_dynamic_route_policy()
        logger.info(f'drouteoutput is:{droutoutput}')
        time.sleep(10)
        check_dict = {
            'gw': Parameter.R_TI_IP,
            'd_protocol': 'rip',
            'interface': 'Ni',
            'route': ['12.12.3.0/24', '172.16.1.0/24']
        }
        reslist = check_droute_learned_from_ti_in_route_policy(routepolicyapi, **check_dict)
        logger.info(f'reslist is :{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: check rip routes learned via tunnel interface failed")


# Expected: the firewall will not allow deleting the tunnel interface if a routing protocol is enabled on this tunnel interface.
class TestTC52_tunnel_interface_cannot_be_deleted_if_enable_routing_protocols_on_it(Test):
    uuid = "SOSAIOT-TC-54156"
    description = show_testcase_info(TESTPLAN, 'tc52', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc52')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_tunnel_interface_with_rip_enabled(self):
        res, msg = interfacev4api.del_tunnel_interface_by_name(Parameter.TUNNEL_INTERFACE, msg=True)
        logger.info(f'res is:{res},msg is :{msg}')
        Assertion.assert_regular(str(msg), 'Interface is in use by RIP', "ERR: delete tunnel interface failed")

    def test_03_disable_rip_for_tunnel_interface_on_local_and_remote_dut(self):
        l_rip = copy.deepcopy(default_rip_dict)
        r_rip = copy.deepcopy(default_rip_dict)
        l_rip.update({'num_id': '1', 'mode': 'disable'})
        r_rip.update({'num_id': '0', 'mode': 'disable'})
        res1 = dynamicroutingapi.set_rip(**l_rip)
        res2 = r_dynamicroutingapi.set_rip(**r_rip)
        logger.info(f"config rip on dut: {res1},{res2}")
        Assertion.assert_equal(res1 & res2, True, "ERR: disable rip on local and remote dut failed")


# Expected:  Allow BGP” VPN > VPN firewall rule is auto-added when BGP is enabled.
class TestTC37_bgp_vpn_to_vpn_accessrule_is_auto_added_when_bgp_is_enabled(Test):
    uuid = "SOSAIOT-TC-54149"
    description = show_testcase_info(TESTPLAN, 'tc37', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc37')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_bgp_on_local_dut(self):
        opt = {
            'advanced': True,
            'BGP': True
        }
        res = dynamicroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res, True, "ERR: enable BGP failed")

    def test_03_check_bgp_auto_added_access_rule_from_vpn_to_vpn(self):
        flag = False
        output = accessruleapi.get_accessrule_via_zones(srczone='VPN', dstzone='VPN')
        ruleslist = output['access_rules']
        for rule in ruleslist:
            if 'BGP' in str(rule):
                logger.info(f'bgp rule is:{rule}')
                srcinfo = rule['ipv4']['source']
                destinfo = rule['ipv4']['destination']
                serviceinfo = rule['ipv4']['service']
                flag = True if "'any': True" in str(srcinfo) and f"'name': '{Parameter.TUNNEL_INTERFACE} IP'" in str(
                    destinfo) and 'BGP' in str(
                    serviceinfo) else False
                break
        Assertion.assert_equal(flag, True, "ERR: check auto added bgp accessrule from vpn to vpn failed")


# Expected:  Allow BGP” VPN > VPN firewall rule is auto-added when BGP is enabled.
class TestTC38_configure_bgp_on_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54150"
    description = show_testcase_info(TESTPLAN, 'tc38', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc38')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_bgp_in_cli_on_local_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.R_TI_IP} remote-as 20', 'bgp router-id 10.10.10.10',
                f'neighbor {Parameter.R_TI_IP} ebgp-multihop 255',
                'network 193.168.1.0/24']
        res, confoutput = routecli.config_router_bgp(cmds, '10')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on local dut failed")


# Expected: route for advertised network prefix is added in the Route Policy table when BGP establishes session on
# tunnel interface.
class TestTC39_bgp_establishes_session_on_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54151"
    description = show_testcase_info(TESTPLAN, 'tc39', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc39')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_bgp_on_remote_dut(self):
        opt = {
            'advanced': True,
            'BGP': True
        }
        res = r_dynamicroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res, True, "ERR: enable BGP failed")

    def test_03_configure_bgp_in_cli_on_remote_dut(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmds = [f'neighbor {Parameter.L_TI_IP} remote-as 10', 'bgp router-id 20.20.20.20',
                f'neighbor {Parameter.L_TI_IP} ebgp-multihop 255',
                'network 12.12.3.0/24']
        res, confoutput = r_routecli.config_router_bgp(cmds, '20')
        logger.info(f'res is :{res},confoutput is:{confoutput}')
        showoutput = r_routecli.show_BGP()
        logger.info(f'showoutput is:{showoutput}')
        checkres = [i in showoutput for i in cmds]
        logger.info(f'checkres  is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: configure bgp in cli on remote dut failed")

    @repeat_method(2)
    def test_04_check_learned_bgp_route_in_route_policy_page(self):
        time.sleep(60)
        res = [False]
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        if 'Established' in showoutput:
            output = routepolicyapi.get_dynamic_route_policy()
            logger.info(f'output is:{output}')
            res = [False]
            for droute in output:
                if '12.12.3.0/24' in str(droute):
                    routelist1 = ["'destination': '12.12.3.0/24'", f"'interface': '{Parameter.TUNNEL_INTERFACE}'",
                                  f"'gateway': '{Parameter.R_TI_IP}'",
                                  "'metric': 20"]
                    res = [i in str(droute) for i in routelist1]
                    logger.info(f'res is:{res}')
        else:
            logger.info(f"bgp doesn't establish up")
        Assertion.assert_equal(all(res), True, "ERR: check bgp routes learned via tunnel interface failed")


# Expected: BGP route is shown in the console window when BGP establishes session on tunnel interface.
class TestTC40_bgp_establishes_session_on_tunnel_interface_zebos(Test):
    uuid = "SOSAIOT-TC-54152"
    description = show_testcase_info(TESTPLAN, 'tc40', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc40')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_learned_bgp_route_in_cli_zebos(self):
        flag = False
        showoutput = routecli.show_BGP('neighbor')
        logger.info(f'showoutput is:{showoutput}')
        if 'Established' in showoutput:
            output = routecli.show_nsm_database()
            logger.info(f'output is:{output}')
            if f"B    *> 12.12.3.0/24 [20/0] via {Parameter.R_TI_IP}, {Parameter.TUNNEL_INTERFACE}" in output:
                flag = True
        else:
            logger.info(f"bgp doesn't establish up")
        Assertion.assert_equal(flag, True, "ERR: check bgp routes learned via tunnel interface in cli failed")


# Expected: BGP status is shown on the Network > Routing page when BGP establishes session on tunnel interface.
class TestTC41_bgp_status_is_shown_in_bgp_summary_window(Test):
    uuid = "SOSAIOT-TC-54153"
    description = show_testcase_info(TESTPLAN, 'tc41', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc41')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_bgp_summary_window(self):
        bgpoutput = dynamicroutingapi.get_bgp_summary()
        logger.info(f'bgp summay output is :{bgpoutput}')
        bgpoutput_new = str(bgpoutput).replace('&nbsp;', ' ')
        logger.info(f'bgpoutput_new is :{bgpoutput_new}')
        checklist = [f'neighbor is {Parameter.R_TI_IP}', 'BGP state = Established']
        checkres = [i in bgpoutput_new for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check bgp summary window info failed")


# Expected: traffic will flow between local network and the network prefix advertised by BGP over tunnel interface
# when manual access rules are added.
class TestTC42_verify_bgp_traffic_over_tunnel_interface_after_add_access_rule(Test):
    uuid = "SOSAIOT-TC-54154"
    description = show_testcase_info(TESTPLAN, 'tc41', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc41')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_verify_icmp_traffic_between_local_x2_subnet_and_remote_x3_subnet(self):
        res1 = PC2_Login.ping_from_eth(PC3_ETH1_IP, 'eth1')
        res2 = PC3_Login.ping_from_eth(PC2_ETH1_IP, 'eth1')
        logger.info(f'res1 is {res1},res2 is :{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: traffic between local x2 subnet and remote x3 subnet failed")


# Expected: a static route can be bound to numbered tunnel interface.
class TestTC48_configure_static_route_based_vpn_on_numbered_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54155"
    description = show_testcase_info(TESTPLAN, 'tc48', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc48')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_disable_bgp_on_local_and_remote_dut(self):
        opt = {
            'advanced': True,
            'BGP': False
        }
        res1 = dynamicroutingapi.set_BGP(**opt)
        res2 = r_dynamicroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res1 & res2, True, "ERR: disable BGP on local and remote dut failed")

    def test_03_delete_accessrule_on_local_dut(self):
        res1 = accessruleapi.delete_accessrule_by_name('l_lan_to_vpn')
        res2 = accessruleapi.delete_accessrule_by_name('l_vpn_to_lan')
        Assertion.assert_equal(res1 & res2, True, "ERR: delete access rule on local dut failed")

    def test_04_add_static_route_with_tunnel_interface_on_local_dut(self):
        res = routepolicyapi.add_route_policy(**pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True,
                               "ERR: add static route based VPN on numbered tunnel interface on local dut failed")

    def test_05_add_static_route_with_tunnel_interface_on_remote_dut(self):
        r_pbr_dict = copy.deepcopy(pbr_dict)
        r_pbr_dict["route_policies"][0]["ipv4"]["source"] = {"name": "X3 Subnet"}
        r_pbr_dict["route_policies"][0]["ipv4"]["destination"] = {"name": "remote_x2_subnet"}
        res = r_routepolicyapi.add_route_policy(**r_pbr_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True,
                               "ERR: add static route based VPN on numbered tunnel interface on remote dut failed")

    def test_06_check_bgp_auto_added_access_rule_from_lan_to_vpn(self):
        flag = False
        output = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        ruleslist = output['access_rules']
        logger.info(f'ruleslist is :{ruleslist}')
        for rule in ruleslist:
            if "'source': {'address': {'name': 'X2 Subnet'}" in str(
                    rule) and "'destination': {'address': {'name': 'remote_x3_subnet'}}" in str(rule):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: check auto added accessrule from lan to vpn failed")

    def test_07_check_bgp_auto_added_access_rule_from_vpn_to_lan(self):
        flag = False
        output = accessruleapi.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        ruleslist = output['access_rules']
        logger.info(f'ruleslist is :{ruleslist}')
        for rule in ruleslist:
            if "'source': {'address': {'name': 'remote_x3_subnet'}" in str(
                    rule) and "'destination': {'address': {'name': 'X2 Subnet'}}" in str(rule):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: check auto added accessrule from vpn to lan failed")

    def test_08_verify_icmp_traffic_between_local_x2_subnet_and_remote_x3_subnet(self):
        res1 = PC2_Login.ping_from_eth(PC3_ETH1_IP, 'eth1')
        res2 = PC3_Login.ping_from_eth(PC2_ETH1_IP, 'eth1')
        logger.info(f'res1 is {res1},res2 is :{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: traffic between local x2 subnet and remote x3 subnet failed")


# Expected: the firewall doesn't allow deleting the tunnel interface if the static route is configured on this tunnel interface.
class TestTC53_tunnel_interface_cannot_be_deleted_if_static_route_with_it_exist(Test):
    uuid = "SOSAIOT-TC-54157"
    description = show_testcase_info(TESTPLAN, 'tc53', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc53')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_tunnel_interface_when_it_is_used_by_route_policy(self):
        res, msg = interfacev4api.del_tunnel_interface_by_name(Parameter.TUNNEL_INTERFACE, msg=True)
        logger.info(f'res is:{res},msg is :{msg}')
        Assertion.assert_regular(str(msg), 'Tunnel Interface is in use by Route Policy',
                                 "ERR: delete tunnel interface failed")


# Expected: a tunnel interface VPN policy cannot be deleted if the policy is attached to the tunnel interface on the
# Network > Interfaces page.
class TestTC63_tunnel_vpn_policy_cannot_be_deleted_if_it_is_used_by_tunnel_interface(Test):
    uuid = "SOSAIOT-TC-54158"
    description = show_testcase_info(TESTPLAN, 'tc63', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc63')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_tunnel_vpn_policy_used_by_tunnel_interface(self):
        del_dict = {
            'name': 'localtunnelvpn'
        }
        res, msg = vpnbasesettingapi.del_tunnelvpn_policy(msg=True, **del_dict)
        logger.info(f'res is:{res},msg is :{msg}')
        Assertion.assert_regular(str(msg), 'Unable to delete VPN Policy used by VPN tunnel interface',
                                 "ERR: delete tunnel interface failed")
