from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    
    def test_01_add_route(self):
        route_v4 = f'route add -net 12.12.1.0/24 gateway {Parameter.FIREWALL}'
        route_v6 = f'ip -6 route add 2001::/64 via {Parameter.X0_V6_IP}'
        pc1_login.send_command(route_v4)
        pc1_login.send_command(route_v6)
        output1 = pc1_login.send_command('ip -4 route')
        output2 = pc1_login.send_command('ip -6 route')
        res1 = True if f'12.12.1.0/24 via {Parameter.FIREWALL}' in output1 else False
        res2 = True if f'2001::/64 via {Parameter.X0_V6_IP}' in output2 else False
        Assertion.assert_equal(res1&res2, True, 'config routes on PC1 failed.')
        