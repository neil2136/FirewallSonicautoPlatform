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
        res = PC3_login.send_commands(cmd_list)
        flag = True if re.search('running', res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup server failed")

    def test_02_dhcp_server_setup(self):
        cmds = [
            f"\cp -rf {CONF_PATH}/dhcpserver/dhcpd.conf  /etc/dhcp",
            "systemctl restart dhcpd",
            "systemctl status dhcpd",
        ]
        output = PC2_login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dhcp server in PC2 failed")

    def test_0_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {PC3_ETH1_NET}/24 gw {PC2_ETH1_IP}',
                'ip -4 r']
        output = PC1_login.send_commands(cmds)
        res['pc1'] = True if f'{PC3_ETH1_NET}/24 via {PC2_ETH1_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = ['echo "1" > /proc/sys/net/ipv4/ip_forward',
                'echo "200 my" >> /etc/iproute2/rt_tables',
                'ip rule add iif eth1 pri 10000 table my',
                'ip rule add iif eth3 pri 10001 table my',
                f'ip route add default via {Parameter.X2_IP} table my',
                f'route add -net {PC1_ETH2_NET}/24 gw {PC2_ETH1_IP}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'{PC1_ETH2_NET}/24 via {PC2_ETH1_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {PC1_ETH2_NET}/24 gw {PC2_ETH3_IP}',
                'ip -4 r']
        output = PC3_login.send_commands(cmds)
        res['pc3'] = True if f'{PC1_ETH2_NET}/24 via {PC2_ETH3_IP}' in output else False

        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")



