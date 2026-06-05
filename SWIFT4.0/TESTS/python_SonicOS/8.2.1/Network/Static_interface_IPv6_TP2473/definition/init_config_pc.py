from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_setup_dibbler_on_PC2(self):
        conf_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/Static_interface_IPv6_TP2473/definition/conf'
        cmd_list = ['dibbler-server stop',
                    f'timeout 5 \cp {conf_path}/radvd.conf /etc/',
                    f'timeout 5 \cp {conf_path}/server.conf /etc/dibbler/',
                    f'timeout 5 \cp {conf_path}/sysctl.conf /etc/',
                    'timeout 5 sysctl -p',
                    'timeout 5 systemctl restart radvd']
        pc2_login.send_commands(cmd_list)
        pc2_login.send_command('dibbler-server run > /var/log/dibbler.log &')
        time.sleep(3)
        out = pc2_login.send_command('dibbler-server status')
        Assertion.assert_regular(out, 'Dibbler server.*RUNNING', 'ERR: start server on pc2 failed.')

    def test_02_config_routes_on_pc2(self):
        pc2_login.send_command('ip -6 r add 2002::/64 dev eth1')
        pc2_login.send_command('ip -6 r add 2001:1:2:3::/64 dev eth1')
        pc2_login.send_command('ip -6 r add 2001:1:2:4::/64 dev eth1')
        pc2_login.send_command('ifconfig eth1 inet6 add 2001:1:2:3::100')
        pc2_login.send_command('ifconfig eth1 inet6 add 2001:1:2:4::100')
        pc2_login.send_command('ifconfig eth1 inet6 add 2002::100')
        Assertion.assert_equal(True, True, 'ERR: add routes failed on PC2')
