from definition.settings import *


class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_add_ipv6_route_on_pc1(self):
        cmds = [
            f'route -A inet6 add {Parameter.REMOTE_DEST_PREFIX} gw {Parameter.X0_V6_IP} dev eth1',
            'ip -6 route show dev eth1'
             ]
        res = PC1_Login.send_commands(cmds)
        logger.info(res)
        routecheck = f'{Parameter.REMOTE_DEST_PREFIX} via {Parameter.X0_V6_IP}'
        flag = True if routecheck in res else False
        Assertion.assert_equal(flag, True, "ERR: Add ipv6 route on pc1 failed")

