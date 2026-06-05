from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    # def test_01_setup_dhcpv6_server_on_PC3(self):
    #     conf_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/IP_Helper_DHCPv6_Relay_part1/definition/file'
    #     cmd_list = ['dibbler-server stop',
    #                 f'timeout 5 \cp {conf_path}/radvd.conf /etc/',
    #                 f'timeout 5 \cp {conf_path}/server.conf /etc/dibbler/',
    #                 f'timeout 5 \cp {conf_path}/sysctl.conf /etc/',
    #                 'timeout 5 sysctl -p',
    #                 'timeout 5 systemctl restart radvd']
    #     pc3_login.send_commands(cmd_list)
    #     pc3_login.send_command('dibbler-server start')
    #     time.sleep(3)
    #     out = pc3_login.send_command('dibbler-server status')
    #     rc = 'Dibbler server: RUNNING' in out
    #     Assertion.assert_equal(rc, True, 'ERR: start server on pc3 failed.')

    # def test_01_add_v6_addr_for
