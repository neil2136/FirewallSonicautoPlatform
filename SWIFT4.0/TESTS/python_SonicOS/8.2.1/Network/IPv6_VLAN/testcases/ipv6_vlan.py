from settings import *


class Test_00_Config_Switch(Test):
    uuid = 'NonTC'

    def test_00_change_untag_to_tag(self):
        osstack = Openstack(Params.testbed)
        rc = osstack.set_node_interface_state('UTM','X1', 'tag')
        Assertion.assert_equal(rc, True, "ERR: change X1 to tag.")


class Test_13_Static_IPv6_Assignment(Test):
    uuid = "SOSAIOT-TC-56690"
    description= show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']
    pc1 = Host('localhost')

    def test_13_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_13_01_config_PC1_IP(self):
        self.pc1.config_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_regular(rc, f"{Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]}", "ERR: Config pc1 ipv6 failed.")

    def test_13_02_add_PC1_route(self):
        self.pc1.config_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X2'])
        rc = self.pc1.send_command(f'route -A inet6')
        Assertion.assert_regular(rc, f"\*/0.*{Parameter.DUT_IP['ipv6']['X2']}", "ERR: Config pc1 route failed.")

    @repeat_method(5, sleep=10)
    def test_13_03_add_subinterface(self):
        rc = True
        ping_result = True
        for zone in zones:
            logger.info(f'Add sub interface with zone {zone}')
            vlan = Parameter.PC1['vlan'][Parameter.DUT_X2_INTER]
            x2_vlan = {
                'if': 'x2',
                'type': 'vlan',
                'vlan_tag': vlan,
                'zone': zone,
                'mode': 'static',
                'ip': '11.2.3.4',
                'gateway': '11.1.1.1',
            }
            rc &= interface.add_interface(**x2_vlan)
            x2_vlan_v6 ={
                'name': 'X2',
                'vlan': vlan,
                'mode': 'static',
                'zone': zone,
                'ip': Parameter.DUT_IP['ipv6']['X2'],
                'mgmt_ping': True,
            }
            rc &= interface_v6.config_interface_ipv6(**x2_vlan_v6)
            time.sleep(2)
            out = self.pc1.send_command(f"ping6 {Parameter.DUT_IP['ipv6']['X2']} -c 10")
            ping_result &= '100 packet loss' not in out
            rc &= interface.del_interface(**x2_vlan)
        Assertion.assert_equal(rc, True, f"ERR:Add sub interface to {zone} zone fail.")
        Assertion.assert_equal(ping_result, True, f"ERR:Add sub interface to {zone} zone and ping fail.")

    def test_13_05_del_PC1_route(self):
        self.pc1.delete_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X2'])
        rc = self.pc1.send_command(f'route -A inet6')
        Assertion.assert_not_regular(rc, f"\*/0.*{Parameter.DUT_IP['ipv6']['X2']}", "ERR: Config pc1 route failed.")

    def test_13_06_del_PC1_IP(self):
        self.pc1.delete_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_not_regular(rc, f"{Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]}", "ERR: Config pc1 ipv6 failed.")


