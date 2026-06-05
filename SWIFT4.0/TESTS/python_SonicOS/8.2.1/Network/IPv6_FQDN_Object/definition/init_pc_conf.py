from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_dns_server_setup_on_pc3(self):
        cmds = [
            f'\cp {CONF_PATH}/dnsserver/named.conf /etc/named.conf',
            f'\cp {CONF_PATH}/dnsserver/named.rfc1912.zones /etc/named.rfc1912.zones',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.zone /var/named/baidu.com.zone',
            f'\cp {CONF_PATH}/dnsserver/baidu.com.local /var/named/baidu.com.local',
            f'\cp {CONF_PATH}/dnsserver/jliantest.com.zone.wildcard /var/named/jliantest.com.zone.wildcard',
            # allow TCP DNS query and response
            'sudo iptables - A INPUT - p tcp - -dport 53 - j ACCEPT',
            'sudo iptables - A OUTPUT - p tcp - -sport 53 - j ACCEPT',
            'systemctl restart named',
            'systemctl status named',
        ]
        output = PC3_Login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dns server in PC3 failed")

    def test_02_add_ipv6_route_on_pc2(self):
        cmds = [f'ip -6 route add {Parameter.X1_IPv6_SUBNET}/64 via {Parameter.X2_IPv6}',
                'ip -6 r']
        output = PC2_Login.send_commands(cmds)
        res = True if f'{Parameter.X1_IPv6_SUBNET}/64 via {Parameter.X2_IPv6}' in output else False
        Assertion.assert_equal(res, True, "ERR: add ipv6 route on pc2 failed")

    def test_03_add_ipv6_address_for_eth1_on_pc3(self):
        cmds = [f'ip addr add {PC3_ETH1_IPv6}/64 dev eth1',
                'ifconfig eth1']
        output = PC3_Login.send_commands(cmds)
        flag = True if PC3_ETH1_IPv6 in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: add ipv6 address for eth1 on pc3 failed")

