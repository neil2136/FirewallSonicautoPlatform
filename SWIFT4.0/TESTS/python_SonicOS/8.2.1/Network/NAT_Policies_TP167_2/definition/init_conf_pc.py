from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'

    def test_01_setup_https_server(self):
        cmd_list = (
            'echo "test for nat policy" > /root/index.html', 'systemctl restart httpd', 'systemctl status httpd')
        out = pc1_login.send_commands(cmd_list)
        Assertion.assert_regular(out, 'active \(running\)', 'ERR: setup lan server failed')

    def test_02_config_route_on_pc(self):
        pc1_login.send_command(f'route add -net 12.12.1.0/24 gw {Parameter.FIREWALL}')
        pc1_login.send_command(f'route add -net 13.13.1.0/24 gw {Parameter.FIREWALL}')
        pc2_login.send_command(f'route add -net 12.12.1.0/24 gw {Parameter.X1_IP}')
        pc3_login.send_command(f'route add -net 12.12.1.0/24 gw {Parameter.X2_IP}')
        pc3_login.send_command(f'route add -net 192.168.168.0/24 gw {Parameter.X2_IP}')
        out1 = pc1_login.send_command('ip -4 r')
        out2 = pc2_login.send_command('ip -4 r')
        out3 = pc3_login.send_command('ip -4 r')
        rc = '12.12.1.0/24 via 192.168.168.168' in out1 and '13.13.1.0/24 via 192.168.168.168' in out1
        rc &= '12.12.1.0/24 via 12.12.1.168' in out2
        rc &= '12.12.1.0/24 via 13.13.1.168' in out3 and '192.168.168.0/24 via 13.13.1.168' in out3
        Assertion.assert_equal(rc, True, 'ERR: config routers for PC failed')

    def test_03_check_traffic_pcs(self):
        logger.info('=======>traffic from LAN to DMZ')
        out1 = pc1_login.send_command('ping -c 5 13.13.1.169')
        logger.info('=======>traffic from DMZ to WAN')
        out2 = pc3_login.send_command('ping -c 5 12.12.1.169')
        rc = '100% packet loss' not in out1 and '100% packet loss' not in out2
        Assertion.assert_equal(rc, True, 'ERR: check traffic from LAN to DMZ failed!!')
