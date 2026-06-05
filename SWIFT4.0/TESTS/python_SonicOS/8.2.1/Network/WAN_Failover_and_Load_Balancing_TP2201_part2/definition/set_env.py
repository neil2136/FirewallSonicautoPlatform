from definition.init_param import *

class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = 'setup router and http ftp server'
    goto_teardown = True

    def test_01_setup_router_on_pc1(self):
        logger.info('setup router on pc1...')
        flag = False
        route_eth0_path = '/etc/sysconfig/network-scripts/route-eth0'
        cmds = (
            'route add -net {}/24 gw {}'.format(vpngw_x1_net, Parameter.X0_IP),
            'route add -net {}/24 gw {}'.format(vpngw_x0_net, Parameter.X0_IP),
            'route add -net {}/24 gw {}'.format(vpngw_x2_net, Parameter.X0_IP),
            'route add -net {}/24 gw {}'.format(rm_x0_net, Parameter.X0_IP),
            'echo \"{}/24 via {} dev eth0\" > {}'.format(vpngw_x0_net, Parameter.X0_IP, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(vpngw_x2_net, Parameter.X0_IP, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(vpngw_x1_net, Parameter.X0_IP, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(rm_x0_net, Parameter.X0_IP, route_eth0_path),
        )
        for cmd in cmds:
            logger.info('run cmd on pc1:{}'.format(cmd))
            local_host.send_command(cmd)
        output = local_host.send_command('route -n')
        if re.search('{}\s+{}'.format(vpngw_x0_net, Parameter.X0_IP), str(output), re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup router on pc1 failed")

    def test_02_setup_router_on_pc2(self):
        logger.info('setup router on pc2...')
        flag = False
        route_eth0_path = '/etc/sysconfig/network-scripts/route-eth0'
        cmds = (
            'route add -net {}/24 gw {}'.format(vpngw_x0_net, rm_x0),
            'route add -net {}/24 gw {}'.format(vpngw_x2_net, rm_x0),
            'route add -net {}/24 gw {}'.format(vpngw_x1_net, rm_x0),
            'route add -net {}/24 gw {}'.format(dut_x0_net, rm_x0),
            'echo \"{}/24 via {} dev eth0\" > {}'.format(vpngw_x0_net, rm_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(vpngw_x2_net, rm_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(vpngw_x1_net, rm_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(dut_x0_net, rm_x0, route_eth0_path),   
        )
        for cmd in cmds:
            logger.info('run cmd on pc2:{}'.format(cmd))
            pc2_ssh.send_command(cmd)
        output = pc2_ssh.send_command('route -n')
        if re.search('{}\s+{}'.format(vpngw_x0_net, rm_x0), str(output), re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup router on pc2 failed")


    def test_02_setup_router_on_pc_gw1(self):
        logger.info('setup router on pc_gw1...')
        flag = False
        dhcp_file = TESTPATH +'/confs/pc_gw1/dhcpd.conf'
        cmds = (
                'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
                'sysctl -p',
                "cp -rf {} /etc/dhcp/dhcpd.conf".format(dhcp_file),
                'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
                'dhcpd',
            )
        for cmd in cmds:
            logger.info('run cmd in pc_gw1:{}'.format(cmd))
            pc_gw1_ssh.send_command(cmd)

        output = pc_gw1_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"max-lease-time", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup router on pc gw1 failed")

    def test_03_setup_router_on_pc_gw2(self):
        logger.info('setup router on pc_gw2...')
        flag = False
        dhcp_file = TESTPATH +'/confs/pc_gw2/dhcpd.conf'
        cmds = (
                'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
                'sysctl -p',
                "cp -rf {} /etc/dhcp/dhcpd.conf".format(dhcp_file),
                'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
                'dhcpd',
            )
        for cmd in cmds:
            logger.info('run cmd in pc_gw2:{}'.format(cmd))
            pc_gw2_ssh.send_command(cmd)

        output = pc_gw2_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"max-lease-time", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup router on pc gw2 failed")

    def test_04_setup_http_and_ftp_server(self):
        logger.info('setup http and ftp server...')
        logger.info('1. Add a route on PC1 to PC_Server...')
        cmd = 'route add -host {} gw 192.168.168.168'.format(Parameter.PC_Server_ETH0)
        local_host.send_command(cmd)

        logger.info('2. Do the configuration on http server...')
        html_file = TESTPATH + '/confs/pc_server/html/index.html'

        logger.info('upload decode_viruses.py to pc4...')
        cmd = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + html_file +' root ' + Parameter.PC_Server_ETH1 + \
             ' /home '  + ' password 22'
        logger.info('run cmd on PC1:{}'.format(cmd))
        local_host.send_command(cmd)

        config_http_cmds = (
                "route add -net 11.11.11.0 netmask 255.255.255.0 gw {}".format(Parameter.PC_GW1_ETH0),
                "route add -net 12.12.2.0 netmask 255.255.255.0 gw {}".format(Parameter.PC_GW2_ETH0),
                'cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak',
                "cp -rf /home/index.html \/var\/www\/html",
                'sed -i "s/^DocumentRoot .*/DocumentRoot \\"' \
                + '\/var\/www\/html\\"/"' \
                + ' /etc/httpd/conf/httpd.conf',
                'service httpd restart',
            )
        for cmd in config_http_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            output1 = pc_server_ssh.send_command(cmd)

        logger.info('3. Do the configuration on ftp server...')
        config_ftp_cmds =(
                'sed -i /root/d /etc/vsftpd/ftpusers',
                'sed -i /root/d /etc/vsftpd/user_list',
                'service vsftpd restart',
        )
        for cmd in config_ftp_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            output2 = pc_server_ssh.send_command(cmd)

        if re.search(r"OK", str(output1), re.S|re.I) and \
            re.search(r"OK", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup http and ftp server failed")
