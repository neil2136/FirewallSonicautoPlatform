from definition.initial_parameter import *


class Test_IPv6_DHCP_Client_2474_04(Test):
    uuid = "SOSAIOT-TC-56430"
    description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_DHCPV6_Server(self):
        dhcp_server_ipv6_scope = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": "3000::",
                                "range": {
                                    "from": "3000::5",
                                    "to": "3000::9"
                                }
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcp_v6_server.add_dhcp_server_scope_dynamic(**dhcp_server_ipv6_scope)
        Assertion.assert_equal(rc, True, "ERR: failed to add dhcpv6 dynamic scope")

    def test_02_config_packet_monitor(self):
        result = list()
        found = 0
        result.append(packet_obj.stop_capture())
        time.sleep(2)
        result.append(packet_obj.clear_packets())
        time.sleep(2)
        pc_info = {
            'monitor_filter': {
                'interfaces': 'X1',
            }
        }
        result.append(packet_obj.conf_packmon(**pc_info))
        time.sleep(2)
        result.append(packet_obj.start_capture())
        for i in result:
            if i == True:
                found += 1
        Assertion.assert_equal(found, 4, "ERR: configure packet monitor failed")

    def test_03_config_X1_DHCPv6_Mode(self):
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'zone': 'WAN',
            "dhcpv6": {"rapid_commit": True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: config client X1 IPv6 failed")

    def test_04_verify_result(self):
        time.sleep(5)
        packet_obj.stop_capture()
        packet_obj.export_captured_packets_pcapng()
        out = localhost.send_command('tshark -V -r /tmp/packet-c.pcapng')
        Assertion.assert_regular(out, 'Rapid Commit', "ERR: check packets failed")

    def test_05_del_dhcpv6_scope(self):
        time.sleep(2)
        rc = dhcp_v6_server.del_dhcp_server_scope_dynamic(version=6, name='scope_ipv6')
        Assertion.assert_equal(rc, True, "ERR: failed to add dhcpv6 dynamic scope")

    def test_06_config_X1_auto_Mode(self):
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'auto',
            'zone': 'WAN',
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: config client X1 IPv6 failed")


class Test_IPv6_DHCP_Client_2474_29(Test):
    uuid = "SOSAIOT-TC-56432"
    description = show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_DHCPV6_Server(self):
        dhcp_server_ipv6_scope = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": "3000::",
                                "range": {
                                    "from": "3000::5",
                                    "to": "3000::9"
                                }
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcp_v6_server.add_dhcp_server_scope_dynamic(**dhcp_server_ipv6_scope)
        Assertion.assert_equal(rc, True, "ERR: failed to add dhcpv6 dynamic scope")

    def test_02_config_X1_DHCPv6_Mode(self):
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'zone': 'WAN',
            "dhcpv6": {"rapid_commit": True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        time.sleep(10)
        # check if X1 has got ipv6 address
        ip_addr = interface_ipv4.get_interface_address(name='X1', version='v6')
        ipv6_got = ip_addr['ip_address']
        Assertion.assert_regular(ip_addr['ip_address'], '3000::', "ERR: config client X1 IPv6 failed")

    def test_03_release_address(self):
        interface_ipv4.click_dhcp_release(name='X1', version='v6')
        time.sleep(5)
        ip_addr = interface_ipv4.get_interface_address(name='X1', version='v6')
        Assertion.assert_not_regular(ip_addr['ip_address'], '3000::', "ERR: config client X1 IPv6 failed")

    @repeat_method(5)
    def test_04_renew_address(self):
        interface_ipv4.click_dhcp_renew(name='X1', version='v6')
        time.sleep(10)
        ip_addr = interface_ipv4.get_interface_address(name='X1', version='v6')
        Assertion.assert_regular(ip_addr['ip_address'], X1_Prefix, "ERR: config client X1 IPv6 failed")

    @repeat_method(5)
    def test_05_cleanup(self):
        time.sleep(6)
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'auto',
            'zone': 'WAN',
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        rc &= dhcp_v6_server.del_dhcp_server_scope_dynamic(version=6, name='scope_ipv6')
        Assertion.assert_equal(rc, True, "ERR: cleanup failed ")


class Test_IPv6_DHCP_Client_2474_27(Test):
    uuid = "SOSAIOT-TC-56430"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']
    dibbler_server = Params.testbed + '-PC1'

    def test_14_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @parameterized.expand([('LAN'),
                           ('WAN'),
                           ('DMZ')])
    def test_14_01_vlan_interface_diffrent_zone(self, zone):
        x2_vlan = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': PC1_vlan_eth2,
            'zone': zone,
            'mode': 'static',
            'ip': '2.2.2.10',
            'gateway': '2.2.2.20',
        }

        logger.info("start_dibbler..............\n")
        # dibbler_server = Params.testbed + '-PC3'
        log_file = '/tmp/dibbler.log'
        dibbler = Host(self.dibbler_server)
        logger.info(f'Mkdir /var/lib/dibbler,/etc/dibbler on {self.dibbler_server}')
        dibbler.send_command('mkdir -p /var/lib/dibbler')
        dibbler.send_command('mkdir -p /etc/dibbler')
        dibbler.send_command('mv /etc/dibbler/server.conf /etc/dibbler/server.conf.bak')
        dibbler.send_command(f'cp {Parameter.DIBBLER_SERVER_CONF} /etc/dibbler/')
        rc = dibbler.start_DHCP_server()
        if rc:
            logger.info("Start dhcp server successfully.\n")
        else:
            logger.error("ERR: Start dhcp server failed.\n")

        logger.info("add vlan interface.............\n")
        rc1 = interface_ipv4.add_interface(**x2_vlan)

        x2_vlan_v6 = {
            'name': 'X2',
            'vlan': PC1_vlan_eth2,
            'mode': 'dhcpv6',
            'zone': 'WAN',
            'mgmg_ping': True,
            'dhcpv6': {
                'mode': 'auto',
            }
        }
        rc1 &= interface_ipv6.config_interface_ipv6(**x2_vlan_v6)
        if rc1:
            logger.info("Add sub interface successfully.\n")
        else:
            logger.error("ERR: Add sub interface failed.\n")

        logger.info("verify DUT got dhcpv6 addr.............\n")
        rc2 = False
        for each in range(0, 5):
            time.sleep(10)
            x2_dict = interface_ipv6.get_interface_address(
                name='X2/vlan/' + str(PC1_vlan_eth2))
            try:
                ip = x2_dict['ip_address']
            except:
                logger.error('Fail to get X1 ipv6.')
                logger.info(x2_dict)
                ip = ''
            if re.search(r'' + X2_Prefix + '', ip):
                rc2 = True
                break
            else:
                logger.info('Try to click renew button.')
                interface_ipv4.click_dhcp_renew('X2:V' + str(PC1_vlan_eth2), version='v6')
        if rc2:
            logger.info("X2  obtain ipv6 addr successfully.\n")
        else:
            logger.error("Error: X2 should obtain ipv6 contain prefix " + X2_Prefix + "\n")

        time.sleep(6)
        logger.info("del sub inteface.............\n")
        rc3 = interface_ipv4.del_interface(**x2_vlan)
        if rc3:
            logger.info("del sub inteface successfully.\n")
        else:
            logger.error("Error: del sub inteface failed")

        dibbler = Host(self.dibbler_server)
        rc4 = dibbler.stop_DHCP_server()
        if rc4:
            logger.info("stop dibbler successfully.\n")
        else:
            logger.error("Error: stop dibbler failed")

        Assertion.assert_equal(rc & rc1 & rc2 & rc3 & rc4, True, "ERR: Start dhcp server failed.")
