from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(5)
    def test_01_setup_dhcpv6_server_on_pc2(self):
        conf_path = os.environ[
                        'PYTHON_SONICOS_HOME'] + '/Network/IPv6_DNS_Client_Full/definition/config_file'
        cmd_list = ['dibbler-server stop',
                    f'timeout 5 \cp {conf_path}/radvd.conf /etc/',
                    f'timeout 5 \cp {conf_path}/server.conf /etc/dibbler/',
                    f'timeout 5 \cp {conf_path}/sysctl.conf /etc/',
                    'timeout 5 sysctl -p',
                    'timeout 5 systemctl restart radvd']
        PC2_login.send_commands(cmd_list)
        PC2_login.send_command('dibbler-server run > /var/log/dibbler.log &')
        time.sleep(3)
        dibbler_log = PC2_login.send_command('cat /var/log/dibbler.log')
        logger.info(dibbler_log)
        out = PC2_login.send_command('dibbler-server status')
        Assertion.assert_regular(out, 'Dibbler server.*RUNNING.*pid', 'ERR: start server on pc2 failed.')
