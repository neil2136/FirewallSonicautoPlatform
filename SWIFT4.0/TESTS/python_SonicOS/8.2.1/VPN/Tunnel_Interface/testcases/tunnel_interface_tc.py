from definition.settings import *


class TestTunnel_Interface_01(Test):
    uuid = "SOSAIOT-TC-54511"
    description= show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_01_add_vpn_tunnel(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Tunnel'))
        rc = Lvpn_obj.add_vpn_policy(**Lvpn)
        Assertion.assert_equal(rc,True,'Add VPN Tunnel Failed.')

    def test_01_02_add_tunnel_interface(self):
        logger.info(" {} ".center(20, '*').format('Add Local Tunnel Interface'))
        rc = LIntObj.add_interface(**LInt_tunnel)
        Assertion.assert_equal(rc, True, "ERR: Add Local Tunnel Interface Failed")

    def test_01_03_remove_tunnel_interface(self):
        logger.info(" {} ".center(20, '-').format('Delete Local Tunnel Interface'))
        rc = LIntObj.del_interface(**LInt_tunnel)
        Assertion.assert_equal(rc,True,'Remove Local VPN Tunnel Failed.')

    def test_01_04_remove_vpn_tunnel(self):
        logger.info(" {} ".center(20, '-').format('Delete Local VPN Tunnel'))
        rc = Lvpn_obj.del_tunnelvpn_policy(**Lvpn)
        Assertion.assert_equal(rc,True,'Remove Local VPN Tunnel Failed.')


class TestTunnel_Interface_02(Test):
    uuid = "SOSAIOT-TC-54521"
    description= show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_conf_rip_for_TI(self):
        logger.info(" {} ".center(20, '*').format('conf rip for Local TI'))
        rc1 = LRouteObj.config_rip(**LRip_opt)
        logger.info(" {} ".center(20, '*').format('conf rip for rmt TI'))
        rc2 = RRouteObj.set_route("advanced")
        rc2 &= RRouteObj.config_rip(**RRip_opt)
        Assertion.assert_equal(rc1&rc2, True, "ERR: conf rip for TI Failed")

    def test_02_02_initiate_continuous_pings_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping 172.16.1.15 -c 1").read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from PC1 to PC2.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_03_recover_rip_for_TI(self):
        logger.info(" {} ".center(20, '*').format('delete rip for Local TI'))
        LRip_opt = {
            'if': LInt_tunnel['tunnel_name'],
            'network': '1.1.1.0/24', 
            'type': 'disable',
            'redistribute': False, 
        }
        rc1 = LRouteObj.config_rip(**LRip_opt)
        logger.info(" {} ".center(20, '*').format('delete rip for rmt TI'))
        RRip_opt = {
            'if': RInt_tunnel['tunnel-name'],
            'network': '1.1.1.0/24', 
            'type': 'disable',
            'redistribute': False, 
        }
        rc2 = RRouteObj.config_rip(**RRip_opt)
        Assertion.assert_equal(rc1&rc2, True, "ERR: delete rip for TI Failed")


class TestTunnel_Interface_03(Test):
    uuid = "SOSAIOT-TC-54525"
    description= show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_conf_ospf_for_TI(self):
        logger.info(" {} ".center(20, '*').format('conf ospf for Local TI'))
        rc1 = LRouteObj.config_ospf(**LOspf_opt)
        logger.info(" {} ".center(20, '*').format('conf ospf for rmt TI'))
        rc2 = RRouteObj.config_ospf(**ROspf_opt)
        Assertion.assert_equal(rc1&rc2, True, "ERR: conf ospf for TI Failed")

    def test_03_02_initiate_continuous_pings_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping 172.16.1.15 -c 1").read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from PC1 to PC2.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_03_recover_ospf_for_TI(self):
        logger.info(" {} ".center(20, '*').format('delete ospf for Local TI'))
        LOspf_opt = {
            'if': LInt_tunnel['tunnel_name'],
            'type': 'disable',
            'network': '1.1.1.0/24',
            'redistribute': False, 
            'area': '10',
        }
        rc1 = LRouteObj.config_ospf(**LOspf_opt)
        logger.info(" {} ".center(20, '*').format('delete ospf for rmt TI'))
        ROspf_opt = {
            'if': RInt_tunnel['tunnel-name'],
            'type': 'disable',
            'network': '1.1.1.0/24',
            'redistribute': False, 
            'area': '10',
        }
        rc2 = RRouteObj.config_ospf(**ROspf_opt)
        Assertion.assert_equal(rc1&rc2, True, "ERR: delete ospf for TI Failed")


class TestTunnel_Interface_04(Test):
    uuid = "SOSAIOT-TC-54529"
    description= show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_conf_bgp_for_TI(self):
        cmds = ['configure',
                'routing',
                'bgp',
                'conf t',
                'router bgp 2', 
                'network 1.1.1.0/24',
                'exit',]
        logger.info(" {} ".center(20, '*').format('conf bgp for Local TI'))
        rc1 = fw_cli.do_cli_commands(cmds)
        logger.info(" {} ".center(20, '*').format('conf bgp for rmt TI'))
        rc2 = rmt.do_cli_commands(cmds)
        Assertion.assert_equal(rc1&rc2, True, "ERR: conf bgp for TI Failed")

    def test_04_03_initiate_continuous_pings_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping 172.16.1.15 -c 1").read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from PC1 to PC2.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_03_recover_bgp_for_TI(self):
        logger.info(" {} ".center(20, '*').format('delete bgp for Local TI'))
        LRip_opt = {
            'if': LInt_tunnel['tunnel_name'],
            'network': '1.1.1.0/24', 
            'type': 'disable',
        }
        rc1 = LRouteObj.config_ospf(**LInt_tunnel)
        logger.info(" {} ".center(20, '*').format('delete bgp for rmt TI'))
        RRip_opt = {
            'if': LInt_tunnel['tunnel_name'],
            'network': '2.2.2.0/24', 
            'type': 'disable',
        }
        rc2 = RRouteObj.config_ospf(**RInt_tunnel)
        Assertion.assert_equal(rc1&rc2, True, "ERR: delete bgp for TI Failed")


class TestTunnel_Interface_09(Test):
    uuid = "SOSAIOT-TC-54561"
    description= show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_01_add_static_route_policy_for_TI(self):
        logger.info(" {} ".center(20, '*').format('conf static route for Local TI'))
        rc1 = LRoutePolicyObj.add_route_policy(**LRoute_policy)
        logger.info(" {} ".center(20, '*').format('conf static route for rmt TI'))
        rc2 = RRoutePolicyObj.add_route_policy(**RRoute_policy)
        Assertion.assert_equal(rc1&rc2, True, "ERR: conf static route for TI Failed")

    def test_09_02_add_LAN_to_VPN_ACL_for_TI(self):
        logger.info(" {} ".center(20, '*').format('add lan to vpn access rule'))
        # rc1 = accessRuleApi.add_ipv4_access_rule(**access_rule_option)
        # logger.info(" {} ".center(20, '*').format('add route from pc1 to TI'))
        output = os.popen("route add -net 1.1.1.0/24 gw 192.168.168.168").read()
        output = os.popen("route -n").read()
        if ('1.1.1.0' in output):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: conf rip for TI Failed")

    def test_09_03_initiate_continuous_pings_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("curl https://1.1.1.1 -k").read()
            if ('SonicWall Administrator' in out):
                logger.info('Successfully login to RMT via TI.')
                rc = True
                break
            else:
                rc = False
        Assertion.assert_equal(rc, True, "ERR: login to RMT via TI failed")

    def test_09_04_delete_static_route_for_TI(self):
        logger.info(" {} ".center(20, '*').format('delete static route policy'))
        rc1 = LRoutePolicyObj.del_route_policy_by_name('static_rm')
        rc2 = RRoutePolicyObj.del_route_policy_by_name('static_local')
        Assertion.assert_equal(rc1&rc2, True, "ERR: delete static route policy Failed")

    def test_09_05_restore_route(self):
        # logger.info(" {} ".center(20, '*').format('add lan to vpn access rule'))
        # rc = accessRuleApi.add_ipv4_access_rule(**access_rule_option)
        logger.info(" {} ".center(20, '*').format('restore route in PC1'))
        output = os.popen("service network restart").read()
        if ('done' in output):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: restore route Failed")
