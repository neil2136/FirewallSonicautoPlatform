from definition.settings import *

class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_setup_http_server_on_LAN_PC(self):
        cmd_list = [
            'mkdir /var/www/https/',
            'chmod 777 /var/www/https/',
            '\cp -rf {}/* /var/www/https/'.format(Parameter.HTTP_CONFS_PATH),
            'rm -f /etc/httpd/conf.d/ssl.conf',
            '\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(Parameter.configPath + "conf.d"),
            '\cp -fr {}/httpd.conf /etc/httpd/conf/'.format(Parameter.configPath + "conf"),
            'grep /www/https /etc/httpd/conf.d/ssl.conf',
            'install {}/* /etc/pki/tls/certs/'.format(Parameter.certPath),
            'install {}/* /etc/pki/tls/private/'.format(Parameter.certPath),
            'systemctl start httpd',
            'systemctl status httpd'
        ]
        res = pc2.send_commands(cmd_list)
        flag = True if re.search(r'active \(running\)', res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")
    
    def test_02_setup_http_server_on_VPN_PC(self):
        cmd_list = [
            'mkdir /var/www/https/',
            'chmod 777 /var/www/https/',
            '\cp -rf {}/* /var/www/https/'.format(Parameter.HTTP_CONFS_PATH),
            'rm -f /etc/httpd/conf.d/ssl.conf',
            '\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(Parameter.configPath + "conf.d"),
            '\cp -fr {}/httpd.conf /etc/httpd/conf/'.format(Parameter.configPath + "conf"),
            'grep /www/https /etc/httpd/conf.d/ssl.conf',
            'install {}/* /etc/pki/tls/certs/'.format(Parameter.certPath),
            'install {}/* /etc/pki/tls/private/'.format(Parameter.certPath),
            'systemctl start httpd',
            'systemctl status httpd'
        ]
        res = pc4.send_commands(cmd_list)
        flag = True if re.search(r'active \(running\)', res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")

    def test_03_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.R_X0_SUBNET}/24 gw {Parameter.X1_IP}',
                'ip -4 r']
        output = pc1.send_commands(cmds)
        res['pc1'] = True if f'{Parameter.R_X0_SUBNET}/24 via {Parameter.X1_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.R_X0_SUBNET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = pc2.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.R_X0_SUBNET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {Parameter.R_X0_SUBNET}/24 gw {Parameter.X2_IP}',
                'ip -4 r']
        output = pc3.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.R_X0_SUBNET}/24 via {Parameter.X2_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC4 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.R_X0_IP}',
                f'route add -net {Parameter.R_X0_SUBNET}/24 gw {Parameter.R_X0_IP}',
                f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.R_X0_IP}',
                f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.R_X0_IP}',
                'ip -4 r']
        output = pc4.send_commands(cmds)
        res['pc4'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.R_X0_IP}' in output else False
        res['pc4'] &= True if f'{Parameter.R_X0_SUBNET}/24 via {Parameter.R_X0_IP}' in output else False
        res['pc4'] &= True if f'{Parameter.X0_SUBNET}/24 via {Parameter.R_X0_IP}' in output else False
        res['pc4'] &= True if f'{Parameter.X2_SUBNET}/24 via {Parameter.R_X0_IP}' in output else False

        logger.info(f'config pcs result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")