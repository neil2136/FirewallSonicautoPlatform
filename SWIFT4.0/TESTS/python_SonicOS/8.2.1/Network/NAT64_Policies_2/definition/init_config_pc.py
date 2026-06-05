from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_route_on_PC(self):
        pc1_login.send_command(f'ip -6 r add {Parameter.Well_Know_Pref64_NET} via {Parameter.X0_V6_IP}')
        pc1_login.send_command(f'ip -6 r add 3000::/32 via {Parameter.X0_V6_IP}')
        pc2_login.send_command('ip -6 route del default; timeout 20 ip -6 route del default')
        pc2_login.send_command('ip -6 route add default via 2001::168')
        pc3_login.send_command('ip -6 route del default; timeout 20 ip -6 route del default')
        pc3_login.send_command('ip -6 route add default via 2002::168')
        out1 = pc1_login.send_command('ip -6 r')
        res1 = f'{Parameter.Well_Know_Pref64_NET} via {Parameter.X0_V6_IP}' in out1 and f'3000::/32 via {Parameter.X0_V6_IP}' in out1
        logger.info(f'config route on PC1 result: {res1}')
        out2 = pc2_login.send_command('ip -6 r')
        res2 = f'default via {Parameter.X1_V6_IP}' in out2
        logger.info(f'config route on PC2 result: {res2}')
        out3 = pc3_login.send_command('ip -6 r')
        res3 = f'default via {Parameter.X2_V6_IP}' in out3
        logger.info(f'config route on PC3 result: {res3}')
        Assertion.assert_equal(res1 & res2 & res3, True, '\033[1;31mERR: add routes on PC failed!\033[0m')

    def test_02_start_httpd_on_pc2(self):
        res = False
        for i in range(3):
            pc2_login.send_command('systemctl restart httpd')
            out = pc2_login.send_command('systemctl status httpd')
            if 'running' in out:
                pc2_login.send_command('echo test for nat64 > /root/index.html')
                out = pc2_login.send_command('curl http://127.0.0.1')
                res = 'test for nat64' in out
                break
        Assertion.assert_equal(res, True, '\033[1;31mERR: start httpd service on pc2 failed!\033[0m')

    def test_03_start_ftp_on_pc2(self):
        logger.info('1, configure vsftpd.conf')
        cmd_list = [f'\cp {ftp_conf_file} /etc/vsftpd/',
                    f'\cp {ftp_user_file} /etc/vsftpd/',
                    'timeout 20 systemctl restart vsftpd',
                    'timeout 20 systemctl status vsftpd -l'
                    ]
        out = pc2_login.send_commands(cmd_list)
        res = 'running' in out
        logger.info('2, mk test file')
        pc2_login.send_command('echo test for nat64 ftp > /var/ftp/test.txt')
        Assertion.assert_equal(res, True, '\033[1;31mERR: start ftp service on pc2 failed!\033[0m')
