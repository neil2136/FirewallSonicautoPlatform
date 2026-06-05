from definition.settings import *


class TestInitPCConfig(Test):
    uuid = 'NonTC'

    def test_01_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X2_IP}',
                f'route add -host 10.103.202.200 gw {Parameter.X2_IP}',
                f'route add -host 172.17.1.10 gw {Parameter.X2_IP}',
                f'route add -host 192.168.4.30 gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_host.send_commands(cmds)
        res['pc2'] = True if (f'{Parameter.https_server_ip} via {Parameter.X2_IP}' in output
                              and f'10.103.202.200 via {Parameter.X2_IP}' in output
                              and f'172.17.1.10 via {Parameter.X2_IP}' in output
                              and f'192.168.4.30 via {Parameter.X2_IP}' in output) else False
        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X3_IP}',
                f'route add -host 10.103.202.200 gw {Parameter.X3_IP}',
                f'route add -host 172.17.1.10 gw {Parameter.X3_IP}',
                'ip -4 r']
        output = PC3_host.send_commands(cmds)
        res['pc3'] = True if (f'{Parameter.https_server_ip} via {Parameter.X3_IP}' in output
                              and f'10.103.202.200 via {Parameter.X3_IP}' in output
                              and f'172.17.1.10 via {Parameter.X3_IP}' in output) else False
        logger.info(" {} ".center(50, '-').format('PC4 Route Configure'))
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X4_IP}',
                f'route add -host 10.103.202.200 gw {Parameter.X4_IP}',
                f'route add -host 172.17.1.10 gw {Parameter.X4_IP}',
                f'route add -host 192.168.2.20 gw {Parameter.X4_IP}',
                'ip -4 r']
        output = PC4_host.send_commands(cmds)
        res['pc4'] = True if (f'{Parameter.https_server_ip} via {Parameter.X4_IP}' in output
                              and f'10.103.202.200 via {Parameter.X4_IP}' in output
                              and f'172.17.1.10 via {Parameter.X4_IP}' in output
                              and f'192.168.2.20 via {Parameter.X4_IP}' in output) else False
        logger.info(" {} ".center(50, '-').format('PC5 Route Configure'))
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X4_IP}',
                f'route add -host 10.103.202.200 gw {Parameter.X4_IP}',
                f'route add -host 172.17.1.10 gw {Parameter.X4_IP}',
                f'route add -host 192.168.4.30 gw {Parameter.X4_IP}',
                'ip -4 r']
        output = PC5_host.send_commands(cmds)
        res['pc5'] = True if (f'{Parameter.https_server_ip} via {Parameter.X4_IP}' in output
                              and f'10.103.202.200 via {Parameter.X4_IP}' in output
                              and f'172.17.1.10 via {Parameter.X4_IP}' in output
                              and f'192.168.4.30 via {Parameter.X4_IP}' in output) else False
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs Route Failed")

    def test_02_get_mac_address_eth1(self):
        res = {}
        rc1 = PC2_host.send_command(f"ifconfig eth1")
        iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc1).group(0)
        Parameter.PC2_ETH1_MAC = iface_mac.lower()
        res['pc2'] = True if Parameter.PC2_ETH1_MAC else False
        rc2 = PC3_host.send_command(f"ifconfig eth1")
        iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc2).group(0)
        Parameter.PC3_ETH1_MAC = iface_mac.lower()
        res['pc3'] = True if Parameter.PC3_ETH1_MAC else False
        rc3 = PC4_host.send_command(f"ifconfig eth1")
        iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc3).group(0)
        Parameter.PC4_ETH1_MAC = iface_mac.lower()
        res['pc4'] = True if Parameter.PC4_ETH1_MAC else False
        rc4 = PC5_host.send_command(f"ifconfig eth1")
        iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc4).group(0)
        Parameter.PC5_ETH1_MAC = iface_mac.lower()
        res['pc5'] = True if Parameter.PC5_ETH1_MAC else False
        logger.info(f'PC2_ETH1_MAC is {Parameter.PC2_ETH1_MAC}')
        logger.info(f'PC3_ETH1_MAC is {Parameter.PC3_ETH1_MAC}')
        logger.info(f'PC4_ETH1_MAC is {Parameter.PC4_ETH1_MAC}')
        logger.info(f'PC5_ETH1_MAC is {Parameter.PC5_ETH1_MAC}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Get PCs mac Failed")


class Test_SetupMail_Server(Test):
    uuid = "NonTC"
    description = "setup mail server on PC1"
    goto_teardown = True

    def test_00_07_config_mail_server(self):
        rc = start_mail_server.start_mail_server(mail_server_host=mail_server_ip)
        Assertion.assert_not_equal(rc, False, "ERR: start email server failed")
