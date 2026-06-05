from definition.settings import *
from definition.utils import *


# make sure transparent info not show in lan/dmz/custom zone for interface x2.
class TestConfigure_TC02(Test):
    uuid = "SOSAIOT-TC-57245"
    description = show_testcase_info(TESTPLAN, 'Configure_TC02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_transparent_not_in_x2_lan(self):
        output = interfaceapi.get_interface_status(name='X2')
        Assertion.assert_not_regular(json.dumps(output), 'transparent', "ERR: check trans not in X2 failed")

    def test_02_check_transparent_not_in_x2_dmz(self):
        x2_dmz_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
        }
        output1 = interfaceapi.config_interface(**x2_dmz_dict)
        res = interfaceapi.get_interface_status(name='X2')
        output2 = True if 'transparent' not in json.dumps(res) else False
        logger.info(f'change dmz zone: {output1}, check transparent: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: check trans not in X2 failed")

    def test_03_check_transparent_not_in_x2_custom(self):
        x2_dmz_dict = {
            'if': 'X2',
            'zone': 'auto_test1',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
        }
        output1 = interfaceapi.config_interface(**x2_dmz_dict)
        res = interfaceapi.get_interface_status(name='X2')
        output2 = True if 'transparent' not in json.dumps(res) else False
        logger.info(f'change custom zone: {output1}, check transparent: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: check trans not in X2 failed")

    def test_04_init_Config_X2(self):
        rc = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")


# check error msg while changed transparent range in x2.
class TestConfigure_TC03(Test):
    uuid = "SOSAIOT-TC-57247"
    description = show_testcase_info(TESTPLAN, 'Configure_TC03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_different_range_out_for_X2_failed(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.out_wan_range
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent Range not in Primary WAN subnet'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check different range out of x2 failed")

    def test_02_change_range_include_wan_ip_for_X2_failed(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.include_x1_ip_range
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent Range includes WAN IP'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check include wan ip range failed")

    def test_03_change_range_include_wan_gw_for_X2_failed(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.include_x1_gw_range
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent Range includes WAN Gateway'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check include wan range gw failed")

    def test_04_change_range_include_wan_for_X2(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: check include wan range failed")

    def test_05_change_X2_to_static_lan(self):
        output = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")


# check error msg while config transparent range to dmz host in x2.
class TestConfigure_TC05(Test):
    uuid = "SOSAIOT-TC-57253"
    description = show_testcase_info(TESTPLAN, 'Configure_TC05', description=True)['title']
    dmz_ao_name = '33.33.33.33'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dmz_ao(self):
        ao_dict = {
            "object_type": "host",
            "name": self.dmz_ao_name,
            "zone": "DMZ",
            "value": self.dmz_ao_name
        }
        (res, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if res is False:
            res = True if 'Already exists' in str(aomsg) else False
        Assertion.assert_equal(res, True, "ERR: add dmz ao failed")

    def test_02_config_host_not_in_wan_sub_in_X2_failed(self):
        x2_transparent_dict['transparent_range']['name'] = self.dmz_ao_name
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent Range not in Primary WAN subnet'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check config host not in wan sub in x2 failed")


# check error msg while config transparent range to dmz range in x2.
class TestConfigure_TC06(Test):
    uuid = "SOSAIOT-TC-57255"
    description = show_testcase_info(TESTPLAN, 'Configure_TC06', description=True)['title']
    dmz_ao_name = '33.33.33.10-30'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dmz_ao(self):
        ao_dict = {
            "object_type": "range",
            "name": self.dmz_ao_name,
            "zone": "LAN",
            "value": '33.33.33.10,33.33.33.30'
        }
        (res, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if res is False:
            res = True if 'Already exists' in str(aomsg) else False
        Assertion.assert_equal(res, True, "ERR: add dmz ao failed")

    def test_02_config_range_not_in_wan_sub_in_X2_failed(self):
        x2_transparent_dict['transparent_range']['name'] = self.dmz_ao_name
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent Range not in Primary WAN subnet'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check config range not in wan sub in x2 failed")


# check error msg while Transparent Range overlaps between X2 and X3.
class TestConfigure_TC08(Test):
    uuid = "SOSAIOT-TC-57258"
    description = show_testcase_info(TESTPLAN, 'Configure_TC08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_in_wan_range1_for_X2(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: check include wan range failed")

    def test_02_config_in_wan_range2_for_X3_failed(self):
        x3_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range2
        (res, msg) = interfaceapi.config_interface(msg=True, **x3_transparent_dict)
        error_msg = 'Transparent Range overlaps with other configured Transparent Interface'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check config overlap failed")


# check error msg while del ao that exist in transparent range.
class TestConfigure_TC09(Test):
    uuid = "SOSAIOT-TC-57259"
    description = show_testcase_info(TESTPLAN, 'Configure_TC09', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC09')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_to_transparent_mode(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to transparent mode failed")

    def test_02_check_delete_ao_in_transparent_range(self):
        ao_del = {
            'ip_type': 'ipv4',
            'name': CaseParams.in_wan_range1,
        }
        output = aoapi.del_addressobject(**ao_del)
        Assertion.assert_equal(output, False, "ERR: delete ao in transparent range failed")


# check error msg while changed mode between x1 and x2.
class TestConfigure_TC10(Test):
    uuid = "SOSAIOT-TC-57236"
    description = show_testcase_info(TESTPLAN, 'Configure_TC10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_X2_to_static_wan(self):
        res = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(res, True, "ERR: configure x2 transparent mode failed")

    def test_03_change_X1_to_dhcp_wan_failed(self):
        logger.info('wait 10s to valid the x1 configure...')
        time.sleep(10)
        (res, msg) = interfaceapi.config_interface(msg=True, **x1_dhcp_dict)
        error_msg = 'Transparent shared link must have static IP assignment'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check config x1 to dhcp wan failed")

    def test_04_change_X2_to_static_lan(self):
        res = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    def test_05_change_X1_to_dhcp_wan(self):
        res = interfaceapi.config_interface(**x1_dhcp_dict)
        Assertion.assert_equal(res, True, "ERR: change x1 to dhcp failed")

    def test_06_change_X2_to_transparent_mode_failed(self):
        logger.info('wait 10s to valid the x1 configure...')
        time.sleep(10)
        (res, msg) = interfaceapi.config_interface(msg=True, **x2_transparent_dict)
        error_msg = 'Transparent shared interface must be static WAN type'
        Assertion.assert_regular(json.dumps(msg), error_msg, "ERR: check config x1 to dhcp wan failed")

    def test_07_change_x1_to_default_mode(self):
        res = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")


# check boundary the Host IP in low/middle/higher range in transparent mode.
class TestConfigure_TC11(Test):
    uuid = "SOSAIOT-TC-57237"
    description = show_testcase_info(TESTPLAN, 'Configure_TC11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Configure_TC11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_to_transparent_mode(self):
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to transparent mode failed")

    def test_02_check_icmp_lower_boundary_range_must_blocked(self):
        res = PC2_login.send_command('ifconfig eth1 12.12.1.9')
        logger.info(res)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, False, "ERR: check icmp failed")

    def test_03_check_icmp_in_lower_boundary_ip_must_passed(self):
        res = PC2_login.send_command('ifconfig eth1 12.12.1.10')
        logger.info(res)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_04_check_icmp_in_boundary_range_must_passed(self):
        res = PC2_login.send_command('ifconfig eth1 12.12.1.65')
        logger.info(res)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_05_check_icmp_higner_boundary_range_must_blocked(self):
        res = PC2_login.send_command('ifconfig eth1 12.12.1.110')
        logger.info(res)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, False, "ERR: check icmp failed")


# check ping passed in The interface X2 within DMZ or Custom zone.
class TestZones_TC13(Test):
    uuid = "SOSAIOT-TC-57239"
    description = show_testcase_info(TESTPLAN, 'Zones_TC13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Zones_TC13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_to_DMZ_zone(self):
        x2_transparent_dict['zone'] = 'DMZ'
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to dmz zone failed")

    def test_02_check_icmp_in_boundary_range_must_passed(self):
        res = PC2_login.send_command('ifconfig eth1 12.12.1.90')
        logger.info(res)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_03_change_X2_to_custom_zone(self):
        x2_transparent_dict['zone'] = CaseParams.custom_zone
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to custom zone failed")

    def test_04_check_icmp_in_boundary_range_must_passed(self):
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")


# check ping https login in x2 interface.
class TestInterface_TC16(Test):
    uuid = "SOSAIOT-TC-57241"
    description = show_testcase_info(TESTPLAN, 'Interface_TC16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Interface_TC16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_to_LAN_zone(self):
        x2_transparent_dict['zone'] = 'LAN'
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range1
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to lan zone failed")

    def test_02_check_ping_to_X2_interface(self):
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_03_check_https_login_via_PC2(self):
        # need add default to PC2 to access conf path
        # PC2_login.send_command(f'route add default gw {Parameter.X1_GW}')
        cmd = [f'python3 {CONF_PATH}/ui_login_fw.py '
               f'-url https://{Parameter.X1_IP} '
               f'-user admin -pwd sonicauto']
        # clean firefox process
        PC2_login.send_command('pkill firefox')
        # check ldap server status
        output = PC2_login.send_commands(cmd)
        res = True if 'login fw result is True' in output else False
        Assertion.assert_equal(res, True, "ERR: login wan host via ui failed")


# check new ip exist in arp entries between lan/wan zones.
class TestARP_TC17(Test):
    uuid = "SOSAIOT-TC-57242"
    description = show_testcase_info(TESTPLAN, 'ARP_TC17', description=True)['title']
    pc2_eth1_ip = '12.12.1.25'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ARP_TC17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_ip_and_check_icmp_in_x2(self):
        res = PC2_login.send_command(f'ifconfig eth1 {self.pc2_eth1_ip}')
        logger.info(res)
        time.sleep(5)
        output = PC2_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_02_check_new_ip_in_arp_entries(self):
        output = arpapi.show_arp_caches()
        Assertion.assert_regular(json.dumps(output), self.pc2_eth1_ip, "ERR: check new ip in arp failed")


# check new ip exist in arp entries between lan/lan zones.
class TestARP_TC18(Test):
    uuid = "SOSAIOT-TC-57243"
    description = show_testcase_info(TESTPLAN, 'ARP_TC18', description=True)['title']
    pc2_eth1_ip = '12.12.1.25'
    pc3_eth1_ip = '12.12.1.192'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ARP_TC18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X3_to_LAN_zone(self):
        x3_transparent_dict['zone'] = 'LAN'
        x3_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range3
        output = interfaceapi.config_interface(**x3_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x3 to lan zone failed")

    def test_02_change_ip_and_check_icmp_in_x3(self):
        res = PC3_login.send_command(f'ifconfig eth1 {self.pc3_eth1_ip}')
        logger.info(res)
        time.sleep(5)
        output = PC3_login.ping_from_eth(ip=self.pc2_eth1_ip, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_03_check_new_ip_in_arp_entries(self):
        output = arpapi.show_arp_caches()
        Assertion.assert_regular(json.dumps(output), self.pc3_eth1_ip, "ERR: check new ip in arp failed")


# check new ip exist in arp entries between lan/dmz zones.
class TestARP_TC19(Test):
    uuid = "SOSAIOT-TC-57244"
    description = show_testcase_info(TESTPLAN, 'ARP_TC19', description=True)['title']
    pc3_eth1_ip = '12.12.1.193'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ARP_TC19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X3_to_LAN_zone(self):
        x3_transparent_dict['zone'] = 'DMZ'
        x3_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range3
        output = interfaceapi.config_interface(**x3_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x3 to lan zone failed")

    def test_02_change_ip_and_check_icmp_in_x2(self):
        res = PC3_login.send_command(f'ifconfig eth1 {self.pc3_eth1_ip}')
        logger.info(res)
        time.sleep(5)
        output = PC2_login.ping_from_eth(ip=self.pc3_eth1_ip, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_03_check_new_ip_in_arp_entries(self):
        output = arpapi.show_arp_caches()
        Assertion.assert_regular(json.dumps(output), self.pc3_eth1_ip, "ERR: check new ip in arp failed")


# check ping in x2 and x1 between lan/wan zones.
class TestPolicy_TC22(Test):
    uuid = "SOSAIOT-TC-57246"
    description = show_testcase_info(TESTPLAN, 'Policy_TC22', description=True)['title']
    wan_to_lan_acl_name = 'auto_wan_to_lan'
    pc2_eth1_ip = '12.12.1.95'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Policy_TC22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_to_LAN_zone(self):
        x2_transparent_dict['zone'] = 'LAN'
        x2_transparent_dict['transparent_range']['name'] = CaseParams.in_wan_range2
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to lan zone failed")

    def test_02_configure_wan_to_lan_acl(self):
        access_rule_dict = {
            'name': self.wan_to_lan_acl_name,
            'from': 'WAN',
            'to': 'LAN',
            'source_addr': {'any': True},
            'dst_addr': {'any': True},
            'service': {'group': 'Ping'},
            'action': 'allow',
        }
        (aclres, aclmsg) = accessruleapi.add_ipv4_access_rule(msg=True, **access_rule_dict)
        if not aclres:
            aclres = True if 'Already exists' in json.dumps(aclmsg) else False
        Assertion.assert_equal(aclres, True, "ERR: Config wan to lan acl failed")

    def test_03_ping_from_lan_to_wan(self):
        res = PC2_login.send_command(f'ifconfig eth1 {self.pc2_eth1_ip}')
        logger.info(res)
        time.sleep(5)
        output = PC2_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_04_ping_from_wan_to_lan(self):
        output = PC4_login.ping_from_eth(ip=self.pc2_eth1_ip, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")


# check ping in x2 and x1 between group host and range.
class TestGroup_Func_TC01(Test):
    uuid = "SOSAIOT-TC-57260"
    description = show_testcase_info(TESTPLAN, 'Group_Func_TC01', description=True)['title']
    ao_host_name = '12.12.1.75'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Group_Func_TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ao_group(self):
        ao_dict = {
            "object_type": "host",
            "name": self.ao_host_name,
            "zone": "WAN",
            "value": self.ao_host_name
        }
        aogroup_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.ao_host_name},
                                {"name": CaseParams.in_wan_range2}
                            ]
                        },
                        "name": CaseParams.ao_group_name
                    }
                }
            ]
        }
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg1) else False
        (aogres, aogmsg) = aogroupapi.add_addressgroup(msg=True, **aogroup_dict)
        if aogres is False:
            aogres = True if 'Already exists' in str(aogmsg) else False
        Assertion.assert_equal(aores & aogres, True, 'ERR: add ao and group failed')

    def test_02_change_X2_to_LAN_zone(self):
        x2_transparent_dict['transparent_range']['group'] = CaseParams.ao_group_name
        output = interfaceapi.config_interface(**x2_transparent_dict)
        Assertion.assert_equal(output, True, "ERR: change x2 to lan zone failed")

    def test_03_ping_from_lan_to_wan_in_host(self):
        res = PC2_login.send_command(f'ifconfig eth1 {self.ao_host_name}')
        logger.info(res)
        time.sleep(5)
        output = PC2_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")

    def test_04_ping_from_lan_to_wan_in_range(self):
        res = PC2_login.send_command(f'ifconfig eth1 12.12.1.98')
        logger.info(res)
        time.sleep(5)
        output = PC2_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")


# check ping in x2 and x1 between group host and range.
class TestDHCP_TC33(Test):
    uuid = "SOSAIOT-TC-57248"
    description = show_testcase_info(TESTPLAN, 'DHCP_TC33', description=True)['title']
    server_start_ip = '12.12.1.91'
    server_end_ip = '12.12.1.93'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DHCP_TC33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_entry_to_X2(self):
        dynamic_entry = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": self.server_start_ip,
                                "to": self.server_end_ip,
                                "enable": True,
                                "lease_time": 1,
                                "default_gateway": Parameter.X1_GW,
                                "netmask": Parameter.MASK,
                                "dns": {"server": {"inherit": True}}
                            }
                        ]}}}}
        (res, msg) = dhcpserverapi.add_dhcp_server_scope_dynamic(msg=True, **dynamic_entry)
        if not res:
            res = True if 'Already exists' in json.dumps(msg) else False
        Assertion.assert_equal(res, True, "ERR: Add dynamic entries failed")

    def test_02_get_dhcp_ip_from_pc2(self):
        DHCLIEN_LEASE_FILE = '/var/lib/dhclient/dhclient.leases'
        PC2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        releaseres = release_ip_in_pc(PC2_login, 'eth1')
        leaseres = get_ip_lease_in_pc(PC2_login, 'eth1')
        logger.info(f'release result: {releaseres}, get ip result: {leaseres}')
        Assertion.assert_equal(leaseres, True, "ERR: get dhcp ip from pc2 failed")

    def test_03_ping_from_lan_to_wan_in_host(self):
        output = PC2_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp failed")


# check cfs info in tsr.
class TestTSR_TC35(Test):
    uuid = "SOSAIOT-TC-57250"
    description = show_testcase_info(TESTPLAN, 'TSR_TC35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TSR_TC35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_transparent_info_in_x2(self):
        x2_info_list = ['Zone  : LAN', 'Transparent Ranges',
                        '2.12.1.90 - 12.12.1.120',
                        '12.12.1.75 - 12.12.1.75',
                        'TRANSPARENT']
        getcontents = tsrfromlanapi.get_tsr_interface_part(lab1='X2', lab2='X3')
        logger.info(f'get x2 info in tsr: \n{getcontents}')
        checkres = [x in getcontents for x in x2_info_list]
        logger.info(f'check transparent info result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check cfs policy settings failed")

    def test_02_check_transparent_info_in_x3(self):
        x3_info_list = ['Zone  : DMZ', 'Transparent Ranges',
                        '12.12.1.171 - 12.12.1.200',
                        'TRANSPARENT']
        getcontents = tsrfromlanapi.get_tsr_interface_part(lab1='X3', lab2='X4')
        logger.info(f'get x3 info in tsr: \n{getcontents}')
        checkres = [x in getcontents for x in x3_info_list]
        logger.info(f'check transparent info result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check cfs policy settings failed")


# check transparent info in Prefs.
class TestPerf_TC38(Test):
    uuid = "SOSAIOT-TC-57251"
    description = show_testcase_info(TESTPLAN, 'Perf_TC38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Perf_TC38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_prefs(self):
        output = settingapi.export_setting_exp()
        Assertion.assert_equal(output, True, "ERR: export settings from fw failed")

    def test_02_change_interface_x2_x3(self):
        output1 = interfaceapi.config_interface(**x2_lan_dict)
        output2 = interfaceapi.config_interface(**x3_lan_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: change x2 x3 failed")

    def test_03_import_prefs(self):
        output = settingapi.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(output, True, "ERR: import settings from fw failed")

    def test_04_check_interface_x2_x3(self):
        output1 = interfaceapi.get_interface_status('X2')
        res1 = True if CaseParams.ao_group_name in json.dumps(output1) else False
        output2 = interfaceapi.get_interface_status('X3')
        res2 = True if CaseParams.in_wan_range3 in json.dumps(output2) else False
        logger.info(f'check x2 result: {res1}, check x3 result: {res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: check interface X2 and X3 failed")

