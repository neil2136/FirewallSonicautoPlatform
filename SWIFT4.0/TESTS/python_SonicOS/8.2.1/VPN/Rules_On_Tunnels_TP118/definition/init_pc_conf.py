from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_start_http_server_on_pc2(self):
        cmds = [
            'cat /dev/null >/usr/share/httpd/noindex/index.html',
            "echo 'auto_vpn_access_test_tag' > /usr/share/httpd/noindex/index.html",
            'systemctl start httpd.service',
            'systemctl status httpd.service'
        ]
        res1 = PC2_Login.send_commands(cmds)
        res2 = PC2_Login.send_command('cat /usr/share/httpd/noindex/index.html')
        flag = True if ('Started The Apache HTTP Server' in res1) and ('auto_vpn_access_test_tag' in res2) else False
        Assertion.assert_equal(flag, True, "ERR: start http server on PC2 failed")

    def test_02_setup_ftp_server_to_pc2(self):
        configfilecmds = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            'service vsftpd restart',
            'service vsftpd status',
        ]
        output = PC2_Login.send_commands(configfilecmds)
        res = True if 'running' in output and 'failed|Not Found' not in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on pc failed")

    def test_03_add_route_to_local_x0_subnet_on_pc3_eth1(self):
        cmds = [f'route add -net {Parameter.X2_NET} netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                'ip -4 r']
        output = PC3_Login.send_commands(cmds)
        flag = True if f'{Parameter.X2_NET}/24 via {Parameter.X3_REMOTE_IP} dev eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: add route to local x2 subnet on PC3 failed")

    def test_04_add_route_to_remote_x3_subnet_on_pc2_eth1(self):
        cmds = [f'route add -net {Parameter.X3_REMOTE_NET} netmask {Parameter.MASK} gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_Login.send_commands(cmds)
        flag = True if f'{Parameter.X3_REMOTE_NET}/24 via {Parameter.X2_IP} dev eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: add route to remote x3 subnet on PC2 failed")
