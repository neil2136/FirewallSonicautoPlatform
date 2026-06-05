from definition.settings import *


class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_add_ipv6_address_for_eth1_on_pc1(self):
        cmds = [f'ip addr add {PC1_ETH1_IPv6}/64 dev eth1',
                'ifconfig eth1']
        output = PC1_Login.send_commands(cmds)
        flag = True if PC1_ETH1_IPv6 in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: add ipv6 address for eth1 on pc1 failed")

    def test_02_add_ipv6_address_for_eth1_on_pc2(self):
        cmds = [f'ip addr add {PC2_ETH1_IPv6}/64 dev eth1',
                'ifconfig eth1']
        output = PC2_Login.send_commands(cmds)
        flag = True if PC2_ETH1_IPv6 in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: add ipv6 address for eth1 on pc2 failed")

    def test_03_add_ipv6_address_for_eth1_on_pc3(self):
        cmds = [f'ip addr add {PC3_ETH1_IPv6}/64 dev eth1',
                'ifconfig eth1']
        output = PC3_Login.send_commands(cmds)
        flag = True if PC3_ETH1_IPv6 in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: add ipv6 address for eth1 on pc3 failed")

    def test_04_add_ipv6_route_on_pc1(self):
        cmds = [
            f'route -A inet6 add {Parameter.R_X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} gw {Parameter.X0_V6_IP} dev eth1',
            'ip -6 route show dev eth1'
        ]
        res = PC1_Login.send_commands(cmds)
        logger.info(res)
        routecheck = f'{Parameter.R_X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} via {Parameter.X0_V6_IP}'
        Assertion.assert_regular(res, routecheck, "ERR: Add ipv6 route on pc1 failed")

    def test_05_add_ipv6_route_on_pc2(self):
        cmds = [
            f'route -A inet6 add {Parameter.R_X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} gw {Parameter.X3_V6_IP} dev eth1',
            'ip -6 route show dev eth1'
        ]
        res = PC2_Login.send_commands(cmds)
        logger.info(res)
        routecheck = f'{Parameter.R_X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} via {Parameter.X3_V6_IP}'
        Assertion.assert_regular(res, routecheck, "ERR: Add ipv6 route on pc2 failed")

    def test_06_add_route_on_pc3(self):
        cmds = [
            f'route -A inet6 add {Parameter.X0_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} gw {Parameter.R_X3_IPV6} dev eth1',
            f'route -A inet6 add {Parameter.X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} gw {Parameter.R_X3_IPV6} dev eth1',
            'ip -6 route show dev eth1'
        ]
        res = PC3_Login.send_commands(cmds)
        logger.info(res)
        routelist = [f'{Parameter.X0_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} via {Parameter.R_X3_IPV6}',
                     f'{Parameter.X3_V6_PREFIX}/{Parameter.PREFIX_LENGTH_1} via {Parameter.R_X3_IPV6}'
                     ]
        flag = True if all(i in res for i in routelist) else False
        Assertion.assert_equal(flag, True, "ERR: Add ipv6 route on pc3 failed")
