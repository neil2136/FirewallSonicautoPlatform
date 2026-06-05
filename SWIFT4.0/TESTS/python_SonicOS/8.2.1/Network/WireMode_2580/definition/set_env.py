from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(10)
    def test_02_register_fw(self):
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = 'test download and decode viruses on server'
    goto_teardown = True


    def test_01_00_upload_viruses_to_pc4(self):
        viruses = (
                '1.cab.bin.base.base',
                'klez.h.bin.base.base',
                'normal.txt.base.base',
                'test.txt.base.base',
                )
        flag = False
        logger.info('create {} to store downloaded virus files..'.format(Parameter.TMP_PATH))
        pc4_ssh.send_command('mkdir {}'.format(Parameter.TMP_PATH))
        
        output = pc4_ssh.send_command('ping -c 5 {}'.format(Parameter.WEB_SERVER))
        pattern = r". packets transmitted, . received, 0% packet loss"
        match = re.search(pattern, output, re.S)
        if match:
            logger.info("check network status,normally")
            flag = True 
        else:
            logger.error('the network has down!')

        logger.info('upload decode_viruses.py to pc4...')
        cmd = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '{}/decode_viruses.py '.format(decodePath) +' root ' + Parameter.PC4_ETH1 + \
             ' /home '  + ' password 22'
        logger.info('run cmd on PC4:{}'.format(cmd))
        local_host.send_command(cmd)
        # download from web server
        logger.info('Download virus files from {}, and decode them'.format(Parameter.WEB_SERVER))
        for virus in viruses: 
            cmd = 'wget -O {}/{} http://{}/DPISSL/POP3S/{}'.format(Parameter.TMP_PATH, virus, Parameter.WEB_SERVER, virus)
            pc4_ssh.send_command(cmd)
        # decode viruses files
        logger.info('Already download viruses file from server, start to decode..')
        cmd = 'python {} {}'.format( '/home/decode_viruses.py', Parameter.TMP_PATH)
        pc4_ssh.send_command(cmd)
        logger.info('Check if the virus is decompressed...')
        cmd_check = 'ls -l {}'.format(Parameter.TMP_PATH)
        output_check = pc4_ssh.send_command(cmd_check)
        logger.info(output_check)
        if re.search(r'klez.h.bin', str(output_check), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: download and decode viruses on pc4 failed')

    def test_01_01_config_route_on_pc3_and_pc4(self):
        logger.info('config route on pc3 and pc4...')
        cmds = ("echo 'any net 172.16.4.0/24 dev eth0' >> /etc/sysconfig/static-routes",
                "systemctl restart network",
                "echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse",
                "echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle")
        for cmd in cmds:
            logger.info('run cmd on pc3:{}'.format(cmd))
            pc3_ssh.send_command(cmd)

        cmds = ( "echo 'any net 172.16.3.0/24 dev eth0' >> /etc/sysconfig/static-routes",
                "systemctl restart network",
                "echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse",
                "echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle")
        for cmd in cmds:
            logger.info('run cmd on pc3:{}'.format(cmd))
            pc4_ssh.send_command(cmd)
        Assertion.assert_equal(True, True, 'ERR: config route on pc3 and pc4 failed')

    def test_01_02_initialize_environment(self):
        config_ftp_cmds =(
                'sed -i /root/d /etc/vsftpd/ftpusers',
                'sed -i /root/d /etc/vsftpd/user_list',
                'systemctl restart vsftpd ',
        )
        for cmd in config_ftp_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            pc3_ssh.send_command(cmd)
            pc4_ssh.send_command(cmd)

        output1 = pc3_ssh.send_command('systemctl status vsftpd')
        output2 = pc4_ssh.send_command('systemctl status vsftpd')

        if re.search(r"active \(running", str(output1), re.S|re.I) and \
            re.search(r"active \(running", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup http and ftp server failed")

    

class TestSetup_Https_Server(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_02_00_initialize_environment(self):
        logger.info('[ SET UP 1/4 ] on PC4, copy html files...')
        logger.info('run cmd: cp -r {}/* /var/www/https')
        pc4_ssh.send_command('mkdir -p /var/www/https')
        pc4_ssh.send_command('cp -r {}/* /var/www/https'.format(WWW_PATH))

        logger.info("[ SET UP 2/4 ] on PC4, install 'mod_ssl' for Apache to get SSL support...")
        pc4_ssh.send_command('yum -y install mod_ssl openssl')

        for i in range(2):
            logger.info('Modify the ssl.conf fro the {} time!'.format(i))
            pc4_ssh.send_command('rm -f /etc/httpd/conf.d/ssl.conf')
            pc4_ssh.send_command('\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(configPath))
            output = pc4_ssh.send_command('grep /www/https /etc/httpd/conf.d/ssl.conf')
            if re.search(r'/www/https', str(output), re.S|re.I):
                logger.info('Overwrite ssl.conf successfully in the {} times...'.format(i))
            else:
                logger.info('Fail to modify ssl.conf in the {} times...'.format(i))
        logger.info('upload httpd.conf to pc4...')
        cmd_httpd = 'python3 {}'.format(toolPath+'/upload_or_download_file.py upload scp ')  + '{}/httpd.conf'.format(resPath) +' root ' + PC4_ETH1_IP + \
            ' /etc/httpd/conf/' + ' password 22'
        logger.info('run cmd:{}'.format(cmd_httpd))
        local_host.send_command(cmd_httpd)

        logger.info('upload index.html to pc4...')
        cmd_html = 'python3 {}'.format(toolPath+'/upload_or_download_file.py upload scp ')  + '{}/index.html'.format(resPath) +' root ' + PC4_ETH1_IP + \
            ' /var/www/https/' + ' password 22'
        logger.info('run cmd:{}'.format(cmd_html))
        local_host.send_command(cmd_html)
        pc4_ssh.send_command('echo "this is http server!" > /var/www/https/index.html')

        logger.info('[ SET UP 3/4 ] on PC4, copy certificate files and key files...')
        pc4_ssh.send_command('install {}/* /etc/pki/tls/certs/'.format(certPath))
        pc4_ssh.send_command('install {}/* /etc/pki/tls/private/'.format(certPath))

        logger.info('[ SET UP 4/4 ] on PC4, copy socat to PC4...')
        pc4_ssh.send_command('install {}/socat /usr/local/bin/'.format(binPath))

        Assertion.assert_equal(True, True, "ERR: initialize the environment failed")


    def test_02_01_start_https_server(self):
        logger.info('Starting Httpd...!')
        flag = False
        httpd_status = pc4_ssh.send_command('systemctl status httpd')
        if re.search(r'active \(running\)', str(httpd_status), re.S|re.I):
            logger.info('Httpd is already running! Stop it!')
            pc4_ssh.send_command('systemctl restart httpd')
        else:
            pc4_ssh.send_command('systemctl start httpd')

        httpd_status = pc4_ssh.send_command('systemctl status httpd')
        logger.info(httpd_status)
        if re.search(r'active \(running\)', str(httpd_status), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start https server failed")
