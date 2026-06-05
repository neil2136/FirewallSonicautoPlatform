from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_routes_on_pc(self):
        PC1.send_command(f'route add -net 12.12.1.0/24 gateway {Parameter.FIREWALL}')
        PC3.send_command(f'route add -net 12.12.1.0/24 gateway {Parameter.X2_IP}')
        PC2.send_command(f'route add -net 192.168.168.0/24 gateway {Parameter.X1_IP}')
        PC2.send_command(f'route add -net 13.13.1.0/24 gateway {Parameter.X1_IP}')
        out1 = PC1.send_command('ip -4 r')
        out2 = PC3.send_command('ip -4 r')
        rc = f'12.12.1.0/24 via {Parameter.FIREWALL} dev eth1' in out1 and f'12.12.1.0/24 via {Parameter.X2_IP} dev eth1' in out2
        Assertion.assert_equal(rc, True, 'ERR: config routes for PC failed!!')

    def test_02_setup_https_server_on_pc(self):
        cmd_list = ['echo "test for nat mapping" > /root/index.html', 'systemctl restart httpd',
                    'systemctl status httpd']
        out1 = PC1.send_commands(cmd_list)
        out2 = PC2.send_commands(cmd_list)
        out3 = PC3.send_commands(cmd_list)
        rc = 'active (running)' in out1 and 'active (running)' in out2 and 'active (running)' in out3
        Assertion.assert_equal(rc, True, 'ERR: start https server on pc failed!!')

    def test_03_setup_syslog_server_on_pc1(self):
        cmd_list = ["sed -i 's/#$ModLoad imudp/$ModLoad imudp/g' /etc/rsyslog.conf",
                    "sed -i 's/#$UDPServerRun 514/$UDPServerRun 514/g' /etc/rsyslog.conf",
                    "systemctl restart rsyslog",
                    "systemctl status rsyslog"]
        out = PC1.send_commands(cmd_list)
        Assertion.assert_regular(out, 'active \(running\)', "ERR: setup syslog server on PC1 failed!!")

    def test_04_add_v6_addr_for_PC(self):
        cmd_list1 = ['ifconfig eth1 inet6 add 1011::169/64', 'ip -6 r add 1011::/64 dev eth1',
                     'route -A inet6 add 1012::/64 gw 1011::168', 'ping6 -c 5 1011::168']
        cmd_list2 = ['ifconfig eth1 inet6 add 1012::169/64', 'route -A inet6 add 1012::/64 gw 1011::168', 'ping6 -c 5 1012::168']
        # PC1.send_commands(cmd)
        # PC1.send_command('ip -6 r add 1011::/64 dev eth1')
        # PC1.send_command('route -A inet6 add 1012::/64 gw 1011::168')
        # PC2.send_command('ifconfig eth1 inet6 add 1012::169/64')
        # PC2.send_command('ip -6 r add 1012::/64 dev eth1')
        out1 = PC1.send_commands(cmd_list1)
        out2 = PC2.send_commands(cmd_list2)
        rc = '100% packet loss' not in out1 and '100% packet loss' not in out2
        Assertion.assert_equal(rc, True, 'ERR: config v6 addr for PC failed!!')
