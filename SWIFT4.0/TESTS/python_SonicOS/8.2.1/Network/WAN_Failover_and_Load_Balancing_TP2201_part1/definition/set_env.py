from definition.init_param import *

class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = 'setup router and http ftp server'
    goto_teardown = True

    def test_01_setup_router_on_pc_gw1(self):
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

    def test_02_setup_router_on_pc_gw2(self):
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

    def test_03_setup_http_and_ftp_server(self):
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
                "route add -net 13.11.0.0 netmask 255.255.255.0 gw {}".format(Parameter.PC_GW1_ETH0),
                "route add -net 13.12.0.0 netmask 255.255.255.0 gw {}".format(Parameter.PC_GW2_ETH0),
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


class TestConfigTB_02(Test):
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
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    @repeat_method(3)
    def test_03_register_fw(self):
        logger.info('config interface to dhcp...')
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    # def test_04_config_interface_to_dhcp(self):
    #     logger.info('config wan interface to dhcp...')
    #     x1 = {
    #         'if': 'X1',
    #         'zone': 'WAN',
    #         'mode': 'dhcp',
    #         'mgmt_snmp': True,
    #     }
    #     x2 = {
    #         'if': 'X2',
    #         'zone': 'WAN',
    #         'mode': 'dhcp',
    #         'mgmt_snmp': True,
    #     }
    #     rc = interfaceObj.config_interface(**x1)
    #     rc &= interfaceObj.config_interface(**x2)
    #     Assertion.assert_equal(rc, True, "ERR: config wan interface to dhcp failed")


    # def test_05_config_dns(self):
    #     logger.info('config dns...')
    #     dns_dict = {
    #         "dns": {
    #             "server": {
    #                 "inherit": False,
    #                 "static": {
    #                     "primary": dns1,
    #                     "secondary": dns2,
    #                     "tertiary": dns3
    #                 },
    #                 "ipv6": {
    #                     "inherit": True,
    #                     "static": {
    #                         "primary": "::",
    #                         "secondary": "::",
    #                         "tertiary": "::"
    #                     },
    #                     "preferred": False
    #                 }
    #             },
    #             "rebinding": {
    #                 "enable": False,
    #                 "action": "log-attack-only",
    #                 "allowed_domains": {}
    #             },
    #             "fqdn_binding": False,
    #             "split_servers": True,
    #             "fqdn_over_tcp_dns": False
    #         }
    #     }
    #     rc = dnsObj.set_dns(**dns_dict)
    #     Assertion.assert_equal(rc, True, "ERR: config dns failed")

    # def test_06_config_LB_group(self):
    #     logger.info('Edit the default LB group...')
    #     lb = {
    #         "failover_lb": {
    #             "group": [
    #                 {
    #                     "name": " Default LB Group",
    #                     "type": "basic",
    #                     "final_backup": "",
    #                     "preempt": True,
    #                     "probing": {
    #                         "health_check": 5,
    #                         "missed_intervals": 3,
    #                         "successful_intervals": 3,
    #                         "global_responder": False
    #                     },
    #                     "interface": [
    #                         {
    #                             "name": "X1",
    #                             "rank": 1,
    #                             "probe_type": "physical",
    #                             "probe_condition": "always"
    #                         },
    #                         {
    #                             "name": "X2",
    #                             "rank": 2
    #                         },
    #                         {}
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    #     rc = failoverlbObj.config_failover_groups_by_multi(**lb)
    #     Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    # def test_07_config_interfaces_under_LB_group(self):
    #     logger.info('config interfaces under LB group...')
    #     lb1 = {
    #         'type': 'basic',
    #         'interface': 'X1',
    #         'rank':1,
    #         'probe_type': 'logical',
    #         "probe_option": "either",
    #         'main_protocol':'ping',
    #         'main_value': True,
    #         'main_host': Parameter.PC_GW1_ETH2,
    #         'alter_protocol':'tcp',
    #         'alter_value': 22,
    #         'alter_host': Parameter.PC_GW1_ETH2,
    #         'default_value': '0.0.0.0'
    #     }
    #     lb2 = {
    #         'type': 'basic',
    #         'interface': 'X2',
    #         'rank':2,
    #         'probe_type': 'logical',
    #         "probe_option": "either",
    #         'main_protocol':'ping',
    #         'main_value': True,
    #         'main_host': Parameter.PC_GW2_ETH2,
    #         'alter_protocol':'tcp',
    #         'alter_value': 22,
    #         'alter_host': Parameter.PC_GW2_ETH2,
    #         'default_value': '0.0.0.0'
    #     }
    #     rc = failoverlbObj.config_failover_groups(**lb1)
    #     rc &= failoverlbObj.config_failover_groups(**lb2)
    #     Assertion.assert_equal(rc, True, "ERR: config interfaces under LB group failed")
