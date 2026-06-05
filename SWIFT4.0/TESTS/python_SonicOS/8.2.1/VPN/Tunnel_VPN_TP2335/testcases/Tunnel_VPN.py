from definition.settings import *
from definition.utils import *


class TestStaticRouteConfig_TC22(Test):
    uuid = "SOSAIOT-TC-54588"
    description = "Add a static route with Tunnel Interface selection on the Network > Routing page.",

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "StaticRouteConfig_TC22")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_check_added_static_route_policy(self):
        output = l_routepolicyapi.get_route_policy_by_name(name=VPNParams.local_route1_name)
        Assertion.assert_regular(str(output), 'localtivpn', "ERR: check added static route failed")


class TestStaticRouteConfig_TC23(Test):
    uuid = "SOSAIOT-TC-54589"
    description = "Added tunnel interface static route entry is enabled."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "StaticRouteConfig_TC23")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_TI_route_policy_must_active(self):
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'active', "ERR: check TI route policy must active failed")


class TestStaticRouteConfig_TC24(Test):
    uuid = "SOSAIOT-TC-54590"
    description = "Added tunnel interface static route entry is disabled and greyed out."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "StaticRouteConfig_TC24")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_disable_remote_TI_vpn(self):
        output = r_vpnbasesettingapi.dis_tunnelvpn_policy(**{"name": VPNParams.remote_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: disable remote ti vpn failed")

    @repeat_method(5)
    def test_02_check_TI_route_policy_must_inactive(self):
        logger.info('wait for 20s to make sure TI down...')
        time.sleep(20)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'inactive', "ERR: check TI route policy must inactive failed")

    def test_03_enable_remote_TI_vpn(self):
        output = r_vpnbasesettingapi.en_tunnelvpn_policy(**{"name": VPNParams.remote_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: enable remote ti vpn failed")

    @repeat_method(5)
    def test_04_check_TI_route_policy_must_active(self):
        logger.info('wait for 20s to make sure TI down...')
        time.sleep(20)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'active', "ERR: check TI route policy must active failed")


class TestACLConfig_TC27(Test):
    uuid = "SOSAIOT-TC-54591"
    description = "Auto-add Access Rule is enabled"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "ACLConfig_TC27")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_auto_add_access_rule_is_enabled(self):
        output = networkroute_api.show_route_policy_by_name(name=VPNParams.local_route1_name)
        Assertion.assert_regular(str(output),
                                 'auto_add_access_rules\': True',
                                 "ERR: check auto add access rule is enabled failed")

    def test_02_check_auto_added_lan_to_vpn_acl(self):
        logger.info('wait for 20s to make sure auto update acl...')
        time.sleep(20)
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['source']['address'] == {'name': 'X0 Subnet'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'remote_vpn_net'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get lan to vpn acl failed: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: check auto added lan to vpn acl failed")

    def test_03_check_auto_added_vpn_to_lan_acl(self):
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                logger.info(f'get target rule successful: {rule}')
                if rule['ipv4']['source']['address'] == {'name': 'remote_vpn_net'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'X0 Subnet'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get vpn to lan acl failed: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: check auto added vpn to lan acl failed")


class TestStaticRouteConfig_TC30(Test):
    uuid = "SOSAIOT-TC-54592"
    description = "Delete route. check acl."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "StaticRouteConfig_TC30")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_ti_route(self):
        output = networkroute_api.del_route_policy_by_name(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, True, "ERR: delete ti route failed")

    def test_02_check_auto_added_lan_to_vpn_not_in_acl(self):
        logger.info('wait for 20s to make sure auto update acl...')
        time.sleep(20)
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['source']['address'] == {'name': 'X0 Subnet'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'remote_vpn_net'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get lan to vpn acl failed: {repr(e)}')
        Assertion.assert_equal(res, False, "ERR: check auto added lan to vpn not in acl failed")

    def test_03_check_auto_added_vpn_to_lan_not_in_acl(self):
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                logger.info(f'get target rule successful: {rule}')
                if rule['ipv4']['source']['address'] == {'name': 'remote_vpn_net'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'X0 Subnet'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get vpn to lan acl failed: {repr(e)}')
        Assertion.assert_equal(res, False, "ERR: check auto added vpn to lan not in acl failed")

    def test_04_add_local_ti_route_policy(self):
        route_dict = {"route_policies": [{"ipv4": l_route_base_dict}]}
        res = networkroute_api.add_route_policy(**route_dict)
        Assertion.assert_equal(res, True, "ERR: Add local ti to route policy failed")


class TestStaticRouteConfig_TC34(Test):
    uuid = "SOSAIOT-TC-54593"
    description = "Added tunnel interface static route entry is disabled and greyed out."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "StaticRouteConfig_TC34")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_disable_local_TI_vpn(self):
        output = l_vpnbasesettingapi.dis_tunnelvpn_policy(**{"name": VPNParams.local_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: disable local ti vpn failed")

    @repeat_method(5)
    def test_02_check_TI_route_policy_must_inactive(self):
        logger.info('wait for 20s to make sure TI down...')
        time.sleep(20)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'inactive', "ERR: check TI route policy must inactive failed")

    def test_03_check_lan_to_vpn_acl_must_inactive(self):
        uuid = ''
        output = ''
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['source']['address'] == {'name': 'X0 Subnet'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'remote_vpn_net'}:
                    logger.info(f'get target rule successful: {rule}')
                    uuid = rule['ipv4']['uuid']
                    break
        except Exception as e:
            logger.info(f'get lan to vpn acl failed: {repr(e)}')
        if uuid:
            logger.info(f'get lan to vpn ti acl uuid: {uuid}')
            output = accessrule_api.check_accessrule_v4_status(uuid=uuid)
        else:
            logger.info('can not get lan to vpn ti policy in acl.')
        Assertion.assert_equal(output, 'inactive', "ERR: check lan to vpn acl must inactive failed")

    def test_04_check_vpn_to_lan_acl_must_inactive(self):
        uuid = ''
        output = ''
        getres = accessrule_api.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                logger.info(f'get target rule successful: {rule}')
                if rule['ipv4']['source']['address'] == {'name': 'remote_vpn_net'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'X0 Subnet'}:
                    logger.info(f'get target rule successful: {rule}')
                    uuid = rule['ipv4']['uuid']
                    break
        except Exception as e:
            logger.info(f'get vpn to lan acl failed: {repr(e)}')
        if uuid:
            logger.info(f'get vpn to lan ti acl uuid: {uuid}')
            output = accessrule_api.check_accessrule_v4_status(uuid=uuid)
        else:
            logger.info('can not get lan to vpn ti policy in acl.')
        Assertion.assert_equal(output, 'inactive', "ERR: check vpn to lan acl must inactive failed")

    def test_05_disable_local_TI_vpn(self):
        output = l_vpnbasesettingapi.en_tunnelvpn_policy(**{"name": VPNParams.local_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: disable local ti vpn failed")

    @repeat_method(5)
    def test_06_check_TI_route_policy_must_active(self):
        logger.info('wait for 20s to make sure TI up...')
        time.sleep(20)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'active', "ERR: check TI route policy must active failed")


class TestTITraffic_TC54(Test):
    uuid = "SOSAIOT-TC-54595"
    description = "traffic flows between networks."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "TITraffic_TC54")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_active_vpn_tunnel(self):
        output = l_vpnbasesettingapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), VPNParams.local_vpn1_name, "ERR: check active vpn tunnel failed")

    def test_02_check_local_to_remote_network_traffic(self):
        output = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: ping local host to remote host failed")


class TestPPPoETraffic_TC76(Test):
    uuid = "SOSAIOT-TC-54595"
    description = "traffic flows between networks."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "PPPoETraffic_TC76")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_x1_pppoe(self):
        res = interface_api.config_interface(**x1_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X1 pppoe ip failed!")

    @repeat_method(20)
    def test_02_verify_x1_can_get_ip_pppoe(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interface_api.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        ipres = resp.get("ip_address")
        Assertion.assert_equal(ipres, Parameter.X1_IP, "Error: X1 should obtain same IP with X1.")

    def test_03_check_local_to_remote_network_traffic(self):
        output = PC1_login.ping_from_eth(ip=PC5_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: ping local host to remote host failed")


class TestDHCPTraffic_TC78(Test):
    uuid = "SOSAIOT-TC-54603"
    description = "dhcp mode, VPN traffic is routed through."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "DHCPTraffic_TC78")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_X1_to_dhcp(self):
        x1_dhcp_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        output = interface_api.config_interface(**x1_dhcp_dict)
        interface_api.click_dhcp_renew(name='X1')
        Assertion.assert_equal(output, True, "ERR: Config X1 to dhcp failed")

    @repeat_method(20)
    def test_02_verify_x1_can_get_ip(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interface_api.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        ipres = resp.get("ip_address")
        Assertion.assert_equal(ipres, Parameter.X1_IP, "Error: X1 should obtain same IP with X1.")

    @repeat_method(20)
    def test_03_check_local_to_remote_network_traffic(self):
        time.sleep(10)
        output = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: ping local host to remote host failed")


class TestDHCPTraffic_TC79(Test):
    uuid = "SOSAIOT-TC-54604"
    description = "DHCP is disconnected, VPN traffic is not routed through."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "DHCPTraffic_TC79")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_disconnected_dhcp(self):
        PC5_login.send_command('systemctl stop dhcpd')
        output = interface_api.click_dhcp_release(name='X1')
        Assertion.assert_equal(output, True, "ERR: disconnected dhcp failed")

    @repeat_method(5)
    def test_02_check_TI_route_policy_must_inactive(self):
        logger.info('wait for 20s to make sure TI down...')
        time.sleep(20)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'inactive', "ERR: check TI route policy must inactive failed")

    def test_03_check_local_to_remote_network_traffic_must_fail(self):
        output = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, False, "ERR: ping local host to remote host must fail failed")

    def test_04_init_x1_configure(self):
        PC5_login.send_command('systemctl start dhcpd')
        output = interface_api.config_interface(**x1_static_dict)
        Assertion.assert_equal(output, True, "ERR: init x1 configure failed")


class TestBoundInterface_TC107(Test):
    uuid = "SOSAIOT-TC-54607"
    description = "VPN policy should be added after changed TI Route Based VPN Policy bound to interface",
    sec_tunnel_name = 'tc107_sectivpn'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "BoundInterface_TC107")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_x1_config_to_any_zones(self):
        output = []
        for zone in ['LAN', 'DMZ', 'WLAN']:
            commands = ['configure', 'interface X1',
                        f'ip-assignment {zone} static',
                        f'ip {Parameter.X1_IP}',
                        f'netmask {Parameter.MASK}',
                        'exit',
                        'management https',
                        'commit',
                        'end', 'commit', 'exit']
            msg = fw_cli.do_cli_commands(commands, tag=1)[1]
            if 'One WAN interface must be selected for Failover' in str(msg):
                output.append(True)
            else:
                output.append(False)
        logger.info(f'check config all zones in x1 result: {output}')
        Assertion.assert_equal(all(output), True, "ERR: check config to any zones failed")

    def test_02_config_X2_to_sec_wan(self):
        res = interface_api.config_interface(**x2_wan_dict)
        Assertion.assert_equal(res, True, "ERR: Config  X2 to sec wan failed")

    def test_03_add_sec_tunnel_vpn(self):
        sec_vpn_dict = {
            'type': 'tunnel_interface',
            'name': self.sec_tunnel_name,
            'pri_gate': Parameter.REMOTE_X2_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '44.44.44.44',
            'peer_ike_id': '44.44.44.44',

            'ike_exchange': 'ikev2',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 12000,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 12000,
            'bound_to': ['interface', 'X2'],

            'keep_alive': False,
        }
        output = l_vpnapi.add_vpn_policy(**sec_vpn_dict)
        Assertion.assert_equal(output, True, "ERR: add sec tunnel pvn failed")

    def test_04_init_sec_tunnel_vpn(self):
        output = l_vpnbasesettingapi.del_tunnelvpn_policy(**{'name': self.sec_tunnel_name})
        Assertion.assert_equal(output, True, "ERR: del sec tunnel pvn failed")


