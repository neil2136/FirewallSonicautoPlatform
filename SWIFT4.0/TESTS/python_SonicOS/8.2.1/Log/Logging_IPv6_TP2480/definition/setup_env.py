from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_X0_ipv6(self):
        logger.info("config X0 ipv6 interface... ")
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPv6,
            'managed': True,
            'other_config': True,
            'router_adv': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x0_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X0 ipv6 Failed!")
 
    def test_02_config_x1_interface(self):
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
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interfaceObj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_03_config_x1_interface_ipv6(self):
        logger.info("config x1 ipv6 interface... ")
        x1 = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv6 failed")

    def test_04_config_x2_interface(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_05_config_x2_interface_ipv6(self):
        logger.info("config x2 ipv6 interface... ")
        x2 = {
            'name': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv6 failed")

    @repeat_method(3)
    def test_06_register_fw(self):
        logger.info('config interface to dhcp...')
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    @repeat_method(3)
    def test_07_Restore_Remote_FW(self):
        logger.info(" {} ".center(20, '-').format('Restore Remote FW'))
        logger.info('add route on pc1...')
        cmd = 'route add -net 12.12.1.0 netmask 255.255.255.0 gw {}'.format(Parameter.FIREWALL)
        local_host.send_command(cmd)
        for i in range(10):
            out = os.popen('ping {} -c 1 -w 1'.format(Parameter.REMOTE_X1)).read()
            if ('100% packet loss' not in out):
                logger.info(out)
                break
            elif i == 9:
                logger.info('Remote DUT is unreachable. Check the network configuration.')
                ret = os.popen('route -n').read()
                logger.info('----- The route policies on PC1 after reset: -----')
                logger.info(ret)
           

        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN7 -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        for i in range(10):
            out = os.popen('ping {} -c 2'.format(Parameter.REMOTE_X1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    def test_08_config_x1_remote_interface_ipv6(self):
        logger.info("config x1 ipv6 remote interface... ")
        x1 = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X1_v6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = remote_interface_ipv6_obj.config_interface_ipv6(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv6 remote interface failed")

class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_setup_http_and_ftp_server(self):
        logger.info('setup http and ftp server...')
        logger.info('1. Do the configuration on http server...')
        html_file = TESTPATH + '/confs/index.html'
        flag = False
        logger.info('upload decode_viruses.py to pc2...')
        cmd = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + html_file +' root ' + Parameter.PC2_ETH0 + \
             ' /home '  + ' password 22'
        logger.info('run cmd on PC1:{}'.format(cmd))
        local_host.send_command(cmd)

        config_http_cmds = (
                "route add -net 11.11.1.0 netmask 255.255.255.0 gw {}".format(Parameter.FIREWALL),
                'cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak',
                "cp -rf /home/index.html \/var\/www\/html",
                'sed -i "s/^DocumentRoot .*/DocumentRoot \\"' \
                + '\/var\/www\/html\\"/"' \
                + ' /etc/httpd/conf/httpd.conf',
                'systemctl restart httpd ',
            )
        for cmd in config_http_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            pc2_ssh.send_command(cmd)

        logger.info('2. Do the configuration on ftp server...')
        config_ftp_cmds =(
                'sed -i /root/d /etc/vsftpd/ftpusers',
                'sed -i /root/d /etc/vsftpd/user_list',
                'systemctl restart vsftpd ',
        )
        for cmd in config_ftp_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            pc2_ssh.send_command(cmd)
        
        output1 = pc2_ssh.send_command('systemctl status httpd')
        output2 = pc2_ssh.send_command('systemctl status vsftpd')

        if re.search(r"active \(running", str(output1), re.S|re.I) and \
            re.search(r"active \(running", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup http and ftp server failed")