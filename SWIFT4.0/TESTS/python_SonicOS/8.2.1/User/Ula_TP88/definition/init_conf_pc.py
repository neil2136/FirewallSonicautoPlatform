from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

   
    def test_02_dns_server_setup(self):
        cmds = [
            f'\cp {CONF_PATH}/dnsserver/named.conf /etc/named.conf',
            f'\cp {CONF_PATH}/dnsserver/named.rfc1912.zones /etc/named.rfc1912.zones',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.zone /var/named/baidu.com.zone',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.local /var/named/baidu.com.local',
            'systemctl restart named',
            'systemctl status named',
        ]
        output = PC4_login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dns server in PC3 failed")

   
    
    def test_06_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.R_X0_NET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC1_login.send_commands(cmds)
        res['pc1'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.R_X0_NET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X3_IP}',
                f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.X3_IP}',
                'ip -4 r']
        output = PC3_login.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.X3_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC5 Route Configure'))
        cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.R_X0_IP}',
                'ip -4 r']
        output = PC5_login.send_commands(cmds)
        res['pc5'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.R_X0_IP}' in output else False

        logger.info(f'config pcs result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
