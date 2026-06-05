from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_dns_server_setup(self):
        cmds = [
            f'\cp {CONF_PATH}/dnsserver/named.conf /etc/named.conf',
            f'\cp {CONF_PATH}/dnsserver/named.rfc1912.zones /etc/named.rfc1912.zones',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.zone /var/named/baidu.com.zone',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.local /var/named/baidu.com.local',
            'systemctl restart named',
            'systemctl status named',
        ]
        output = PC4_login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dns server in PC4 failed")

    def test_02_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC1_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.REMOTE_X0_NET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X3_IP}',
                f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.X3_IP}',
                'ip -4 r']
        output = PC3_login.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.REMOTE_X0_NET}/24 via {Parameter.X3_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC5 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}',
                f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}',
                f'route add -net {Parameter.X3_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}',
                'ip -4 r']
        output = PC5_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.REMOTE_X0_IP}' in output else False
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
