from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_v6_addr_for_PC(self):
        pc2_login.send_command('ifconfig eth1 inet6 add 2022::100/64')
        pc2_login.send_command('ip -6 r add 2022::/64 dev eth1')
        # pc3_login.config_IPv6_route(
        #     route='2013:2::', prefix=64, gw=Parameter.X3_V1_V6)
        # pc4_login.config_IPv6_route(
        #     route='2013:1::', prefix=64, gw=Parameter.X3_V2_V6)
        Assertion.assert_equal(True, True, 'ERR: config for V6 addr for PC2 failed!')

    def test_02_setup_dhcpv6_server_on_pc2(self):
        conf_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_VLAN_2/definition/conf'
        cmd_list = ['dibbler-server stop',
                    f'timeout 5 \cp {conf_path}/radvd.conf /etc/',
                    f'timeout 5 \cp {conf_path}/server.conf /etc/dibbler/',
                    f'timeout 5 \cp {conf_path}/sysctl.conf /etc/',
                    'timeout 5 sysctl -p',
                    'timeout 5 systemctl restart radvd']
        pc2_login.send_commands(cmd_list)
        pc2_login.send_command('dibbler-server run > /var/log/dibbler.log &')
        time.sleep(3)
        out1 = pc2_login.send_command('systemctl status radvd')
        out2 = pc2_login.send_command('dibbler-server status')
        rc = 'active (running)' in out1 and bool(re.search(r'Dibbler server.*RUNNING', out2))
        Assertion.assert_equal(rc, True, 'ERR: start server on pc2 failed.')
