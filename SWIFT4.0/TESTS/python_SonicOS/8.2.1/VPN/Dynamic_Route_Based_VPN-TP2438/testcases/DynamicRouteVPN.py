from definition.settings import *
from definition.utils import *


# Add Tunnel Interface VPN policy with Keep Alive and enabled "Allow Advanced Routing"
class Test_addvpnenableOption_TC02(Test):
    uuid = "SOSAIOT-TC-54259"
    description = show_testcase_info(
        TESTPLAN, '1515035', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515035')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc1 = vpnapi.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc2 = gwvpnapi.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_03_check_Routing_Protocols_table(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        flag = True if tunnel_id else False
        Assertion.assert_equal(flag, True, 'check_Routing_Protocols_table Failed.')

    def test_04_check_active_vpn(self):
        time.sleep(10)
        flag = False
        activeIPsecSAs = vpnapi.get_active_vpn_tunnels()
        filter_tuple = ('"policyName": "test"', f'"gateway": "{Parameter.GW_X1_IP}"')
        logger.info(filter_tuple)
        for activeIPsecSA in activeIPsecSAs:
            logger.info(json.dumps(activeIPsecSA))
            if all(x in json.dumps(activeIPsecSA) for x in filter_tuple):
                flag = True
                break
        Assertion.assert_equal(flag, True, 'check_Routing_Protocols_table Failed.')


# Disable "Allow Advanced Routing" in Tunnel Interface policy
class Test_disableOption_TC03(Test):
    uuid = "SOSAIOT-TC-54262"
    description = show_testcase_info(
        TESTPLAN, '1515038', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515038')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        uptade_option = {'advanced_routing': False}
        ref1.update(uptade_option)
        rc1 = vpnapi.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc1, True, 'Edit VPN Policy Failed.')

    def test_03_check_Routing_Protocols_table(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        flag = True if tunnel_id else False
        Assertion.assert_equal(flag, False, 'check_Routing_Protocols_table Failed.')


#  Enable "Allow Advanced Routing" in Tunnel Interface policy
class Test_enableOption_TC04(Test):
    uuid = "SOSAIOT-TC-54265"
    description = show_testcase_info(
        TESTPLAN, '1515041', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515041')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        rc1 = vpnapi.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc1, True, 'Edit VPN Policy Failed.')

    def test_03_check_Routing_Protocols_table(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        flag = True if tunnel_id else False
        Assertion.assert_equal(flag, True, 'check_Routing_Protocols_table Failed.')


# Enable OSPF on tunnel interface
class Test_enableOspf_TC08(Test):
    uuid = "SOSAIOT-TC-54273"
    description = show_testcase_info(
        TESTPLAN, '1515049', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515049')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': Parameter.X1_IP,
            'static_route': 'on',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute Static Networks: {res}')
        Assertion.assert_equal(res, True, "ERR:enable Redistribute Static Networks fail")

    def test_04_enable_ospf_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        ospf_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.GW_X0_IP,
            'area': '0',
        }
        resdut = dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf on dut: {resdut}")
        Assertion.assert_equal(resdut, True, "ERR: Failed to enable ospf")

    def test_05_enable_ospf_on_vpngw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        ospf_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
            'area': '0',
        }
        resgw = gwdyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf on vpngw: {resgw}")
        Assertion.assert_equal(resgw, True, "ERR: Failed to enable ospf")

    def test_06_check_route_table(self):
        filter_route = {
            f'{Parameter.FIREWALL}',
            'Full',
            'TI:test'
        }
        res = gwroutecli.show_ospf2(mode='neighbor')
        flag = True if all(x in str(res) for x in filter_route) else False
        Assertion.assert_equal(flag, True, "ERR:can not find ospf route in dynamcic route table")

    def test_07_add_static_Route_on_gw(self):
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
            "name": 'test_route_59',
            "interface": "X0",
            'gateway': {'name': 'X0GW'},
            'destination': {"name": 'test_59'},
        }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}
        resrt = routeapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(resrt, True, "ERR: show testcase info failed")

    def test_08_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_08 = {
            '1.1.1.0/24',
            '110',
        }
        flag = True if all(x in str(dyntb) for x in filter_08) else False
        Assertion.assert_equal(flag, True, "ERR:can not find ospf route in dynamcic route table")


# OSPFv2: Hello packets are sent every Hello Interval seconds to the IP multicast address (224.0.0.5)
class Test_checkOspfPacket_TC59(Test):
    uuid = "SOSAIOT-TC-54267"
    description = show_testcase_info(
        TESTPLAN, '1515043', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515043')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        filter_route = {
            'OSPF Version: 2',
            f'Source: {Parameter.FIREWALL}',
            'Destination: 224.0.0.5',
            'Message Type: Hello Packet'
        }
        filteredpackets = filter_packet(gwpkgapi, PC1_Login, protocol='ospf')
        hellonumber = check_packet(filteredpackets, filter_route)
        logger.info(f"the number of hello is {hellonumber}")
        flag = True if hellonumber >= 5 else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")


#  TC06 Enable RIP on tunnel interface
class Test_enableRip_TC06(Test):
    uuid = "SOSAIOT-TC-54268"
    description = show_testcase_info(
        TESTPLAN, '1515044', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515044')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_rip_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.GW_X0_IP,
            'receive': '2',
            'send': '2',
        }
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on dut")

    def test_03_enable_rip_on_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
            'receive': '2',
            'send': '2',
        }
        resrip = gwdyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on lbox")

    def test_04_redistribute_connected_from_rip(self):
        rip_setting_dict = {
            'RedistributeConnectedNetworks': 'on',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR: Redistribute Connected Networks failed")


# Connected networks are advertised in RIP RTUs when the Redistribute Connected Networks check box is turned on
class Test_enableRip_TC37(Test):
    uuid = "SOSAIOT-TC-54264"
    res_for_test_tc30 = ContextVar('res_for_test_tc30')
    description = show_testcase_info(
        TESTPLAN, '1515040', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515040')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_route_table(self):
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_06 = {
            f'{Parameter.X3_VLAN1_SUBNET}',
            f'{Parameter.X2_SUBNET}',
            "120",
        }
        flag = True if all(x in str(dyntb) for x in filter_06) else False
        self.res_for_test_tc30.set(flag)
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


#  TC30 Send and Receive. Receive RIPv2, Send RIPv2 on DUT
class Test_enableRip_TC30(Test):
    uuid = "SOSAIOT-TC-54263"
    description = show_testcase_info(
        TESTPLAN, '1515039', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515039')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_route_table(self):
        flag = Test_enableRip_TC37().res_for_test_tc30.get()
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


#  Send and Receive. Receive RIPv2, Send RIPv1 on DUT
class Test_enableRip_TC28(Test):
    uuid = "SOSAIOT-TC-54261"
    description = show_testcase_info(
        TESTPLAN, '1515037', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515037')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_rip_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.GW_X0_IP,
            'receive': '2',
            'send': '0',
        }
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on dut")

    def test_03_enable_rip_on_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
            'receive': '0',
            'send': '2',
        }
        resrip = gwdyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on lbox")

    def test_04_check_packet_on_dut(self):
        logger.info("check packet receive on DUT with ripv2")
        filter_route = {
            f'Source: {Parameter.GW_X0_IP}',
            'Source port: router (520)',
            'Destination port: router (520)',
            'Version: RIPv2 (2)',
            "Destination: 224.0.0.9",
        }
        filteredpackets = filter_packet(pkgapi, PC1_Login, protocol='udp')
        ripnumber = check_packet(filteredpackets, filter_route)
        logger.info(f"the number of rip is {ripnumber}")
        flag = True if ripnumber > 0 else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_05_check_packet_on_gw(self):
        logger.info("check packet send to GW with ripv1")
        filter_route = {
            'Version: RIPv1',
            f'Source: {Parameter.FIREWALL}',
            f'Destination: {Parameter.GW_X0_IP}',
            'Source port: router (520)',
            'Destination port: router (520)'
        }
        gwfilteredpackets = filter_packet(gwpkgapi, PC1_Login, protocol='udp')
        ripnumber = check_packet(gwfilteredpackets, filter_route)
        logger.info(f"the number of rip is {ripnumber}")
        flag = True if ripnumber > 0 else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_06_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_06 = {
            f'{Parameter.X3_VLAN1_SUBNET}',
            f'{Parameter.X2_SUBNET}',
            '12.0.0.0/8',
            '120',
        }
        flag = True if all(x in str(dyntb) for x in filter_06) else False
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


#  Send Only RIPv2-v1 compatible on DUT
class Test_enableRip_TC21(Test):
    uuid = "SOSAIOT-TC-54260"
    description = show_testcase_info(
        TESTPLAN, '1515036', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515036')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_rip_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.GW_X0_IP,
            'send': '1',
        }
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(resrip, True, "ERR: Failed To enable rip on dut")

    def test_03_enable_rip_on_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
            'receive': '2',
        }
        resrip = gwdyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(resrip, True, "ERR: Failed To enable rip on lbox")

    def test_04_check_packet_on_gw(self):
        logger.info("check packet send to GW with  RIPv2-v1 compatible")
        filter_route = {
            'Version: RIPv2 (2)',
            f'Source: {Parameter.FIREWALL}',
            f'Destination: {Parameter.GW_X0_IP}',
            'Source port: router (520)',
            'Destination port: router (520)'
        }
        gwfilteredpackets = filter_packet(gwpkgapi, PC1_Login, protocol='udp')
        ripnumber = check_packet(gwfilteredpackets, filter_route)
        logger.info(f"the number of rip is {ripnumber}")
        flag = True if ripnumber > 0 else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    @repeat_method(3)
    def test_05_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_06 = {
            f'{Parameter.X3_VLAN1_SUBNET}',
            f'{Parameter.X2_SUBNET}',
            '120',
        }
        flag = True if all(x in str(dyntb) for x in filter_06) else False
        Assertion.assert_equal(flag, True, "ERR:can not find ospf route in dynamcic route table")


#  Verify after reboot, all dynamic route based VPN are still work well.
class Test_reboot_TC102(Test):
    uuid = "SOSAIOT-TC-54258"
    description = show_testcase_info(
        TESTPLAN, '1515033', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_reboot(self):
        rc = settingapi.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    @repeat_method(5)
    def test_03_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_102 = {
            f'{Parameter.X3_VLAN1_SUBNET}',
            f'{Parameter.X2_SUBNET}',
            '120',
            '1.1.1.0/24',
            '110',
        }
        flag = True if all(x in str(dyntb) for x in filter_102) else False
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


# Disable tunnel interface VPN policy
class Test_disableVPN_TC10(Test):
    uuid = "SOSAIOT-TC-54257"
    description = show_testcase_info(
        TESTPLAN, '1515032', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515036')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        uptade_option = {'enable':  False}
        ref1.update(uptade_option)
        rc1 = vpnapi.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc1, True, 'Edit VPN Policy Failed.')

    def test_03_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_10 = {
             f'{Parameter.X3_VLAN1_SUBNET}',
             f'{Parameter.X2_SUBNET}',
            '120',
            '1.1.1.0/24',
            '110',
        }
        flag = False if all(x in str(dyntb) for x in filter_10) else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")

    def test_04_enable_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        uptade_option = {'enable':  True}
        ref1.update(uptade_option)
        rc1 = vpnapi.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc1, True, 'Edit VPN Policy Failed.')


# static route doesn't appear in the OSPF route database of a peer when the Redistribute Static Routes check box is turned off
class Test_Ospf_TC68(Test):
    uuid = "SOSAIOT-TC-54269"
    description = show_testcase_info(
        TESTPLAN, '1515045', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515045')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': Parameter.X1_IP,
            'static_route': 'off',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute Static Networks: {res}')
        Assertion.assert_equal(
            res, True, "ERR:enable Redistribute Static Networks fail")

    def test_03_check_route_table(self):
        time.sleep(10)
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_08 = {
            '1.1.1.0/24',
            '110',
        }
        flag = False if all(x in str(dyntb) for x in filter_08) else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


# Disable OSPF on tunnel interface
class Test_disableOspf_TC09(Test):
    uuid = "SOSAIOT-TC-54276"
    description = show_testcase_info(
        TESTPLAN, '1515052', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_ospf_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        ospf_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'disable',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
        }
        res = dyrouteapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(
            res, True, "ERR: Failed To enable_passive_ospf on dut")

    def test_03_disable_ospf_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        ospf_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'disable',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
        }
        res = gwdyrouteapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(
            res, True, "ERR: Failed To enable_passive_ospf on dut")

    def test_04_check_route_table(self):
        filter_route = {
            f'{Parameter.FIREWALL}',
            'Full',
            'TI:test'
        }
        res = gwroutecli.show_ospf2(mode='neighbor')
        flag = False if all(x in str(res) for x in filter_route) else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


#   RIP: Disable RIP on tunnel interface
class Test_disableRip_TC07(Test):
    uuid = "SOSAIOT-TC-54270"
    description = show_testcase_info(
        TESTPLAN, '1515046', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_rip_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'disable',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.GW_X0_IP,
            'receive': '2',
            'send': '2',
        }
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on dut")

    def test_03_disable_rip_on_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'disable',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter.FIREWALL,
            'receive': '2',
            'send': '2',
        }
        resrip = gwdyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on lbox")

    def test_04_check_route_table(self):
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_06 = {
            f'{Parameter.X3_VLAN1_SUBNET}',
            f'{Parameter.X2_SUBNET}',
            '120',
        }
        flag =False if all(x in str(dyntb) for x in filter_06) else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


