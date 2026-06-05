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
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")
    
    def test_03_config_interface_x3(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_04_config_interface_x4(self):
        logger.info("config x4 interface... ")
        x4 = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X4_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x4)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 failed")

    def test_05_config_interface_x5(self):
        logger.info("config x5 interface... ")
        x5 = {
            'if': 'X5',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X5_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x5)
        Assertion.assert_equal(rc, True, "ERR: Config X5 IPv4 failed")

    def test_06_change_route_on_pc_server(self):
        logger.info('change route on pc server...')
        cmds = (
            "route add -net 13.0.11.0/24 gw {}".format(Parameter.GW1_ETH1),
            "route add -net 13.0.12.0/24 gw {}".format(Parameter.GW2_ETH1),
            "route add -net 13.0.13.0/24 gw {}".format(Parameter.GW3_ETH1),
            "route add -net 13.0.14.0/24 gw {}".format(Parameter.GW4_ETH1),
            "route add -net 13.0.15.0/24 gw {}".format(Parameter.GW5_ETH1),
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list"
        )
        for cmd in cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            server_ssh.send_command(cmd)
        Assertion.assert_equal(True, True, "ERR: change route on pc server failed")

    def test_07_change_route_on_pc1(self):
        logger.info('change route on pc1....')
        cmd  = "route add -host {} gw {}".format(Parameter.SERVER_ETH1, Parameter.FIREWALL)
        local_host.send_command(cmd)
        output = local_host.send_command('route -n')
        if re.search(r'{}\s+{}'.format(IP_Server, Parameter.FIREWALL), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: change route on pc1 failed")

    def test_08_config_on_gw(self):
        logger.info('config on pc gw...')
        cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
        gw1_ssh.send_command(cmd)
        gw2_ssh.send_command(cmd)
        gw3_ssh.send_command(cmd)
        gw4_ssh.send_command(cmd)
        gw5_ssh.send_command(cmd)
        Assertion.assert_equal(True, True, "ERR: config on gw failed")

class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_start_server_HTTP_service(self):
        logger.info('start server HTTP service...')
        flag = False
        Path = binPath.replace('/','\/')
        cmds = (
            'cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak',
            'sed -i "s/^DocumentRoot .*/DocumentRoot \\"' \
                + '{}\/var\/www\/html\\"/"'.format(Path) \
                + ' /etc/httpd/conf/httpd.conf',
            'service httpd restart',            
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            server_ssh.send_command(cmd)
        
        sleep(5)
        output = server_ssh.send_command('service httpd status')
        if re.search(r'running', str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start server HTTP service failed")

    # def test_02_start_server_DHCP_service_gw1(self):
    #     logger.info('start server DHCP service gw1...')
      
    #     cmds =  (
    #             'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
    #             'sysctl -p',
    #             'cat /proc/sys/net/ipv4/ip_forward',
    #             '>/etc/dhcp/dhcpd.conf',
    #             "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_1),
    #             'cat /etc/dhcp/dhcpd.conf',
    #             'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
    #             'dhcpd',
    #         )
    #     for cmd in cmds:
    #         logger.info('run cmd on server:{}'.format(cmd))
    #         gw1_ssh.send_command(cmd)

      
    #     Assertion.assert_equal(True, True, "ERR: start server DHCP service on gw1 failed")

    # def test_03_start_server_DHCP_service_gw2(self):
    #     logger.info('start server DHCP service gw2...')
  
    #     cmds =  (
    #             'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
    #             'sysctl -p',
    #             'cat /proc/sys/net/ipv4/ip_forward',
    #             '>/etc/dhcp/dhcpd.conf',
    #             "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_2),
    #             'cat /etc/dhcp/dhcpd.conf',
    #             'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
    #             'dhcpd',
    #         )
    #     for cmd in cmds:
    #         logger.info('run cmd on server:{}'.format(cmd))
    #         gw2_ssh.send_command(cmd)

    #     Assertion.assert_equal(True, True, "ERR: start server DHCP service on gw2 failed")

    # def test_04_start_server_DHCP_service_gw3(self):
    #     logger.info('start server DHCP service gw3...')

    #     cmds =  (
    #             'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
    #             'sysctl -p',
    #             'cat /proc/sys/net/ipv4/ip_forward',
    #             '>/etc/dhcp/dhcpd.conf',
    #             "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_3),
    #             'cat /etc/dhcp/dhcpd.conf',
    #             'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
    #             'dhcpd',
    #         )
    #     for cmd in cmds:
    #         logger.info('run cmd on server:{}'.format(cmd))
    #         gw3_ssh.send_command(cmd)

  
    #     Assertion.assert_equal(True, True, "ERR: start server DHCP service on gw3 failed")

    # def test_05_start_server_DHCP_service_gw4(self):
    #     logger.info('start server DHCP service gw4...')
  
    #     cmds =  (
    #             'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
    #             'sysctl -p',
    #             'cat /proc/sys/net/ipv4/ip_forward',
    #             '>/etc/dhcp/dhcpd.conf',
    #             "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_4),
    #             'cat /etc/dhcp/dhcpd.conf',
    #             'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
    #             'dhcpd',
    #         )
    #     for cmd in cmds:
    #         logger.info('run cmd on server:{}'.format(cmd))
    #         gw4_ssh.send_command(cmd)


    #     Assertion.assert_equal(True, True, "ERR: start server DHCP service on gw4 failed")

    # def test_06_start_server_DHCP_service_gw5(self):
    #     logger.info('start server DHCP service gw5...')
  
    #     cmds =  (
    #             'sed -i "s/net.ipv4.ip_forward = .*/net.ipv4.ip_forward = 1/" /etc/sysctl.conf',
    #             'sysctl -p',
    #             'cat /proc/sys/net/ipv4/ip_forward',
    #             '>/etc/dhcp/dhcpd.conf',
    #             "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_5),
    #             'cat /etc/dhcp/dhcpd.conf',
    #             'sed -i "s/DHCPDARGS=/DHCPDARGS=eth2/" /etc/sysconfig/dhcpd',
    #             'dhcpd',
    #         )
    #     for cmd in cmds:
    #         logger.info('run cmd on server:{}'.format(cmd))
    #         gw5_ssh.send_command(cmd)
    
    #     Assertion.assert_equal(True, True, "ERR: start server DHCP service on gw5 failed")