class Test_14_Dynamic_IPv6_Assignment(Test):
    uuid = "SOSAIOT-TC-56691"
    description= show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']
    dibbler_server = Params.testbed + '-PC3'
    x1_vlan = {
        'if': 'x1',
        'type': 'vlan',
        'vlan_tag': Parameter.PC3['vlan'][Parameter.DUT_X1_INTER],
        'zone': 'WAN',
        'mode': 'static',
        'ip': '2.2.2.10',
        'gateway': '2.2.2.20',
    }
    def test_14_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(5)
    def test_14_01_start_dibbler(self):
        # dibbler_server = Params.testbed + '-PC3'
        log_file = '/tmp/dibbler.log'
        dibbler = Host(self.dibbler_server) 
        logger.info(f'Mkdir /var/lib/dibbler,/etc/dibbler on {self.dibbler_server}')
        dibbler.send_command('mkdir -p /var/lib/dibbler')
        dibbler.send_command('mkdir -p /etc/dibbler')
        dibbler.send_command('mv /etc/dibbler/server.conf /etc/dibbler/server.conf.bak')
        dibbler.send_command(f'cp {Parameter.DIBBLER_SERVER_CONF} /etc/dibbler/')
        rc = dibbler.start_DHCP_server()
        Assertion.assert_equal(rc, True, "ERR: Start dhcp server failed.")
   
    def test_14_02_add_sub_interface(self):
        rc = interface.add_interface(**self.x1_vlan)
        x1_vlan_v6 ={
            'name': 'X1',
            'vlan': Parameter.PC3['vlan'][Parameter.DUT_X1_INTER],
            'mode': 'dhcpv6',
            'zone': 'WAN',
            'ip': Parameter.DUT_IP['ipv6']['X1'],
            'mgmg_ping': True,
            'dhcpv6': {
                'mode': 'manual',
            },
            'listen_router_advertisement':True,           
        }
        rc &= interface_v6.config_interface_ipv6(**x1_vlan_v6)
        Assertion.assert_equal(rc, True, "ERR: Add sub interface failed.")

    def test_14_03_config_PC3_IP(self):
        dibbler = Host(self.dibbler_server) 
        dibbler.config_IPv6_ip(ip=Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER], prefix=64, interface=Parameter.DUT_X1_INTER)

    @repeat_method(5)
    def test_14_05_verify_DUT_got_dhcpv6_addr(self):
        time.sleep(10)
        x1_dict = interface_v6.get_interface_address(name='X1/vlan/' + str(Parameter.PC3['vlan'][Parameter.DUT_X1_INTER]))
        try:
            ip = x1_dict['ip_address']
        except:
            logger.error('Fail to get X1 ipv6.')
            logger.info(x1_dict)
            ip = ''
        if not re.search(r'' + Parameter.DUT_IP['prefix']['X1'] + '', ip):
            logger.info('Try to click renew button.')
            interface.click_dhcp_renew('X1:V'+ str(Parameter.PC3['vlan'][Parameter.DUT_X1_INTER]), version='v6')
        Assertion.assert_regular(ip, Parameter.DUT_IP['prefix']['X1'], f"Error: X1 should obtain ipv6 contain prefix {Parameter.DUT_IP['prefix']['X1']}")

    def test_14_06_delete_PC3_IP(self):
        dibbler = Host(self.dibbler_server) 
        dibbler.delete_IPv6_ip(ip=Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER], prefix=64, interface=Parameter.DUT_X1_INTER)

    def test_14_07_delete_sub_interface(self):
        rc = interface.del_interface(**self.x1_vlan)
        Assertion.assert_equal(True, True, f'Err: Delete sub interface failed.')

    def test_14_08_stop_dibbler(self):
        dibbler = Host(self.dibbler_server) 
        rc = dibbler.stop_DHCP_server()
        Assertion.assert_equal(rc, True, "ERR: Start dhcp server failed.")

class Test_17_management_https(Test):
    uuid = "SOSAIOT-TC-56694"
    description= show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']
    pc1 = Host('localhost')
    x2_vlan = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': Parameter.PC1['vlan'][Parameter.DUT_X2_INTER],
            'zone': 'WAN',
            'mode': 'static',
            'ip': '3.3.3.10',
            'gateway': '3.3.3.20',
        }

    def test_17_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_17_01_add_sub_interface(self):
        rc = interface.add_interface(**self.x2_vlan)
        x2_vlan_v6 ={
            'name': 'X2',
            'vlan': Parameter.PC1['vlan'][Parameter.DUT_X2_INTER],
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.DUT_IP['ipv6']['X2'],
            'mgmt_https': True,
        }
        rc &= interface_v6.config_interface_ipv6(**x2_vlan_v6)
        Assertion.assert_equal(rc, True, "ERR: Add sub interface failed.")

    def test_17_02_config_PC1_IP(self):
        self.pc1.config_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_regular(rc, f"{Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]}", "ERR: Config pc1 ipv6 failed.")

    def test_17_03_manage_DUT(self):
        fw_ipv6 = Firewall(f"[{Parameter.DUT_IP['ipv6']['X2']}]", user='admin', password='password', supported_config_mode='api')
        rc = fw_ipv6.api_login()
        rc &= fw_ipv6.api_logout()
        Assertion.assert_equal(rc, True, f"ERR: Login https://[{Parameter.DUT_IP['ipv6']['X2']}] fail.")

    def test_17_04_delete_PC1_IP(self):
        self.pc1.delete_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_not_regular(rc, "Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]", "ERR: Config pc1 ipv6 failed.")

    def test_17_05_delete_sub_interface(self):
        rc = interface.del_interface(**self.x2_vlan)
        Assertion.assert_equal(rc, True, f'Err: Delete sub interface failed.')


