from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial firewall"
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
        rc = interfaceObj.config_interface(**x1)
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
        rc = interfaceObj.config_interface(**x2)
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
        rc = interfaceObj.config_interface(**x3)
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
        rc = interfaceObj.config_interface(**x4)
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
        rc = interfaceObj.config_interface(**x5)
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
        if re.search(r'{}\s+{}'.format(HTTP_Server, Parameter.FIREWALL), str(output), re.I|re.DOTALL):
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
            'cp {}/httpd.conf /etc/httpd/conf'.format(binPath),
            'cp {}/index.html /var/www/html/'.format(binPath),
            'systemctl start httpd',            
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            server_ssh.send_command(cmd)
        
        sleep(5)
        output = server_ssh.send_command('systemctl status httpd')
        if re.search(r'running', str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start server HTTP service failed")

    def test_02_start_server_DHCP_service_gw1(self):
        logger.info('start server DHCP service gw1...')
        flag = False
        cmds = (
                'echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf',
                'sysctl -p',
                "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_1),
                'echo "DHCPDARGS=eth2" >> /etc/sysconfig/dhcpd',
                'systemctl start dhcpd',
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            gw1_ssh.send_command(cmd)

        output = gw1_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"subnet 13.0.11.0", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start server DHCP service on gw1 failed")

    def test_03_start_server_DHCP_service_gw2(self):
        logger.info('start server DHCP service gw2...')
        flag = False
        cmds = (
                'echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf',
                'sysctl -p',
                "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_2),
                'echo "DHCPDARGS=eth2" >> /etc/sysconfig/dhcpd',
                'systemctl start dhcpd',
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            gw2_ssh.send_command(cmd)

        output = gw2_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"subnet 13.0.12.0", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start server DHCP service on gw2 failed")

    def test_04_start_server_DHCP_service_gw3(self):
        logger.info('start server DHCP service gw3...')
        flag = False
        cmds = (
                'echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf',
                'sysctl -p',
                "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_3),
                'echo "DHCPDARGS=eth2" >> /etc/sysconfig/dhcpd',
                'systemctl start dhcpd',
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            gw3_ssh.send_command(cmd)

        output = gw3_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"subnet 13.0.13.0", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start server DHCP service on gw3 failed")

    def test_05_start_server_DHCP_service_gw4(self):
        logger.info('start server DHCP service gw4...')
        flag = False
        cmds = (
                'echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf',
                'sysctl -p',
                "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_4),
                'echo "DHCPDARGS=eth2" >> /etc/sysconfig/dhcpd',
                'systemctl start dhcpd',
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            gw4_ssh.send_command(cmd)

        output = gw4_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"subnet 13.0.14.0", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start server DHCP service on gw4 failed")

    def test_06_start_server_DHCP_service_gw5(self):
        logger.info('start server DHCP service gw5...')
        flag = False
        cmds = (
                'echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf',
                'sysctl -p',
                "echo \"{}\" >> /etc/dhcp/dhcpd.conf".format(dhcpdcfg_5),
                'echo "DHCPDARGS=eth2" >> /etc/sysconfig/dhcpd',
                'systemctl start dhcpd',
        )
        for cmd in cmds:
            logger.info('run cmd on server:{}'.format(cmd))
            gw5_ssh.send_command(cmd)

        output = gw5_ssh.send_command('cat /etc/dhcp/dhcpd.conf')
        if re.search(r"subnet 13.0.15.0", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start server DHCP service on gw5 failed")


class TestConfigTB_03(Test):
    uuid = 'NonTC'
    description = "setup pppoe server"
    goto_teardown = True

    def test_01_setup_pppoe_server_on_gw2(self):
        logger.info('setup pppoe server on gw2...')
        flag = False
        logger.info(f"{' Install pppoe-server-env ':=^50}")
        cmds = (
            'echo "INT=eth2" > /etc/ppp/pppoe-server-env ',
            'echo "LOCAL={}" >> /etc/ppp/pppoe-server-env'.format(ip_pool_start_X2),
            'echo "START={}" >> /etc/ppp/pppoe-server-env'.format(ip_pool_end_X2),
            'echo "NUMBER=10" >> /etc/ppp/pppoe-server-env'
        )
        for cmd in cmds:
            logger.info('run cmd on gw2:{}'.format(cmd))
            gw2_ssh.send_command(cmd)

        logger.info(f"{'Copy pppoe to gw2 ':=^50}")

        logger.info(f"{' Setup chap-secrets ':=^50}")
        cmd_cp_chap = f'\cp -rf /{binPath}/chap-secrets  /etc/ppp/chap-secrets'
        gw2_ssh.send_command(cmd_cp_chap)
        
        # logger.info(f"{' Setup pppoe-server-options ':=^50}")
        # cmd_cp_pppoe_server = f'\cp -rf /{binPath}/pppoe-server-options  /etc/ppp/pppoe-server-options'
        # gw2_ssh.send_command(cmd_cp_pppoe_server)

        logger.info(f"{' Setup pppoe-server-service ':=^50}")
        cmd_cp_pppoe_service= f'\cp -rf /{binPath}/pppoe-server.service /etc/systemd/system/'
        gw2_ssh.send_command(cmd_cp_pppoe_service)

        logger.info(f"{' start pppoe-server-service ':=^50}")

        gw2_ssh.send_command('systemctl start pppoe-server')
        # gw2_ssh.send_command('systemctl enable pppoe-server')
        output = gw2_ssh.send_command('systemctl status pppoe-server')
        if re.search(r"running", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup pppoe server on gw2 failed")

    def test_02_setup_pppoe_server_on_gw3(self):
        logger.info('setup pppoe server on gw3...')
        flag = False
        logger.info(f"{' Install pppoe-server-env ':=^50}")
        cmds = (
            'echo "INT=eth2" > /etc/ppp/pppoe-server-env ',
            'echo "LOCAL={}" >> /etc/ppp/pppoe-server-env'.format(ip_pool_start_X3),
            'echo "START={}" >> /etc/ppp/pppoe-server-env'.format(ip_pool_end_X3),
            'echo "NUMBER=10" >> /etc/ppp/pppoe-server-env'
        )
        for cmd in cmds:
            logger.info('run cmd on gw2:{}'.format(cmd))
            gw3_ssh.send_command(cmd)

        logger.info(f"{'Copy pppoe to gw2 ':=^50}")

        logger.info(f"{' Setup chap-secrets ':=^50}")
        cmd_cp_chap = f'\cp -rf /{binPath}/chap-secrets  /etc/ppp/chap-secrets'
        gw3_ssh.send_command(cmd_cp_chap)
        
        # logger.info(f"{' Setup pppoe-server-options ':=^50}")
        # cmd_cp_pppoe_server = f'\cp -rf /{binPath}/pppoe-server-options  /etc/ppp/pppoe-server-options'
        # gw3_ssh.send_command(cmd_cp_pppoe_server)

        logger.info(f"{' Setup pppoe-server-service ':=^50}")
        cmd_cp_pppoe_service= f'\cp -rf /{binPath}/pppoe-server.service /etc/systemd/system/'
        gw3_ssh.send_command(cmd_cp_pppoe_service)

        logger.info(f"{' start pppoe-server-service ':=^50}")

        gw3_ssh.send_command('systemctl start pppoe-server')
        # gw3_ssh.send_command('systemctl enable pppoe-server')
        output = gw3_ssh.send_command('systemctl status pppoe-server')
        if re.search(r"running", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup pppoe server on gw2 failed")