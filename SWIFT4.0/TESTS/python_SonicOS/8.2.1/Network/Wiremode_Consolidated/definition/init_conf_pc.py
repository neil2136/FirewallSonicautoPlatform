from definition.settings import *

class TestSetup_PC(Test):
    uuid = 'NonTC'

    def test_01_setup_ftp_server_on_pc1(self):
        configfilecmds = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            'service vsftpd restart',
            'service vsftpd status',
        ]
        output = PC1_login.send_commands(configfilecmds)
        res = True if 'running' in output and 'failed|Not Found' not in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on pc1 failed")

    def test_02_setup_ftp_server_on_pc2(self):
        configfilecmds = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            'service vsftpd restart',
            'service vsftpd status',
        ]
        output = PC2_login.send_commands(configfilecmds)
        res = True if 'running' in output and 'failed|Not Found' not in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on pc2 failed")

    def test_03_setup_http_server_on_pc2(self):
        res =False
        # get virus file in public server to PC2
        getfilecmds = ['mkdir /var/www/html/virus',
                'cp -f /etc/httpd/conf/httpd.conf /var/www/html/virus/test.txt',
                'wget http://10.6.0.69/virus/password-protected-test.zip -O /var/www/html/virus/password-protected-test.zip',
                'wget http://10.6.0.69/virus/Exploit.VBS.Agent.q.gz -O /var/www/html/virus/Exploit.VBS.Agent.q.gz',
                'wget http://10.6.0.69/virus/upx.exe -O /var/www/html/virus/upx.exe'
                ]
        output1 = PC2_login.send_commands(getfilecmds)
        if output1.count('100%') == 3 and 'failed|Not Found' not in output1:
            logger.info("Copy virus and anti-spyware file pass")
            # change http config file in PC2
            configfilecmds = [
                f'cp -f {CONF_PATH} /etc/httpd/conf/',
                'service httpd restart',
                'service httpd status',
            ]
            output2 = PC2_login.send_commands(configfilecmds)
            res = True if 'running' in output2 and 'failed|Not Found' not in output2 else False
        else:
            logger.info("Copy virus and anti-spyware file fail")
        Assertion.assert_equal(res, True, "ERR: setup http server on pc2 failed")


    def test_04_change_eth0_to_PC2(self):
        cmds = [
            f'ifconfig eth0 {Parameter.PC2_ETH0_NewIP}',
            f'route add -host {Parameter.PUBLIC_SERVER} gw {Parameter.X2_IP}',
        ]
        output = PC2_login.send_commands(cmds)
        logger.info(output)
        output2 = PC2_login.send_command('ip -4 r')
        res = True if f'{Parameter.PUBLIC_SERVER} via {Parameter.X2_IP} dev eth0' in output2 else False
        Assertion.assert_equal(res, True, "ERR: changed PC2 eth0 ip failed")
