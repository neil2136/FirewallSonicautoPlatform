from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_routes_on_pc(self):
        cmd_list1 = [f'route add -net {PC4_ETH1_NW}/24 gw {Parameter.FIREWALL}',
                     f'route add -net {PC2_ETH1_NW}/24 gw {Parameter.FIREWALL}',
                     f'route add -net {PC3_ETH1_NW}/24 gw {Parameter.FIREWALL}',
                     f'route add -net {PC1_ETH3_NW}/24 gw {Parameter.X3_IP}'
                     ]
        cmd_list2 = [f'route add -net {PC1_ETH1_NW}/24 gw {Parameter.X1_IP}',
                     f'route add -net {PC3_ETH1_NW}/24 gw {Parameter.X1_IP}',
                     f'route add -net {PC4_ETH1_NW}/24 gw {Parameter.X1_IP}',
                     f'route add -net {PC2_ETH1_NW}/24 gw {Parameter.X1_IP}'
                     ]
        cmd_list3 = [f'route add -net {PC2_ETH1_NW}/24 gw {Parameter.X4_IP}',
                     f'route add -net {PC1_ETH3_NW}/24 gw {Parameter.X4_IP}',
                     f'route add -net {PC1_ETH1_NW}/24 gw {Parameter.X4_IP}'
                     ]
        cmd_list4 = [f'route add -net {PC2_ETH1_NW}/24 gw {Parameter.X5_IP}',
                     f'route add -net {PC1_ETH3_NW}/24 gw {Parameter.X5_IP}',
                     f'route add -net {PC1_ETH1_NW}/24 gw {Parameter.X5_IP}'
                     ]
        localhost.send_commands(cmd_list1)
        pc2_login.send_commands(cmd_list2)
        pc3_login.send_commands(cmd_list3)
        pc4_login.send_commands(cmd_list4)
        logger.info('=> check add routes result')
        output1 = localhost.send_command('ip -4 r')
        output2 = pc2_login.send_command('ip -4 r')
        output3 = pc3_login.send_command('ip -4 r')
        output4 = pc4_login.send_command('ip -4 r')
        check_list1 = [f'{PC4_ETH1_NW}/24 via {Parameter.FIREWALL}',
                       f'{PC2_ETH1_NW}/24 via {Parameter.FIREWALL}',
                       f'{PC3_ETH1_NW}/24 via {Parameter.FIREWALL}'
                       ]
        check_list2 = [f'{PC1_ETH1_NW}/24 via {Parameter.X1_IP}',
                       f'{PC3_ETH1_NW}/24 via {Parameter.X1_IP}',
                       f'{PC4_ETH1_NW}/24 via {Parameter.X1_IP}',
                       f'{PC2_ETH1_NW}/24 via {Parameter.X1_IP}'
                       ]
        check_list3 = [f'{PC2_ETH1_NW}/24 via {Parameter.X4_IP}',
                       f'{PC1_ETH3_NW}/24 via {Parameter.X4_IP}',
                       f'{PC1_ETH1_NW}/24 via {Parameter.X4_IP}'
                       ]
        check_list4 = [f'{PC2_ETH1_NW}/24 via {Parameter.X5_IP}',
                       f'{PC1_ETH3_NW}/24 via {Parameter.X5_IP}',
                       f'{PC1_ETH1_NW}/24 via {Parameter.X5_IP}'
                       ]
        res = 0 if all(item in output1 for item in check_list1) else 1
        res += 0 if (all(item in output2 for item in check_list2)) else 1
        res += 0 if (all(item in output3 for item in check_list3)) else 1
        res += 0 if (all(item in output4 for item in check_list4)) else 1
        Assertion.assert_equal(
            res, 0, "ERR: config routes on PC failed")

    def test_02_setup_pptp_server_on_pc2(self):
        res = False
        cmd_list1 = [
            'mv /etc/pptpd.conf /etc/pptpd.conf.bak',
            'mv /etc/ppp/options.pptpd /etc/ppp/options.pptpd.bak',
            'mv /etc/ppp/chap-secrets /etc/ppp/chap-secrets.bak'
            'mv /etc/ppp/pap-secrets /etc/ppp/pap-secrets.bak'
        ]
        pc2_login.send_commands(cmd_list1)
        cmd_list2 = [
            f'cp -rf {PPTP_CONFIG_PATH}pptpd.conf /etc/',
            f'cp -rf {PPTP_CONFIG_PATH}options.pptpd /etc/ppp/',
            f'cp -rf {PPTP_CONFIG_PATH}pap-secrets /etc/ppp/',
            f'cp -rf {PPTP_CONFIG_PATH}chap-secrets /etc/ppp/'
        ]
        pc2_login.send_commands(cmd_list2)
        for i in range(5):
            pc2_login.send_command('service pptpd restart-kill')
            pc2_login.send_command('service pptpd start')
            status = pc2_login.send_command('service pptpd status')
            if 'is running' in status:
                res = True
                break
        Assertion.assert_equal(
            res, True, "ERR: Start pptp server on PC2 failed")

    def test_03_setup_https_server_on_pc3(self):
        res = pc3_login.start_HTTPS_server(HTTPS_CONF_PATH)
        Assertion.assert_equal(
            res, True, 'ERR: setup https server on PC3 failed.')
