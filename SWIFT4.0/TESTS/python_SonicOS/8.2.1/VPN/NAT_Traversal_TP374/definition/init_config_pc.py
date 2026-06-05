from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_cfg_routes_for_pc(self):
        pc1_login.send_command(f'route add -net 12.12.2.0/24 gw {Parameter.FIREWALL}')
        pc2_login.send_command(f'route add -net 192.168.168.0/24 gw {Parameter.REM_X2_IP}')
        out1 = pc1_login.send_command('ip -4 route')
        out2 = pc2_login.send_command('ip -4 route')
        res = f'12.12.2.0/24 via {Parameter.FIREWALL} dev eth1' in out1 and f'192.168.168.0/24 via {Parameter.REM_X2_IP} dev eth1' in out2
        Assertion.assert_equal(res, True, 'ERR: config routes on pc failed.')
