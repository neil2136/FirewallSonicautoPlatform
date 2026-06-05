from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    def test_01_setup_iodline_server_on_pc3(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master','make', 'make install']
        pc3_login.send_commands(cmds)
        out = pc3_login.send_command(f'ls -l {install_iodine_path}/bin/iodined')
        Assertion.assert_regular(out, 'iodined', 'ERR: install iodine failed on PC3')

    def test_02_setup_iodline_client_on_pc1(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master', 'make', 'make install']
        pc1_login.send_commands(cmds)
        res = os.path.exists('/tmp/iodine-master/bin/iodine')
        Assertion.assert_equal(res, True, 'ERR: install iodine failed on PC1')

    def test_03_setup_iodline_client_on_pc2(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master', 'make', 'make install']
        pc2_login.send_commands(cmds)
        out = pc2_login.send_command(f'ls -l {install_iodine_path}/bin/iodine')
        Assertion.assert_regular(out, 'iodine', 'ERR: install iodine failed on PC2')

    def test_04_setup_iodline_client_on_pc4(self):
        cmds = [f'cp -r {iodine_path} /tmp/', 'cd /tmp/iodine-master', 'make', 'make install']
        pc4_login.send_commands(cmds)
        out = pc4_login.send_command(f'ls -l {install_iodine_path}/bin/iodine')
        Assertion.assert_regular(out, 'iodine', 'ERR: install iodine failed on PC4')

    def test_05_add_route_on_pc1(self):
        pc1_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.FIREWALL}')
        pc2_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.FIREWALL}')
        pc4_login.send_command(f'route add -net {Parameter.X1_NET}/24 gateway {Parameter.X2_IP}')
        out1 = pc1_login.send_command('ip -4 route')
        out2 = pc2_login.send_command('ip -4 route')
        out3 = pc4_login.send_command('ip -4 route')
        res1 = True if f'{Parameter.X1_NET}/24 via {Parameter.FIREWALL} dev eth1' in out1 else False
        res2 = True if f'{Parameter.X1_NET}/24 via {Parameter.FIREWALL} dev eth1' in out2 else False
        res3 = True if f'{Parameter.X1_NET}/24 via {Parameter.X2_IP} dev eth1' in out3 else False
        Assertion.assert_equal(res1&res2&res3, True, "ERR: add route on PC1&PC2&PC3 failed.")
