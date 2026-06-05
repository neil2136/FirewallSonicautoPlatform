from definition.settings import *


class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_add_route_on_pc1(self):
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X0_IP}',
                f'route add -net {Parameter.R_X0_NET}/24 gw {Parameter.X0_IP}',
                f'route add -net {Parameter.R_X2_NET}/24 gw {Parameter.X0_IP}',
                'ip -4 r',
                ]
        res = LAN_HOST.send_commands(cmds)
        routelist = [f'{Parameter.X1_SUBNET}/24 via {Parameter.X0_IP} dev eth1',
                     f'{Parameter.R_X0_NET}/24 via {Parameter.X0_IP} dev eth1',
                     f'{Parameter.R_X2_NET}/24 via {Parameter.X0_IP} dev eth1']
        flag = True if all(i in res for i in routelist) else False
        Assertion.assert_equal(flag, True, "ERR: Add route to remote dut failed")

    def test_02_restore_eth_on_pc2(self):
        cmds = [f'ifconfig eth1 0.0.0.0',
                f'ifconfig eth1 down',
                f'ifconfig eth1 up',
                f'ifconfig eth2 0.0.0.0',
                f'ifconfig eth2 down',
                f'ifconfig eth2 up',
                ]
        res = RMT_HOST.send_commands(cmds)
        logger.info(res)

        cmds1 = [f'ifconfig eth1',
                 f'ifconfig eth2']
        res1 = RMT_HOST.send_commands(cmds1)
        flag = True if 'inet addr' not in res1 else False
        Assertion.assert_equal(flag, True, "ERR: restore eth on PC2 failed")

    def test_03_setup_dhcp_server_on_pc1(self):
        conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/DHCP_Relay_TP28/definition/files/dhcpd.conf'
        cmds = [f'cp -f {conf_file} /etc/dhcp/dhcpd.conf',
                'service dhcpd restart',
                ]
        res = LAN_HOST.send_commands(cmds)
        logger.info(res)
        res1 = LAN_HOST.send_command('service dhcpd status')
        flag = True if 'is running' in res1 else False
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC2 failed")