class TestDifferentBoundTo_TC89(Test):
    uuid = "SOSAIOT-TC-54608"
    description = "Add multiple tunnel interface policies with same gateway but different bound to interface"
    sec_tunnel_name = 'tc89_sectivpn'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "DifferentBoundTo_TC89")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_sec_tunnel_vpn_with_diff_bound(self):
        sec_vpn_dict = {
            'type': 'tunnel_interface',
            'name': self.sec_tunnel_name,
            'pri_gate': Parameter.REMOTE_X1_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '55.55.55.55',
            'peer_ike_id': '55.55.55.55',

            'ike_exchange': 'ikev2',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 300,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 180,
            'bound_to': ['interface', 'X2'],

            'keep_alive': True,
        }
        output = l_vpnapi.add_vpn_policy(**sec_vpn_dict)
        Assertion.assert_equal(output, True, "ERR: add sec tunnel pvn failed")

    def test_02_check_sec_vpn_in_policy_list(self):
        time.sleep(10)
        output = l_vpnbasesettingapi.show_tunnelvpnpolicy()
        Assertion.assert_regular(str(output), self.sec_tunnel_name, "ERR: check sec vpn in list failed")

    def test_03_init_sec_tunnel_vpn(self):
        output = l_vpnbasesettingapi.del_tunnelvpn_policy(**{'name': self.sec_tunnel_name})
        Assertion.assert_equal(output, True, "ERR: del sec tunnel vpn failed")


