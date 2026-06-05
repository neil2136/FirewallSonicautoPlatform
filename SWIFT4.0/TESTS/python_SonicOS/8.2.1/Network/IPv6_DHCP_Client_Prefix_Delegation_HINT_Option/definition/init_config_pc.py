from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_setup_dhcpv6_server_on_pc2(self):
        conf_path = os.environ[
                        'PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_Prefix_Delegation_HINT_Option/definition/config_file'
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
