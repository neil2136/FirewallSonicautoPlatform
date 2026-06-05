from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_start_http_server_on_pc2(self):
        cmds = [
            'systemctl start httpd.service',
            'systemctl status httpd.service'
        ]
        res = PC2_Login.send_commands(cmds)
        flag = True if 'Started The Apache HTTP Server' in res else False
        Assertion.assert_equal(flag, True, "ERR: start http server on PC2 failed")

    def test_02_add_route_to_local_x0_subnet_on_pc4_eth1(self):
        cmds = [f'route add -net {Parameter.X0_NET} netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                f'route add -net 11.1.1.0 netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                'ip -4 r']
        checklist = [f'{Parameter.X0_NET}/24 via {Parameter.X3_REMOTE_IP} dev eth1',
                     f'11.1.1.0/24 via {Parameter.X3_REMOTE_IP} dev eth1']
        output = PC4_Login.send_commands(cmds)
        checkres = [i in output for i in checklist]
        logger.info(f' check result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: add route to local x0 subnet on PC4 failed")

    def test_03_add_route_to_local_x0_subnet_on_pc5_eth1(self):
        cmds = [f'route add -net {Parameter.X0_NET} netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                'ip -4 r']
        output = PC5_Login.send_commands(cmds)
        flag = True if f'{Parameter.X0_NET}/24 via {Parameter.X3_REMOTE_IP} dev eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: add route to local x0 subnet on PC5 failed")
