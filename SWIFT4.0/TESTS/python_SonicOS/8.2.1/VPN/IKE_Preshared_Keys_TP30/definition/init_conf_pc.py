from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_setup_ftp_server_on_pc4(self):
        configfilecmds = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            'systemctl restart vsftpd',
            'systemctl status vsftpd',
        ]
        output = PC4_login.send_commands(configfilecmds)
        res = True if 'running' in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on pc1 failed")

    def test_02_setup_http_server_on_pc4(self):
        server_path = '10.6.0.69/virus'
        res = False
        # get virus file in public server to PC4
        getfilecmds = ['mkdir /var/www/html/virus',
                       'cp -f /etc/httpd/conf/httpd.conf /var/www/html/virus/test.txt',
                       f'wget http://{server_path}/password-protected-test.zip -O /var/www/html/virus/password-protected-test.zip',
                       f'wget http://{server_path}/Exploit.VBS.Agent.q.gz -O /var/www/html/virus/Exploit.VBS.Agent.q.gz',
                       f'wget http://{server_path}/upx.exe -O /var/www/html/virus/upx.exe'
                       ]
        output1 = PC4_login.send_commands(getfilecmds)
        if output1.count('100%') == 3:
            logger.info("Copy virus and anti-spyware file pass")
            # change http config file in PC4
            configfilecmds = [
                f'cp -f {CONF_PATH}/httpserver/* /etc/httpd/conf/',
                'systemctl restart httpd',
                'systemctl status httpd',
            ]
            output2 = PC4_login.send_commands(configfilecmds)
            res = True if 'running' in output2 else False
        else:
            logger.info("Copy virus and anti-spyware file fail")
        Assertion.assert_equal(res, True, "ERR: setup server on pc4 failed")

    def test_03_config_DNS_server_in_PC3(self):
        cmds = [
            f'\cp {CONF_PATH}/dnsserver/named.conf /etc/named.conf',
            f'\cp {CONF_PATH}/dnsserver/named.rfc1912.zones /etc/named.rfc1912.zones',
            f'\cp {CONF_PATH}/dnsserver/test.com.zone /var/named/test.com.zone',
            f'\cp {CONF_PATH}/dnsserver/test.com.local /var/named/test.com.local',
            'systemctl restart named',
            'systemctl status named',
        ]
        output = PC3_login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dns server in PC3 failed")

    def test_04_config_route_on_pc1_pc4(self):
        cmds = [f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.FIREWALL}']
        PC1_login.send_commands(cmds)
        cmd = f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.X2_IP}'
        PC2_login.send_command(cmd)
        cmds = [
            f'route add -net {Parameter.LOCAL_X0_NET}/24 gw {Parameter.REMOTE_X0_IP}',
            f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}'
        ]
        PC4_login.send_commands(cmds)
        Assertion.assert_equal(True, True, "ERR: PC2 and PC4 route settings failed")

    def test_05_run_STAF_in_PC1PC4_and_add_route_for_PC5PC6(self):
        output1 = False
        output2 = False
        logger.info('start run STAFProc service in PC1 and add route to remote net for PC5...')
        cmds = ['killall STAFProc', 'sleep 10']
        cmdres = PC1_login.send_commands(cmds)
        logger.info(f'clean staf service in PC1 result: {cmdres}')
        PC1_login.send_command('nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &')
        starres = PC1_login.send_command('pgrep -lf STAFProc')
        logger.info(f'start staf service in PC1 result: {starres}')
        for count in range(3):
            if 'STAFProc' in starres or 'nohup' in starres:
                cmds = [f'/usr/local/staf/bin/staf {PC5_ETH0_IP} process start shell command '
                        f'route add {Parameter.REMOTE_X0_NET} mask {Parameter.MASK} {Parameter.FIREWALL}',
                        ]
                routeres = PC1_login.send_commands(cmds)
                # make sure pc5 route added.
                os.system(cmds[0])
                logger.info(f'run staf in PC1 to add PC5 route result: {routeres}')
                output1 = True
                break
            else:
                time.sleep(10)
        logger.info('start run STAFProc service in PC4 and add route to remote net for PC6...')
        cmds = ['killall STAFProc', 'sleep 10']
        cmdres = PC4_login.send_commands(cmds)
        logger.info(f'clean staf service in PC4 result: {cmdres}')
        PC4_login.send_command('nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &')
        starres = PC4_login.send_command('pgrep -lf STAFProc')
        logger.info(f'start staf service in PC4 result: {starres}')
        for count in range(3):
            if 'STAFProc' in starres or 'nohup' in starres:
                cmds = [f'/usr/local/staf/bin/staf {PC6_ETH0_IP} process start shell command '
                        f'route add {Parameter.LOCAL_X0_NET} mask {Parameter.MASK} {Parameter.REMOTE_X0_IP}',
                        ]
                routeres = PC4_login.send_commands(cmds)
                # make sure pc5 route added.
                os.system(cmds[0])
                logger.info(f'run staf in PC1 to add PC5 route result: {routeres}')
                output2 = True
                break
            else:
                time.sleep(10)
        logger.info(f'pc1 check staf: {output1}, pc4 check staf: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: install stafproc in pc5 and pc6 failed.")
