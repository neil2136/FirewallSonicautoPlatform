from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_dns_server_setup_on_pc4(self):
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
        output = PC4_Login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dns server in PC4 failed")

    def test_02_start_http_server_on_pc4(self):
        cmds = [
            'cat /dev/null >/usr/share/httpd/noindex/index.html',
            "echo 'auto_cfs_test_tag' > /usr/share/httpd/noindex/index.html",
            'systemctl start httpd.service',
            'systemctl status httpd.service'
        ]
        res1 = PC4_Login.send_commands(cmds)
        res2 = PC4_Login.send_command('cat /usr/share/httpd/noindex/index.html')
        flag = True if ('Started The Apache HTTP Server' in res1) and ('auto_cfs_test_tag' in res2) else False
        Assertion.assert_equal(flag, True, "ERR: start http server on PC4 failed")

    def test_03_add_ip_route_on_pc2(self):
        cmds = [f'ip route add {Parameter.X1_NET}/24 via {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_Login.send_commands(cmds)
        res = True if f'{Parameter.X1_NET}/24 via {Parameter.X2_IP}' in output else False
        Assertion.assert_equal(res, True, "ERR: add ip route on pc2 failed")

    def test_04_add_ip_route_on_pc3(self):
        cmds = [f'ip route add {Parameter.X1_NET}/24 via {Parameter.X2_IP}',
                'ip -4 r']
        output = PC3_Login.send_commands(cmds)
        res = True if f'{Parameter.X1_NET}/24 via {Parameter.X2_IP}' in output else False
        Assertion.assert_equal(res, True, "ERR: add ip route on pc3 failed")



