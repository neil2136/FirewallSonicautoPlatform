from definition.settings import *
from definition.utils import *


class TestInit_DNS_Server_and_Route(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = 'initialize 3 dns servers and PC1 route'

    def test_01_setup_dns_server_on_pc2(self):
        named_conf = '/etc/named.conf'
        confs_path = CONF_PATH + 'dnsserver_pc2/'
        cmds = ['service named stop',
                       f'rm -f {named_conf}.bak',
                       f'mv {named_conf} {named_conf}.bak',
                       f'\\cp -f {confs_path}named.conf /etc/',
                       f'\\cp -f {confs_path}baidu.com.zone /var/named/',
                       f'\\cp -f {confs_path}baidu.com.local /var/named/',
                       f'\\cp -f {confs_path}named.rfc1912.zones /var/named/',
                "systemctl restart named",
                "systemctl status named"]
        res = PC2_login.send_commands(cmds)
        Assertion.assert_regular(str(res), 'named.*running', "ERR: initial DNS in PC2 failed")

    def test_02_setup_dns_server_on_pc3(self):
        named_conf = '/etc/named.conf'
        confs_path = CONF_PATH + 'dnsserver_pc3/'
        cmds = ['service named stop',
                       f'rm -f {named_conf}.bak',
                       f'mv {named_conf} {named_conf}.bak',
                       f'\\cp -f {confs_path}named.conf /etc/',
                       f'\\cp -f {confs_path}baidu.com.zone /var/named/',
                       f'\\cp -f {confs_path}baidu.com.local /var/named/',
                       f'\\cp -f {confs_path}named.rfc1912.zones /var/named/',
                "systemctl restart named",
                "systemctl status named"]
        res = PC3_login.send_commands(cmds)
        Assertion.assert_regular(str(res), 'named.*running', "ERR: initial DNS in PC3 failed")

    def test_03_setup_dns_server_on_pc4(self):
        named_conf = '/etc/named.conf'
        confs_path = CONF_PATH + 'dnsserver_pc4/'
        cmds = ['service named stop',
                       f'rm -f {named_conf}.bak',
                       f'mv {named_conf} {named_conf}.bak',
                       f'\\cp -f {confs_path}named.conf /etc/',
                       f'\\cp -f {confs_path}baidu.com.zone /var/named/',
                       f'\\cp -f {confs_path}baidu.com.local /var/named/',
                       f'\\cp -f {confs_path}named.rfc1912.zones /var/named/',
                "systemctl restart named",
                "systemctl status named"]
        res = PC4_login.send_commands(cmds)
        Assertion.assert_regular(str(res), 'named.*running', "ERR: initial DNS in PC4 failed")

    def test_04_config_PC1_route(self):
        logger.info(f'Set route on PC1 via gw {Parameter.FIREWALL}')
        cmds = [
            f'route add -net {Parameter.X1_DNS1} netmask 255.255.255.255 gw {Parameter.FIREWALL}',
            'ip -4 r'
        ]
        output = PC1_login.send_commands(cmds)
        logger.info(output)
        Assertion.assert_regular(output, f'{Parameter.X1_DNS1} via 192.168.168.168 dev eth2', "ERR: Config PC1 route failed!!")