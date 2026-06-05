from definition.settings_part2 import *
from definition.utils_part2 import *


class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_Get_PC_MAC(self):
        res1 = Parameter.X2_GW1_MAC = get_pc_int_mac(PC_GW1_Login, 'eth2')
        logger.info(f'X2_GW1_MAC is :{Parameter.X2_GW1_MAC}')

        res2 = Parameter.X2_GW2_MAC = get_pc_int_mac(PC_GW2_Login, 'eth2')
        logger.info(f'X2_GW2_MAC is :{Parameter.X2_GW2_MAC}')

        res3 = Parameter.X2_GW3_MAC = get_pc_int_mac(PC_GW3_Login, 'eth2')
        logger.info(f'X2_GW3_MAC is :{Parameter.X2_GW3_MAC}')

        res4 = Parameter.X2_GW4_MAC = get_pc_int_mac(PC_GW4_Login, 'eth2')
        logger.info(f'X2_GW4_MAC is :{Parameter.X2_GW4_MAC}')

        flag = True if res1 and res2 and res3 and res4 else False

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
            'route add -net 13.12.1.0/24 gw 100.100.11.11 dev eth1',
            'route add -net 13.12.2.0/24 gw 100.100.12.12 dev eth1',
            'route add -net 13.12.3.0/24 gw 100.100.13.13 dev eth1',
            'route add -net 13.12.4.0/24 gw 100.100.14.14 dev eth1',
            'ip -4 route show dev eth1']
        cmds2 = [
            'route -A inet6 add 2001:2012:12:12:1001::/96 gw 2001:1000:1000:1000:11::10 dev eth1',
            'route -A inet6 add 2001:2012:12:12:1002::/96 gw 2001:1000:1000:1000:12::10 dev eth1',
            'route -A inet6 add 2001:2012:12:12:1003::/96 gw 2001:1000:1000:1000:13::10 dev eth1',
            'route -A inet6 add 2001:2012:12:12:1004::/96 gw 2001:1000:1000:1000:14::10 dev eth1',
            'ip -6 route show dev eth1']
        res1 = PC_Server_Login.send_commands(cmds1)
        res2 = PC_Server_Login.send_commands(cmds2)
        logger.info(res1.count('13.12.'))
        logger.info(res2.count('2001:2012:12:12:100'))
        flag = True if res1.count('13.12.') == res2.count('2001:2012:12:12:100') == 4 else False
        Assertion.assert_equal(flag, True, "ERR: Add  route on pc server failed")

    def test_04_add_ipv6_route_on_GW(self):
        cmds = [
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X2_IP} dev eth2',
            f'route -A inet6 add {Parameter.X0_NET_V6} gw {Parameter.X2_IPV6} dev eth2',
            'ip -4 route show dev eth2',
            'ip -6 route show dev eth2']
        routecheck1 = f'{Parameter.X0_NET}/24 via {Parameter.X2_IP}'
        routecheck2 = f'{Parameter.X0_NET_V6} via {Parameter.X2_IPV6}'
        logger.info(routecheck1)
        logger.info(routecheck2)
        pc_obj_list = [PC_GW1_Login, PC_GW2_Login, PC_GW3_Login, PC_GW4_Login]
        res_list = []
        for pc_obj in pc_obj_list:
            res = pc_obj.send_commands(cmds)
            flag = True if routecheck1 in res and routecheck2 in res else False
            pc_obj.ping_from_eth(Parameter.X2_IP, 'eth2', num=2)
            res_list.append(flag)
        Assertion.assert_equal(all(res_list), True, "ERR: Add route on pc_gw failed")



