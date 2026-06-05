from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_setup_iodline_server_on_pc3(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master','make', 'make install']
        pc3_login.send_commands(cmds)
        out = pc3_login.send_command('ls -l /tmp/iodine-master/bin/iodined')
        Assertion.assert_regular(out, 'iodine', 'ERR: install iodine failed on PC2')

    def test_02_setup_iodline_client_on_pc1(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master', 'make', 'make install']
        pc1_login.send_commands(cmds)
        res = os.path.exists('/tmp/iodine-master/bin/iodine')
        Assertion.assert_equal(res, True, 'ERR: install iodine failed on PC1')

    def test_03_setup_iodline_client_on_pc2(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master', 'make', 'make install']
        pc2_login.send_commands(cmds)
        out = pc2_login.send_command('ls -l /tmp/iodine-master/bin/iodine')
        Assertion.assert_regular(out, 'iodine', 'ERR: install iodine failed on PC2')

    def test_04_add_route_on_pc1(self):
        pc1_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.FIREWALL}')
        pc2_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.FIREWALL}')
        out1 = pc1_login.send_command('ip -4 route')
        out2 = pc2_login.send_command('ip -4 route')
        res1 = f'{Parameter.X1_NET}/24 via {Parameter.FIREWALL} dev eth1' in out1
        res2 = f'{Parameter.X1_NET}/24 via {Parameter.FIREWALL} dev eth1' in out2
        Assertion.assert_equal(res1 & res2, True, "ERR: add route on PC1&PC2 failed.")
