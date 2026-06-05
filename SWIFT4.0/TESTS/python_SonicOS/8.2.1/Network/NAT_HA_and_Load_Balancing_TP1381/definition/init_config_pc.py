from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_routes_on_pc(self):
        pc1_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.FIREWALL}')
        pc2_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.X1_IP}')
        pc4_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.X1_IP}')
        out1 = pc1_login.send_command('ip -4 r')
        out2 = pc2_login.send_command('ip -4 r')
        out3 = pc4_login.send_command('ip -4 r')
        rc2 = f'{Parameter.X1_NET}/24 via {Parameter.X1_IP} dev eth1' in out2
        rc3 = f'{Parameter.X1_NET}/24 via {Parameter.X1_IP} dev eth1' in out3
        rc1 = f'{Parameter.X1_NET}/24 via {Parameter.FIREWALL} dev eth1' in out1
        Assertion.assert_equal(rc1&rc2&rc3, True, "\033[1;31mERR: config routes on pc failed!\033[0m")
