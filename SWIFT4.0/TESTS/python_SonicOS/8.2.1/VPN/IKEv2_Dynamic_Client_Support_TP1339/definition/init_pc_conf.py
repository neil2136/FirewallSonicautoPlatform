from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_route_to_local_x0_subnet_on_pc3_eth1(self):
        cmds = [f'route add -net {Parameter.X2_NET} netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                'ip -4 r']
        output = PC3_Login.send_commands(cmds)
        flag = True if f'{Parameter.X2_NET}/24 via {Parameter.X3_REMOTE_IP} dev eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: add route to local x2 subnet on PC3 failed")

    def test_02_add_route_to_remote_x3_subnet_on_pc2_eth1(self):
        cmds = [f'route add -net {Parameter.X3_REMOTE_NET} netmask {Parameter.MASK} gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_Login.send_commands(cmds)
        flag = True if f'{Parameter.X3_REMOTE_NET}/24 via {Parameter.X2_IP} dev eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: add route to remote x3 subnet on PC2 failed")