class TestSameBoundTo_TC90(Test):
    uuid = "SOSAIOT-TC-54609"
    description = "Attempt to add multiple tunnel interface policies with same gateway and same bound to interface"
    sec_tunnel_name = 'tc89_sectivpn'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "SameBoundTo_TC90")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_sec_tunnel_vpn_with_same_bound(self):
        sec_vpn_dict = {
            'type': 'tunnel_interface',
            'name': self.sec_tunnel_name,
            'pri_gate': Parameter.REMOTE_X1_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '55.55.55.55',
            'peer_ike_id': '55.55.55.55',

            'ike_exchange': 'ikev2',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 300,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 180,
            'bound_to': ['interface', 'X1'],

            'keep_alive': True,
        }
        output, msg = l_vpnapi.add_vpn_policy(msg=True, **sec_vpn_dict)
        if 'Duplicate IPsec Gateway Address Found' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: add sec tunnel vpn failed")


class TestDiffBoundToTraffic_TC94(Test):
    uuid = "SOSAIOT-TC-54620"
    description = "2 vpn with same gateway but different bound to interface. VPN traffic pass through secondary WAN."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "DiffBoundToTraffic_TC94")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ti_local_vpn2_local(self):
        ti_dict = copy.deepcopy(ti_vpn_dict)
        ti_dict.update({
            'name': VPNParams.local_vpn2_name,
            'pri_gate': Parameter.REMOTE_X2_IP,
            'local_ike_id': '55.55.55.55',
            'peer_ike_id': '55.55.55.55',
            'bound_to': ['interface', 'X2'],
        })
        output, msg = l_vpnapi.add_vpn_policy(msg=True, **ti_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: Add local ti vpn2 policy failed.")

    def test_02_add_ti_remote_vpn(self):
        ti_dict = copy.deepcopy(ti_vpn_dict)
        ti_dict.update({
            'name': VPNParams.remote_vpn2_name,
            'pri_gate': Parameter.X2_IP,
            'local_ike_id': '55.55.55.55',
            'peer_ike_id': '55.55.55.55',
            'bound_to': ['interface', 'X2'],
        })
        output, msg = r_vpnapi.add_vpn_policy(msg=True, **ti_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: Add local ti vpn policy failed.")

    def test_03_add_local_ti_route_bound_to_vpn2(self):
        edit_dict = copy.deepcopy(l_route_base_dict)
        edit_dict.update({
            "name": VPNParams.local_route2_name,
            "interface": VPNParams.local_vpn2_name,
        })
        local_route_dict = {"route_policies": [{"ipv4": edit_dict}]}
        networkroute_api.del_route_policy_by_name(name=VPNParams.local_route1_name)
        output, msg = networkroute_api.add_route_policy(msg=True, **local_route_dict)
        if 'Already exists' in str(msg):
            output = True
        # res = l_routepolicyapi.edit_route_policy(name=VPNParams.local_route1_name, **local_route_dict)
        Assertion.assert_equal(output, True, "ERR: add local ti route bound to vpn2 failed")

    def test_04_edit_remote_ti_route_bound_to_vpn2(self):
        edit_dict = copy.deepcopy(r_route_base_dict)
        edit_dict.update({
            "name": VPNParams.remote_route2_name,
            "interface": VPNParams.remote_vpn2_name,
        })
        remote_route_dict = {"route_policies": [{"ipv4": edit_dict}]}
        output, msg = r_routepolicyapi.add_route_policy(msg=True, **remote_route_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: Add remote ti route bound to vpn2 failed")

    @repeat_method(5)
    def test_05_check_ping_form_local_to_remote_network(self):
        logger.info("start verify ping from pc1 eth1 to remote host pc4 eth1... ")
        time.sleep(20)
        pingres = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: ping from pc1 eth1 to remote host pc4 eth1 failed")

    def test_06_check_active_vpn_tunnel(self):
        output = l_vpnbasesettingapi.get_active_vpn_tunnels()
        res = True if VPNParams.local_vpn2_name in str(output) and VPNParams.local_vpn1_name in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check active vpn tunnel failed")

    def test_07_check_ping_must_via_sec_vpn(self):
        request_filters = ['out:X2', 'IP Type: ESP', f'Dst=[{Parameter.REMOTE_X2_IP}]',
                           f'Src=[{Parameter.X2_IP}]', 'IPSec ESP Header']
        (reqres, packet) = check_capture_packets(request_filters)
        Assertion.assert_equal(reqres, True, "ERR: test traffic via route2 failed.")

    def test_08_init_vpn_and_route(self):
        res1 = l_vpnbasesettingapi.del_tunnelvpn_policy(**{'name': VPNParams.local_vpn2_name})
        res2 = r_vpnbasesettingapi.del_tunnelvpn_policy(**{'name': VPNParams.remote_vpn2_name})
        local_route_dict = {"route_policies": [{"ipv4": l_route_base_dict}]}
        res3, msg = networkroute_api.add_route_policy(msg=True, **local_route_dict)
        if 'Already exists' in str(msg):
            res3 = True
        logger.info(f'init vpn and route result: {res1, res2, res3}')
        Assertion.assert_equal(True, True, "ERR: init vpn add route failed.")


class TestChangeBoundTo_TC1563926(Test):
    uuid = "SOSAIOT-TC-54610"
    description = "'VPN Policy bound to' can be changed"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "ChangeBoundTo_TC1563926")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_change_vpn_bound_to(self):
        vpn_dict = {
            'enable': True,
            'edit_proposal': True,
            'edit_advanced': True,
            'type': 'tunnel_interface',
            'name': VPNParams.local_vpn1_name,
            'pri_gate': Parameter.REMOTE_X1_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '33.33.33.33',
            'peer_ike_id': '33.33.33.33',

            'ike_exchange': 'ikev2',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 300,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 180,
            'bound_to': ['interface', 'X2'],

            'keep_alive': True,
        }
        output = l_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(output, True, "ERR: show test case info failed")

    def test_02_check_vpn_bound_to(self):
        output = l_vpnbasesettingapi.show_tunnelvpnpolicy()
        Assertion.assert_regular(str(output), 'interface\': \'X2', "ERR: check sec vpn failed")

    def test_03_disable_local_TI_vpn(self):
        output = l_vpnbasesettingapi.dis_tunnelvpn_policy(**{"name": VPNParams.local_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: disable local ti vpn failed")

    def test_04_enable_local_TI_vpn(self):
        output = l_vpnbasesettingapi.en_tunnelvpn_policy(**{"name": VPNParams.local_vpn1_name})
        Assertion.assert_equal(output, True, "ERR: disable local ti vpn failed")

    def test_05_init_vpn_settings(self):
        vpn_dict = copy.deepcopy(ti_vpn_dict)
        vpn_dict.update({'enable': True,
                         'edit_proposal': True,
                         'edit_advanced': True, })
        output = l_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(output, True, "ERR: show test case info failed")


class TestRekey_TC61(Test):
    uuid = "SOSAIOT-TC-54612"
    description = "Rekey of IPSec SA has no impact on the routes and auto-added rules."

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "Rekey_TC61")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(5)
    def test_01_check_ping_form_local_to_remote_network(self):
        logger.info("start verify ping from pc1 eth1 to remote host pc4 eth1... ")
        time.sleep(10)
        pingres = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: ping from pc1 eth1 to remote host pc4 eth1 failed")

    def test_02_continuous_ping_in_vpn(self):
        pingres = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1', num=190)
        Assertion.assert_equal(pingres, True, "ERR: continuous ping in vpn failed")

    @repeat_method(5)
    def test_03_check_TI_route_policy_must_active(self):
        time.sleep(5)
        output = networkroute_api.show_route_policy_status(name=VPNParams.local_route1_name)
        Assertion.assert_equal(output, 'active', "ERR: check TI route policy must active failed")

    def test_04_check_lan_to_vpn_acl_must_active(self):
        uuid = ''
        output = ''
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['source']['address'] == {'name': 'X0 Subnet'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'remote_vpn_net'}:
                    logger.info(f'get target rule successful: {rule}')
                    uuid = rule['ipv4']['uuid']
                    break
        except Exception as e:
            logger.info(f'get lan to vpn acl failed: {repr(e)}')
        if uuid:
            logger.info(f'get lan to vpn ti acl uuid: {uuid}')
            output = accessrule_api.check_accessrule_v4_status(uuid=uuid)
        else:
            logger.info('can not get lan to vpn ti policy in acl.')
        Assertion.assert_equal(output, 'active', "ERR: check lan to vpn acl must active failed")

    def test_05_check_vpn_to_lan_acl_must_active(self):
        uuid = ''
        output = ''
        getres = accessrule_api.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                logger.info(f'get target rule successful: {rule}')
                if rule['ipv4']['source']['address'] == {'name': 'remote_vpn_net'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'X0 Subnet'}:
                    logger.info(f'get target rule successful: {rule}')
                    uuid = rule['ipv4']['uuid']
                    break
        except Exception as e:
            logger.info(f'get vpn to lan acl failed: {repr(e)}')
        if uuid:
            logger.info(f'get vpn to lan ti acl uuid: {uuid}')
            output = accessrule_api.check_accessrule_v4_status(uuid=uuid)
        else:
            logger.info('can not get lan to vpn ti policy in acl.')
        Assertion.assert_equal(output, 'active', "ERR: check vpn to lan acl must active failed")


class TestUnnumberTIConfig_TC100(Test):
    uuid = "SOSAIOT-TC-54584"
    description = "Unnumber TI policy will be replaced by Number interface in static routing->interface"
    tunnel_inter_name = 'AutoNITest'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "UnnumberTIConfig_TC100")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_tunnel_interface(self):
        output, msg = interface_api.add_interface(msg=True, **unnumber_ti_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: add tunnel interface failed")

    def test_02_add_unnumber_ti_in_route(self):
        edit_dict = copy.deepcopy(l_route_base_dict)
        edit_dict.update({
            "name": VPNParams.local_route1_name,
            "interface": self.tunnel_inter_name,
        })
        local_route_dict = {"route_policies": [{"ipv4": edit_dict}]}
        networkroute_api.del_route_policy_by_name(name=VPNParams.local_route1_name)
        output, msg = networkroute_api.add_route_policy(msg=True, **local_route_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: add unnumber ti in route failed")

    def test_03_check_unnumber_ti_in_route(self):
        output = l_routepolicyapi.get_route_policy_by_name(name=VPNParams.local_route1_name)
        Assertion.assert_regular(str(output), VPNParams.local_route1_name, "ERR: check unnumber ti in route failed")


class TestUnnumberTIConfig_TC103(Test):
    uuid = "SOSAIOT-TC-54586"
    description = "Disable and Enable 'Auto-add Access Rule' on Unnumber TI"
    tunnel_inter_name = 'AutoNITest'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "UnnumberTIConfig_TC103")
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_disable_auto_add_acl_with_unnumber_ti_in_route(self):
        base_dict = copy.deepcopy(edit_local_route_dict)
        base_dict.update({
            "interface": self.tunnel_inter_name,
            "name": VPNParams.local_route1_name,
            "auto_add_access_rules": False
        })
        local_route_dict = {"route_policies": [{"ipv4": base_dict}]}
        output = l_routepolicyapi.edit_route_policy(name=VPNParams.local_route1_name, **local_route_dict)
        Assertion.assert_equal(output, True, "ERR: disable auto add acl with unnumber ti in route failed")

    def test_02_check_not_auto_added_lan_to_vpn_acl(self):
        logger.info('wait for 20s to make sure auto update acl...')
        time.sleep(20)
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['source']['address'] == {'name': 'X0 Subnet'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'remote_vpn_net'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get lan to vpn acl failed: {repr(e)}')
        Assertion.assert_equal(res, False, "ERR: check not auto added lan to vpn acl failed")

    def test_03_check_not_auto_added_vpn_to_lan_acl(self):
        res = False
        getres = accessrule_api.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                logger.info(f'get target rule successful: {rule}')
                if rule['ipv4']['source']['address'] == {'name': 'remote_vpn_net'} \
                        and rule['ipv4']['destination']['address'] == {'name': 'X0 Subnet'}:
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except Exception as e:
            logger.info(f'get vpn to lan acl failed: {repr(e)}')
        Assertion.assert_equal(res, False, "ERR: check not auto added vpn to lan acl failed")

    def test_04_init_vpn_and_route(self):
        networkroute_api.del_route_policy_by_name(name=VPNParams.local_route1_name)
        res1 = interface_api.del_interface(**unnumber_ti_dict)
        local_route_dict = {"route_policies": [{"ipv4": l_route_base_dict}]}
        res2, msg = networkroute_api.add_route_policy(msg=True, **local_route_dict)
        if 'Already exists' in str(msg):
            res2 = True
        logger.info(f'init vpn and route result: {res1, res2}')
        Assertion.assert_equal(True, True, "ERR: init vpn add route failed.")


