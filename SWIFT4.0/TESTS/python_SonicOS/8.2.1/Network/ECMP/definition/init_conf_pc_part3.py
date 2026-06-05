from definition.settings_part3 import *
from definition.utils_part2 import *

class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_Get_PC_MAC(self):
        res1 = Parameter.GW1_MAC = get_pc_int_mac(PC_GW1_Login, 'eth2')
        logger.info(f'GW1_MAC is :{Parameter.GW1_MAC}')

        res2 = Parameter.GW2_MAC = get_pc_int_mac(PC_GW2_Login, 'eth2')
        logger.info(f'GW2_MAC is :{Parameter.GW2_MAC}')

        res3 = Parameter.GW3_MAC = get_pc_int_mac(PC_GW3_Login, 'eth2')
        logger.info(f'GW3_MAC is :{Parameter.GW3_MAC}')

        res4 = Parameter.GW4_MAC = get_pc_int_mac(PC_GW4_Login, 'eth2')
        logger.info(f'GW4_MAC is :{Parameter.GW4_MAC}')

        res5 = Parameter.GW5_MAC = get_pc_int_mac(PC_GW5_Login, 'eth2')
        logger.info(f'GW5_MAC is :{Parameter.GW5_MAC}')

        flag = True if res1 and res2 and res3 and res4 and res5 else False

        Assertion.assert_equal(flag, True, "ERR: get pc mac failed")

    def test_02_Add_route_in_PC1(self):
        pc1_cmds = [
            f'route add -net {Parameter.SERVER_NET}/24 gw {Parameter.X0_IP} dev eth1',
            f'route -A inet6 add {Parameter.SERVER_NET_V6} gw {Parameter.X0_IPV6} dev eth1',
            'ip -4 route show dev eth1',
            'ip -6 route show dev eth1']
        res = PC1_Login.send_commands(pc1_cmds)
        routecheck1 = f'{Parameter.SERVER_NET}/24 via {Parameter.X0_IP}'
        logger.info(routecheck1)
        routecheck2 = f'{Parameter.SERVER_NET_V6} via {Parameter.X0_IPV6}'
        logger.info(routecheck2)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add  route on pc1 failed")

    def test_03_Add_default_route_in_PC_Server(self):
        cmds1 = [
            "route add -net 13.0.11.0/24 gw 100.100.11.11 dev eth1",
            "route add -net 13.0.12.0/24 gw 100.100.12.12 dev eth1",
            "route add -net 13.0.13.0/24 gw 100.100.13.13 dev eth1",
            "route add -net 13.0.14.0/24 gw 100.100.14.14 dev eth1",
            "route add -net 13.0.15.0/24 gw 100.100.15.15 dev eth1",
            'ip -4 route show dev eth1']
        cmds2 = [
            f'route -A inet6 add 2001:2011::/64 gw 2001:1000::11 dev eth1',
            f'route -A inet6 add 2001:2012::/64 gw 2001:1000::12 dev eth1',
            f'route -A inet6 add 2001:2013::/64 gw 2001:1000::13 dev eth1',
            f'route -A inet6 add 2001:2014::/64 gw 2001:1000::14 dev eth1',
            f'route -A inet6 add 2001:2015::/64 gw 2001:1000::15 dev eth1',
            'ip -6 route show dev eth1']
        res1 = PC_Server_Login.send_commands(cmds1)
        res2 = PC_Server_Login.send_commands(cmds2)
        logger.info(res1.count('13.0.1'))
        logger.info(res2.count('2001:201'))
        flag = True if res1.count('13.0.1') == res2.count('2001:201') == 5 else False
        Assertion.assert_equal(flag, True, "ERR: Add  route on pc server failed")

    def test_04_add_route_on_GW1(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X1_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X1_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X1_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X1_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)

        res = PC_GW1_Login.send_commands(cmds)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add route on pc_gw failed")

    def test_05_add_route_on_GW2(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X2_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X2_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X2_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X2_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)
        res = PC_GW2_Login.send_commands(cmds)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add route on pc_gw failed")

    def test_06_add_route_on_GW3(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X3_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X3_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X3_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)
        res = PC_GW3_Login.send_commands(cmds)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add route on pc_gw failed")

    def test_07_add_route_on_GW4(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X4_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X4_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X4_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X4_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)
        res = PC_GW4_Login.send_commands(cmds)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add route on pc_gw failed")

    def test_08_add_route_on_GW5(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X5_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X5_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X5_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X5_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)
        res = PC_GW5_Login.send_commands(cmds)
        flag = True if routecheck1 in res and routecheck2 in res else False
        Assertion.assert_equal(flag, True, "ERR: Add route on pc_gw failed")