#  RIP: IP Address Borrowed From VLAN interface
class Test_enableRipBorrowedVlan_TC56(Test):
    uuid = "SOSAIOT-TC-54266"
    description = show_testcase_info(
        TESTPLAN, '1515042', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515042')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_rip_on_dut(self):
        tunnel_id = get_tunnel_id(dyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X3:V' + str(X3_VLAN1_ID),
            'UnnumDstIp': Parameter.GW_X0_IP,
            'receive': '2',
            'send': '2',
        }
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on dut")

    def test_03_enable_rip_on_gw(self):
        tunnel_id = get_tunnel_id(gwdyrouteapi, 'test')
        rip_dict = {
            'type': 'UnnumTI',
            'interface': 'test',
            'tunnel_id': tunnel_id,
            'mode': 'send_and_receive',
            'UnnumBorrowedIf': 'X0',
            'UnnumDstIp': Parameter. X3_VLAN1_IP,
            'receive': '2',
            'send': '2',
        }
        resrip = gwdyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(
            resrip, True, "ERR: Failed To enable rip on lbox")

    def test_04_check_route_table(self):
        dyntb = gwroutecli.show_route_policies(type='dynamic')
        filter_06 = {
            f'{Parameter.X2_SUBNET}',
            '120',
        }
        flag = True if all(x in str(dyntb) for x in filter_06) else False
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")