class Test_24_passing_traffic(Test):
    uuid = "SOSAIOT-TC-56698"
    description= show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']
    pc1 = Host('localhost')
    pc3 = Host(Params.testbed + '-PC3')
    x2_vlan = {
        'if': 'x2',
        'type': 'vlan',
        'vlan_tag': Parameter.PC1['vlan'][Parameter.DUT_X2_INTER],
        'zone': 'WAN',
        'mode': 'static',
        'ip': '3.3.3.10',
        'gateway': '3.3.3.20',
    }
    x1_vlan = {
        'if': 'x1',
        'type': 'vlan',
        'vlan_tag': Parameter.PC3['vlan'][Parameter.DUT_X1_INTER],
        'zone': 'LAN',
        'mode': 'static',
        'ip': '2.2.2.10',
        'gateway': '2.2.2.20',
    }

    def test_24_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_24_001_add_sub_interface(self):
        rc = interface.add_interface(**self.x2_vlan)
        x2_vlan_v6 ={
            'name': 'X2',
            'vlan': Parameter.PC1['vlan'][Parameter.DUT_X2_INTER],
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.DUT_IP['ipv6']['X2'],
            'mgmg_https': True,
        }
        rc &= interface_v6.config_interface_ipv6(**x2_vlan_v6)
        Assertion.assert_equal(rc, True, "ERR: Add sub interface failed.")
  
    def test_24_002_add_X1_sub_interface(self):
        rc = interface.add_interface(**self.x1_vlan)
        x1_vlan_v6 ={
            'name': 'X1',
            'vlan': Parameter.PC3['vlan'][Parameter.DUT_X1_INTER],
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_IP['ipv6']['X1'],
        }
        rc &= interface_v6.config_interface_ipv6(**x1_vlan_v6)
        Assertion.assert_equal(rc, True, "ERR: Add sub interface failed.")
  
    def test_24_003_config_PC1_IP(self):
        self.pc1.config_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_regular(rc, f"{Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]}", "ERR: Config pc1 ipv6 failed.")

    def test_24_004_add_PC1_route(self):
        self.pc1.config_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X2'])
        rc = self.pc1.send_command(f'route -A inet6')
        Assertion.assert_regular(str(rc), f"{Parameter.DUT_IP['ipv6']['X2']}", "ERR: Config pc1 route failed.")
     
    def test_24_005_config_PC3_IP(self):
        self.pc3.config_IPv6_ip(ip=Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER], prefix=64, interface=Parameter.DUT_X1_INTER)
        rc = self.pc3.send_command(f'ifconfig {Parameter.DUT_X1_INTER}')
        Assertion.assert_regular(str(rc), f"{Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER]}", "ERR: Config pc3 ipv6 failed.")

    def test_24_006_add_PC3_route(self):
        self.pc3.config_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X1'])
        rc = self.pc3.send_command(f'route -A inet6')
        Assertion.assert_regular(str(rc), f"{Parameter.DUT_IP['ipv6']['X1']}", "ERR: Config pc1 route failed.")

    def test_24_007_check_route_policy(self):
        policies = route_obj.get_auto_route_policy(version='v6')
        logger.info(policies)
        foundit = 0
        for policy in policies:
            logger.info(Parameter.DUT_IP['prefix']['X1'] + '/64')
            logger.info(Parameter.PC3['vlan'][Parameter.DUT_X1_INTER])
            logger.info(Parameter.PC1['vlan'][Parameter.DUT_X2_INTER])
            if policy['source'] == 'Any' and policy['destination'] == Parameter.DUT_IP['prefix']['X1'] + '/64' and policy['interface'] == 'X1:V' + str(Parameter.PC3['vlan'][Parameter.DUT_X1_INTER]):
                logger.info(f"Find policy from any to {Parameter.DUT_IP['prefix']['X1']}")
                foundit += 1
            elif policy['source'] == 'Any' and policy['destination'] == Parameter.DUT_IP['prefix']['X2'] + '/64' and policy['interface'] == 'X2:V' + str(Parameter.PC1['vlan'][Parameter.DUT_X2_INTER]):
                logger.info(f"Find policy from any to {Parameter.DUT_IP['prefix']['X2']}")
                foundit += 1
            if foundit ==2:
                break
        Assertion.assert_equal(foundit, 2, f"Err: Not find policy from any to {Parameter.DUT_IP['prefix']['X1']} and {Parameter.DUT_IP['prefix']['X2']}")

    def test_24_008_ping_from_pc1_to_pc3(self):
        rc1 = self.pc3.send_command(f"ping6 {Parameter.PC1['ipv6'][Parameter.DUT_X1_INTER]} -c 5")    
        rc2 = ping6(Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER])
        Assertion.assert_not_equal(rc1, '100% packet loss', f'Err: ping from pc3 to pc1 failed.')
        Assertion.assert_not_equal(rc2, '100% packet loss', f'Err: ping from pc1 to pc3 failed.')

    def test_24_009_delete_sub_interface(self):
        rc = interface.del_interface(**self.x1_vlan)
        rc &= interface.del_interface(**self.x2_vlan)
        Assertion.assert_equal(True, True, f'Err: Delete sub interface failed.')

    def test_24_010_del_PC1_route(self):
        self.pc1.delete_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X2'])
        rc = self.pc1.send_command(f'route -A inet6')
        Assertion.assert_not_regular(str(rc), f"{Parameter.DUT_IP['ipv6']['X2']}", "ERR: Config pc1 route failed.")
    
    def test_24_011_delete_PC1_IP(self):
        self.pc1.delete_IPv6_ip(ip=Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER], prefix=64, interface=Parameter.DUT_X2_INTER)
        rc = self.pc1.send_command(f'ifconfig {Parameter.DUT_X2_INTER}')
        Assertion.assert_not_regular(rc, f"{Parameter.PC1['ipv6'][Parameter.DUT_X2_INTER]}", "ERR: Config pc1 ipv6 failed.")

    def test_24_012_add_PC3_route(self):
        self.pc3.delete_IPv6_route(route='::',prefix='0', gw=Parameter.DUT_IP['ipv6']['X1'])
        rc = self.pc1.send_command(f'route -A inet6')
        Assertion.assert_not_regular(str(rc), f"{Parameter.DUT_IP['ipv6']['X1']}", "ERR: Config pc1 route failed.")

    def test_24_013_config_PC3_IP(self):
        self.pc3.delete_IPv6_ip(ip=Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER], prefix=64, interface=Parameter.DUT_X1_INTER)
        rc = self.pc3.send_command(f'ifconfig {Parameter.DUT_X1_INTER}')
        Assertion.assert_not_regular(str(rc), f"{Parameter.PC3['ipv6'][Parameter.DUT_X1_INTER]}", "ERR: Config pc3 ipv6 failed.")


class Test_100_Config_Switch(Test):
    uuid = 'NonTC'

    def test_100_change_tag_to_untag(self):
        osstack = Openstack(Params.testbed)
        rc = osstack.set_node_interface_state('UTM','X1', 'untag')
        Assertion.assert_equal(rc, True, "ERR: change X1 to untag.")