from definition.settings import *
from definition.utils import *


# Expected: all zone can be saved in X2
class Test31bit_TC01(Test):
    uuid = "SOSAIOT-TC-56155"
    description = show_testcase_info(
        Parameter.TESTPLAN, '01', description=True)['title']
    czname = 'tc01zone1'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_x2_with_lan_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '22.22.22.22',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to lan failed")

    def test_02_edit_x2_with_dmz_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'dmz',
            'mode': 'static',
            'ip': '33.33.33.33',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to dmz failed")

    def test_03_edit_x2_with_wan_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '44.44.44.44',
            'netmask': Parameter.MASK,
            'gateway': '44.44.44.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to wan failed")

    def test_04_edit_x2_with_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': '55.55.55.55',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            output &= interfacev4api.config_interface(**x2_dict)
        else:
            logger.error(f'add custom zone: {self.czname} failed')

        # init x2 configure and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(self.czname)

        Assertion.assert_equal(output, True, "ERR: edit interface x2 to custom zone failed")


# Expected: every zone can be saved in X2
class Test31bit_TC02(Test):
    uuid = "SOSAIOT-TC-56154"
    description = show_testcase_info(
        Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_x2_with_lan_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '100.100.100.100',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to lan failed")

    def test_02_change_x2_to_dmz_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'dmz',
            'mode': 'static',
            'ip': '100.100.100.100',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            res = interfacev4api.get_interface_status('X2')
            try:
                if res['interfaces'][0]['ipv4']['ip_assignment']['zone'] == x2_dict['zone']:
                    output &= True
            except Exception as e:
                logger.error(repr(e))

        Assertion.assert_equal(output, True, "ERR: edit interface x2 to lan failed")

    def test_03_change_x2_ip(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '110.110.110.110',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            res = interfacev4api.get_interface_status('X2')
            try:
                if res['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip'] == x2_dict['ip']:
                    output &= True
            except Exception as e:
                logger.error(repr(e))

        Assertion.assert_equal(output, True, "ERR: modify interface x2 ip failed")

    def test_04_change_x2_mask(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '100.100.100.100',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            res = interfacev4api.get_interface_status('X2')
            try:
                if res['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['netmask'] == x2_dict['netmask']:
                    output &= True
            except Exception as e:
                logger.error(repr(e))
            res2 = aoapi.get_addressobject_by_name(name='X2 Subnet', version='ipv4')
            try:
                if res2['address_objects'][0]['ipv4']['network']['mask'] == x2_dict['netmask']:
                    output &= True
            except Exception as e:
                logger.error(repr(e))
        Assertion.assert_equal(output, True, "ERR: modify interface x2 ip failed")


# Expected: unassign x2 and vlan x2 successful.
class Test31bit_TC03(Test):
    uuid = "SOSAIOT-TC-56156"
    description = show_testcase_info(
        Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_x2_with_lan_zone(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '120.120.120.120',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            output &= interfacev4api.unassign_interface(interface='X2')
        else:
            logger.error('config interface X2 to lan fail')
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to lan failed")

    def test_02_add_wan_vlan_to_x2_(self):
        x2_wan_dict = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': 777,
            'zone': 'wan',
            'mode': 'static',
            'ip': '130.130.130.130',
            'netmask': Parameter.MASK,
            'gateway': '130.130.130.1',
            'dns1': '4.4.4.4',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        x2_del_dict = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': '777',
        }
        output = interfacev4api.add_interface(**x2_wan_dict)
        if output:
            output &= interfacev4api.del_interface(**x2_del_dict)
        else:
            logger.error('add vlan wan zone to interface X2 fail')
        Assertion.assert_equal(output, True, "ERR: edit interface x2 to lan failed")


# Expected: check traffic between x2 on pc2 successful.
class Test31bit_TC04(Test):
    uuid = "SOSAIOT-TC-56157"
    description = show_testcase_info(
        Parameter.TESTPLAN, '04', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_ping_passed_between_x2_pc2(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '12.12.1.101',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        PC2_login.send_command(f'ifconfig eth1 12.12.1.100')
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            output &= PC2_login.ping_from_eth(ip=x2_dict['ip'], eth='eth1')
        else:
            logger.error('config X2 to 31 bit interface failed')
        Assertion.assert_equal(output, True, "ERR: config interface x2 to lan failed")

    def test_01_ping_failed_between_x2_pc2(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': '12.12.1.99',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            pingres = PC2_login.ping_from_eth(ip=x2_dict['ip'], eth='eth1')
            output &= True if not pingres else False
        else:
            logger.error('config X2 to 31 bit interface failed')
        Assertion.assert_equal(output, True, "ERR: check traffic between x2 on pc2 failed")


# Expected: Management (https/snmp/ssh) on interface x2 with 31 bit addressing successful.
class Test31bit_TC05(Test):
    uuid = "SOSAIOT-TC-56158"
    description = show_testcase_info(
        Parameter.TESTPLAN, '05', description=True)['title']
    tc05x2ip = '192.168.100.100'
    tc05pc3ip = '192.168.200.100'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_x2_to_lan(self):
        x2_lan_dict['ip'] = self.tc05x2ip
        output = interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(output, True, "ERR: config interface x2 to lan failed")

    def test_02_config_x3_to_lan(self):
        dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable": True
                }
            }
        }
        dynamic_entry_dict = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.200.101",
                                "to": "192.168.200.120",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": self.tc05pc3ip,
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        x3_lan_dict['ip'] = self.tc05pc3ip
        output = interfacev4api.config_interface(**x3_lan_dict)
        output &= dhcpserverapi.config_dhcp_server_settings(**dhcp_server_settings)
        output &= dhcpserverapi.add_dhcp_server_scope_dynamic(**dynamic_entry_dict)
        Assertion.assert_equal(output, True, "ERR: config interface x3 to lan failed")

    def test_03_config_dhcp_and_route_for_PC3(self):
        res = PC3_login.send_command("ifconfig eth1 0.0.0.0;killall dhclient;dhclient -v eth1;sleep 10;")
        logger.info(f'start dhcp get from pc3 result：{res}')
        res = re.search('bound to 192.168.200.\d+', res, re.I)
        if res:
            res1 = PC3_login.send_command('route add -net 192.168.100.0/24 gw 192.168.200.100')
            logger.info(f'add route to pc3 result：{res1}')
        else:
            logger.info("failed to get ip address for PC3 eth1")
        Assertion.assert_equal(True, True, "ERR: config dhcp an route for x3 failed")

    def test_04_verify_pc3_https_login_x2(self):
        output = login_fw_in_pc(ip=self.tc05x2ip)
        logger.info(f'check https login pass result: {output}')

        x2_lan_dict['mgmt_https'] = False
        uncheckhttps = interfacev4api.config_interface(**x2_lan_dict)
        logger.info(f'uncheck https for X2 result: {uncheckhttps}')
        res = login_fw_in_pc(ip=self.tc05x2ip)
        output &= False if res else True

        # init x2 configure
        x2_lan_dict['mgmt_https'] = True
        x2_lan_dict['ip'] = self.tc05x2ip
        interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(
            output, True, "ERR: PC3 https Login x2 failed")

    def test_05_verify_pc3_ssh_login_x2(self):
        output = login_fw_in_pc(ip=self.tc05x2ip,
                                action='showversion',
                                msg='Firmware Version')
        logger.info(f'check ssh login for x2 result: {output}')

        x2_lan_dict['mgmt_ssh'] = False
        uncheckssh = interfacev4api.config_interface(**x2_lan_dict)
        logger.info(f'x2 uncheck ssh result: {uncheckssh}')
        res = login_fw_in_pc(ip=self.tc05x2ip,
                             action='showversion',
                             msg='Firmware Version')
        output &= False if res else True

        # init x2 configure
        x2_lan_dict['mgmt_ssh'] = True
        x2_lan_dict['ip'] = self.tc05x2ip
        interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(
            output, True, "ERR: PC3 ssh Login x2 failed")

    def test_06_add_snmp_group(self):
        enableres = snmpapi.enable_snmp()
        addres = snmpapi.add_snmp_group(name='group1')
        Assertion.assert_equal(enableres & addres, True, 'ERR: Add snmp group failed!')

    def test_07_add_snmp_user(self):
        user_json = {"snmp": {"user": [
            {"name": "test1", "authentication":
                {"md5": "12345678"},
             "security_level":
                 {"authentication_only": True},
             "group": "group1"}
        ]}}
        rc = snmpapi.add_snmp_user(**user_json)
        Assertion.assert_equal(rc, True, 'ERR: Add snmp user failed!')

    def test_08_add_snmp_access(self):
        access_json = {"snmp": {"access": [
            {"name": "Access1",
             "read_view": "root",
             "master_group": "group1",
             "security_level":
                 {"authentication_only": True}
             }
        ]}}
        rc = snmpapi.add_access(**access_json)
        Assertion.assert_equal(rc, True, 'ERR: Add snmp access failed!')

    def test_09_verify_snmp_get_from_pc3_to_x2(self):
        cmd = f'snmpwalk -c public -u test1 {self.tc05x2ip} -l authNoPriv -a MD5 -A 12345678  1.3.6.1.2.1.4'
        getres = PC3_login.send_command(cmd)
        output = True if 'ipAdEntAddr' in getres else False
        logger.info(f'check snmp get result: {output}')

        x2_lan_dict['mgmt_snmp'] = False
        unchecksnmp = interfacev4api.config_interface(**x2_lan_dict)
        logger.info(f'x2 uncheck snmp result: {unchecksnmp}')
        getres = PC3_login.send_command(cmd)
        output &= True if 'Timeout' in getres else False
        logger.info(f'check snmp get result: {output}')

        # init x2 configure, pc3 route
        x2_lan_dict['mgmt_snmp'] = True
        x2_lan_dict['ip'] = Parameter.X2_IP
        interfacev4api.unassign_interface(interface='X2')
        x3_lan_dict['ip'] = Parameter.X3_IP
        interfacev4api.unassign_interface(interface='X3')
        PC3_login.send_command("route del -net 192.168.100.0/24 gw 192.168.200.100")
        Assertion.assert_equal(output, True, f"ERR: check x2 snmp failed!!")


# Expected: check traffic from pc4 to x4 vlan.
class Test31bit_TC06(Test):
    uuid = "SOSAIOT-TC-56159"
    description = show_testcase_info(
        Parameter.TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_x4_vlan(self):
        x4_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.add_interface(**x4_vlan1_dict)
        Assertion.assert_equal(
            output, True, "ERR: Add Vlan interfaces to X4 failed")

    def test_02_verify_traffic_x4_vlan(self):
        PC4_login.send_command('ifconfig eth1 192.168.40.169')
        time.sleep(10)
        output = PC4_login.ping(Parameter.X4_VLAN1_IP)
        logger.info(f'inbound subnet ping result: {output}')

        PC4_login.send_command('ifconfig eth1 192.168.40.170')
        res = PC4_login.ping(Parameter.X4_VLAN1_IP)
        logger.info(f'outbound subnet ping result: {output}')
        output &= False if res else True

        # init x4 and pc4 ip
        x4_del_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': str(X4_VLAN1_ID),
        }
        interfacev4api.del_interface(**x4_del_vlan1_dict)
        PC4_login.send_command(f'ifconfig eth1 {PC4_ETH1_IP}')
        Assertion.assert_equal(
            output, True, "ERR: verify traffic between PC4 on X4 vlan failed")


# Expected: traffic pass from pc1 to wan via net.
class Test31bit_TC07(Test):
    uuid = "SOSAIOT-TC-56160"
    description = show_testcase_info(
        Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_x3_to_wan(self):
        x3_static_dict = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.config_interface(**x3_static_dict)
        logger.info('config X3 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X3 to static failed")

    def test_02_configure_dut_failover(self):
        # rc = failoverapi.config_failover_groups(**probe_conf_dict)
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X3'
        rc = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(rc, True, "ERR: Config DUT failover failed")

    def test_03_ping_from_pc1_to_wan(self):
        PC1_login.send_command(
            f'route add -host {Parameter.X1_DNS1} gw {Parameter.FIREWALL}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        PC1_login.ping_from_eth(ip=Parameter.X1_DNS1, eth='eth1')
        time.sleep(5)
        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()

        output, checkres = nat_icmp_check(resp, Parameter.X3_IP, Parameter.X1_DNS1)
        logger.info(checkres)

        Assertion.assert_equal(output, True, "ERR: ping form pc1 to wan failed")

    def test_init_tc7_pc_route_fw_interface_lb(self):
        # probe_conf_dict['interface'] = 'X1'
        # failoverapi.config_failover_groups(**probe_conf_dict)
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X1'
        failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        interfacev4api.unassign_interface(interface='X3')
        PC1_login.send_command(
            f'route del -host {Parameter.X1_DNS1} gw {Parameter.FIREWALL}')
        Assertion.assert_equal(True, True, "ERR: init pc and fw failed")


# Expected: BGP Established between dut1 x2 on dut2 x1.
class Test31bit_TC10(Test):
    uuid = "SOSAIOT-TC-56163"
    description = show_testcase_info(
        Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_dut1_x2_to_wan(self):
        res = interfacev4api.config_interface(**x2_static_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to static wan failed")

    def test_02_config_bgp_settings(self):
        logger.info(" {} ".center(20, '-').format('Config local settings for BGP'))
        cmd1 = f'neighbor {Parameter.X1_REMOTE_IP} remote-as 2'
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmd1,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        rc1, output1 = dut1_cli.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('Config remote settings for BGP'))
        cmd2 = f'neighbor {Parameter.X2_IP} remote-as 1'
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'commit',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmd2,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = dut2_cli.do_cli_commands(commands2, 1)
        if 'Error' not in output2:
            logger.info('Remote Success!')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config settings for BGP failed")

    def test_03_check_bgp_status(self):
        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        cmd = f'show ip bgp neighbors {Parameter.X1_REMOTE_IP}'
        commands = [
            'configure',
            'routing',
            'bgp',
            cmd,
            'exit', 'commit', 'end', 'exit']
        rc = False
        for i in range(5):
            logger.info(f'start try {i} time...')
            (ret, output) = dut1_cli.do_cli_commands(commands, 1)
            if 'BGP state = Established' in output:
                logger.info('Check Established Success!')
                rc = True
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: BGP Establish failed")


# Expected: traffic pass between lan x0 to wan x2 var pbr policy.
class Test31bit_TC11(Test):
    uuid = "SOSAIOT-TC-56161"
    description = show_testcase_info(
        Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_dut1_x2_to_wan(self):
        res = interfacev4api.config_interface(**x2_static_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to static wan failed")

    def test_02_configure_dut_failover(self):
        # probe_conf_dict['interface'] = 'X2'
        # rc = failoverapi.config_failover_groups(**probe_conf_dict)
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X2'
        rc = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(rc, True, "ERR: Config DUT failover failed")

    def test_03_add_pbr_form_x0_to_x2(self):
        ao_dict = {
            "object_type": "host",
            "name": Parameter.X1_DNS1,
            "zone": "LAN",
            "value": Parameter.X1_DNS1
        }
        route_policy_dict = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": {'name': 'X0 Subnet'},
                        "destination": {'name': Parameter.X1_DNS1},
                        "service": {'any': True},
                        "gateway": {'name': 'X2 Default Gateway'},
                        "name": "auto_test",
                    }
                }
            ]
        }
        res = aoapi.config_addressobject(**ao_dict)
        res &= routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Config PBR failed")

    def test_04_ping_from_lan_to_wan(self):
        PC1_login.send_command(
            f'route add -host {Parameter.X1_DNS1} gw {Parameter.FIREWALL}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        PC1_login.ping_from_eth(ip=Parameter.X1_DNS1, eth='eth1')
        time.sleep(5)
        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()

        output, packet = nat_icmp_check(resp, Parameter.X2_IP, Parameter.X1_DNS1)
        logger.info(packet)
        Assertion.assert_equal(output, True, "ERR: ping form lan to wan failed")

    def test_init_pc_route_fw_interface_lb(self):
        # probe_conf_dict['interface'] = 'X1'
        # failoverapi.config_failover_groups(**probe_conf_dict)
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X1'
        failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        interfacev4api.unassign_interface(interface='X2')
        PC1_login.send_command(
            f'route del -host {Parameter.X1_DNS1} gw {Parameter.FIREWALL}')
        Assertion.assert_equal(True, True, "ERR: init pc and fw failed")


# Expected: traffic will pass from lan to x2 sub wilie set x2 to lan/dmz/custom zone.
class Test31bit_TC31(Test):
    uuid = "SOSAIOT-TC-56162"
    description = show_testcase_info(
        Parameter.TESTPLAN, '31', description=True)['title']
    tc31x2ip = '12.12.1.80'
    tc31pc2eth1 = '12.12.1.81'
    tc31czname1 = 'tc31customzone1'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_config_dut1_x2_to_lan(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'lan',
            'mode': 'static',
            'ip': self.tc31x2ip,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = interfacev4api.config_interface(**x2_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to lan failed")

    def test_02_ping_from_lan_to_lan(self):
        PC2_login.send_command(f'ifconfig eth1 {self.tc31pc2eth1}')
        PC2_login.send_command(
            f'route add -net {Parameter.X0_NET}/24 gw {self.tc31x2ip}')
        res = PC1_login.ping_from_eth(ip=self.tc31pc2eth1, eth='eth1')
        Assertion.assert_equal(res, True, "ERR: ping form lan to lan failed")

    def test_03_config_dut1_x2_to_dmz(self):
        x2_dmz_dict = {
            'if': 'X2',
            'zone': 'dmz',
            'mode': 'static',
            'ip': self.tc31x2ip,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = interfacev4api.config_interface(**x2_dmz_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to dmz failed")

    def test_04_ping_from_lan_to_dmz(self):
        res = PC1_login.ping_from_eth(ip=self.tc31pc2eth1, eth='eth1')
        Assertion.assert_equal(res, True, "ERR: ping form lan to dmz failed")

    def test_05_config_x2_to_custom_zone(self):
        base_dict = {
            'name': self.tc31czname1,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        x2_cz_dict = {
            'if': 'X2',
            'zone': base_dict['name'],
            'mode': 'static',
            'ip': self.tc31x2ip,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        if output:
            output &= interfacev4api.config_interface(**x2_cz_dict)
        Assertion.assert_equal(output, True, "ERR: config x2 to custom zone failed")

    def test_06_ping_from_lan_to_custom_zone(self):
        res = PC1_login.ping_from_eth(ip=self.tc31pc2eth1, eth='eth1')
        Assertion.assert_equal(res, True, "ERR: ping form lan to custom zone failed")

    def test_init_pc_route_fw_interface_lb(self):
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.tc31czname1)
        PC2_login.send_command(f'ifconfig eth1 {PC2_ETH1_IP}')
        PC2_login.send_command(
            f'route del -net {Parameter.X0_NET}/24 gw {self.tc31x2ip}')
        Assertion.assert_equal(True, True, "ERR: init pc and fw failed")
