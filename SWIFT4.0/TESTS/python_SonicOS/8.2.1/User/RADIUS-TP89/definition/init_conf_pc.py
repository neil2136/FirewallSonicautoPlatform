from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_httpd_server_setup(self):
        virus_server = '10.6.0.69'
        cmd_list = [
            'mkdir /var/www/https/',
            'chmod 777 /var/www/https/',
            '\cp -rf {}/* /var/www/https/'.format(HTTPS_SERVER_PATH),
            f'wget http://{virus_server}/virus/password-protected-test.zip -O /var/www/https/password-protected-test.zip',
            f'wget http://{virus_server}/virus/Exploit.VBS.Agent.q.gz -O /var/www/https/Exploit.VBS.Agent.q.gz',
            f'wget http://{virus_server}/virus/upx.exe -O /var/www/https/upx.exe',
            f'wget http://{virus_server}/spyware/testsp/spy_3_449.bin -O /var/www/https/spy_3_449.bin',
            f'wget http://{virus_server}/ips/high_priority/IPS_5342_high_poc.xls -O /var/www/https/IPS_5342_high_poc.xls',
            'rm -f /etc/httpd/conf.d/ssl.conf',
            '\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(configPath + "conf.d"),
            '\cp -fr {}/httpd.conf /etc/httpd/conf/'.format(configPath + "conf"),
            'grep /www/https /etc/httpd/conf.d/ssl.conf',
            'install {}/* /etc/pki/tls/certs/'.format(certPath),
            'install {}/* /etc/pki/tls/private/'.format(certPath),
            'systemctl start httpd',
            'systemctl status httpd'
        ]
        res = PC4_login.send_commands(cmd_list)
        flag = True if re.search(r'active \(running\)', res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")

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

  
    def test_04_syslog_server_setup(self):
        cmds = [
            f"\\cp -f {CONF_PATH}/syslog_server/rsyslog.conf /etc/rsyslog.conf",
            f"\\cp -f {CONF_PATH}/syslog_server/rsyslog /etc/sysconfig/rsyslog",
            "systemctl status rsyslog",
        ]
        output = PC4_login.send_commands(cmds)
        Assertion.assert_regular(output, 'active', "syslog server setup failed")

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
                f'route add -net {Parameter.R_X0_NET}/24 gw {Parameter.FIREWALL}',
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
