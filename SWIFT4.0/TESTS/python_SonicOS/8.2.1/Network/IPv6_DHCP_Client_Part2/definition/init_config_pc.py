from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    dibbler_file = 'server_1.conf'
    pc = pc2_login

    def test_01_setup_dhcpv6_server_on_pc2(self):
        cmd_list = ['dibbler-server stop',
                    f'timeout 5\cp {server_conf_path}/radvd.conf /etc/',
                    f'timeout 5 \cp {server_conf_path}/{self.dibbler_file} /etc/dibbler/server.conf',
                    f'timeout 5 \cp {server_conf_path}/sysctl.conf /etc/',
                    'timeout 5 sysctl -p',
                    'timeout 5 systemctl restart radvd']
        self.pc.send_commands(cmd_list)
        self.pc.send_command('dibbler-server run > /var/log/dibbler.log &')
        sleep(3)
        out = self.pc.send_command('dibbler-server status')
        Assertion.assert_regular(out, 'Dibbler server: RUNNING', 'ERR: start server on pc2 failed.')

    def test_02_setup_dhcpv6_server_on_pc3(self):
        self.dibbler_file = 'server_2.conf'
        self.pc = pc3_login
        self.test_01_setup_dhcpv6_server_on_pc2()
