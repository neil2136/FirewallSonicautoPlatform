from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_x1(self):
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
        logger.info('register fw..')
        rc = licenseObj.register('online')
        Assertion.assert_equal(rc, True, 'ERR: Register fw failed')

    def test_03_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_04_config_interface_x3(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_05_add_addrobj(self):
        logger.info('add address object...')
        obj = {
            'object_type': 'host',
            'name': 'WAN Host',
            'zone': 'WAN',
            'value': PC2_WAN_IP,
        }
        rc = addressObj.config_addressobject(**obj)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add WAN Host Address Object")

    def test_06_config_dhcp_file_and_add_route_in_pc2(self):
        logger.info('config dhcp file in pc2 and add route...')
        flag = False
        pc2_ssh.send_command("\cp -f {}/confs/dhcp.conf /etc/dhcp/dhcpd.conf".format(TESTPATH))
        pc2_ssh.send_command('route add -net 192.168.168.0/24 gw {}'.format(Parameter.X1_IP))
        output = pc2_ssh.send_command('route -n')
        logger.info(output)
        if re.search(r'192.168.168.0\s+{}'.format(Parameter.X1_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config dhcp file in pc2 and add route failed")

    def test_07_disable_dhcp_server(self):
        dhcp_server_opt = {
            "dhcp_server": {
                "ipv4": {
                    "enable": False
                    , "conflict_detection": True
                    , "persistence": True
                    , "persistence_monitoring_interval": 5
                    , "trusted_relay_agents": ""
                    , "recycle_expired_lease": 0
                }
            }
        }
        rc = dhcpObj.config_dhcp_server_settings(**dhcp_server_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp server on fw failed!")

    def test_08_chmod_exe_subbroadcast(self):
        logger.info('copy py file to local path...')
        cmds = (
            'mkdir -p /root/iphelper ',
            '\cp -rf {}/* /root/iphelper'.format(confPath)
        )
        
        for cmd in cmds:
            sleep(1)
            logger.info('run cmd :'.format(cmd))
            local_host.send_command(cmd)
            pc2_ssh.send_command(cmd)

        output = local_host.send_command('ls -l /root/iphelper')
        if re.search(r'subbroadcast', str(output), re.S|re.I):
            local_host.send_command('chmod a+x /root/iphelper/subbroadcast')

        local_host.send_command('yum install -y nc')


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
                'packed_upx.exe.base.base'
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
        cmd = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '{}/decode_viruses.py '.format(toolPath) +' root ' + Parameter.PC4_ETH1 + \
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


        logger.info('[ SET UP 3/4 ] on PC4, copy certificate files and key files...')
        pc4_ssh.send_command('install {}/* /etc/pki/tls/certs/'.format(certPath))
        pc4_ssh.send_command('install {}/* /etc/pki/tls/private/'.format(certPath))

        logger.info('[ SET UP 4/4 ] on PC4, copy socat to PC4...')
        pc4_ssh.send_command('install {}/socat /usr/local/bin/'.format(binPath))

        Assertion.assert_equal(True, True, "ERR: initialize the environment failed")


    def test_02_01_start_https_server(self):
        logger.info('Starting Httpd...!')
        flag = False
        httpd_status = pc4_ssh.send_command('service httpd status')
        if re.search(r'running', str(httpd_status), re.S|re.I):
            logger.info('Httpd is already running! Stop it!')
            pc4_ssh.send_command('service httpd stop')

        for i  in range(2):
            httpd_status = pc4_ssh.send_command('service httpd start')
            logger.info(httpd_status)
            if re.search(r'OK', str(httpd_status), re.S|re.I):
                logger.info('Start httpd successfully in the {} times'.format(i))
                flag = True
                break
            else:
                logger.info('Failed to start httpd!')
                logger.info('Clean up the environment and restart httpd...')
                output_httpd = pc4_ssh.send_command("netstat -ltnp |grep ':80'")
                output = re.search(r'(\d+)(/socat)', str(output_httpd), re.S|re.I)
                if output != None:
                    pid = output.group(1)
                    logger.info('My PID is {}'.format(pid))
                    pc4_ssh.send_command('kill -9 {}'.format(pid))
                else:
                    pc4_ssh.send_command('pkill socat')
                    sleep(1)
                pc4_ssh.send_command('service httpd stop')
                    
        Assertion.assert_equal(flag, True, "ERR: start https server failed")
