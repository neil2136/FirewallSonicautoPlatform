from definition.settings import *
from definition.utils import *


#   Assign Primary WAN IPv6 through PPPoEv6
class TestPPPoE_TC012(Test):
    uuid = "SOSAIOT-TC-56652"
    description = show_testcase_info(
        TESTPLAN, '1530520', description=True)['title']
    res_for_tc20 = ContextVar('res_for_tc20')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530520')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_as_pppoe(self):
        x1_pppoe_opt_dynamic_dict = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'test',
            'pppoe_servicename': '',
            'pppoe_passwd': 'test',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 2,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        res = interfaceapi.config_interface(**x1_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X1 pppoe ip failed!")

    def test_02_config_X1_as_pppoev6(self):
        x1_v6_dict = {
            'name': 'x1',
            'mode': 'pppoe6',
            "listen_router_advertisement": True,
            'pppoe6': {
                'mode_assign': 'dhcpv6',
                'dhcp_mode': 'auto',
                 'prefix_delegation':
                     {"preferred":
                          {'addr': "2001:db8:2226:2d00::",
                           'prefix': 56}
                      },
                'rapid_commit': False,
                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
        res = interfacev6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X1 pppoev6 failed!")

    @repeat_method(5)
    def test_03_check_ppp_on_pc2(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X1', version='v4')
        print(ip_addr)
        if "192.168.2." not in str(ip_addr):
            interfaceapi.click_pppoe_connect('X1')

        time.sleep(10)
        res1 = PC2_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC2_login.send_command('timeout 5 systemctl restart pppoe-server')

            time.sleep(5)

            interfaceapi.click_pppoe_disconnect('X1')
            interfaceapi.click_pppoe_connect('X1')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name='X1', version='v4')
            print(ip_addr)
            res2 = PC2_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: Check ppp on pc2 failed!")

    @repeat_method(5)
    def test_04_check_X1_pppoev6_address(self):
        start_dibbler_server(PC2_login)
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if "2001:db8:222:" in str(ip_addr['ip_address']) and 'DHCPv6' in str(ip_addr['ip_address']) else False
        self.res_for_tc20.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X1 pppoe ip failed!")


#  Verify PPPoEv6 can obtain IPv6 address in DHCPv6 Automatic mode
class TestPPPoE_TC020(Test):
    uuid = "SOSAIOT-TC-56663"
    description = show_testcase_info(
        TESTPLAN, '1530549', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530549')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_X2_pppoev6_address(self):
        flag = TestPPPoE_TC012().res_for_tc20.get()
        Assertion.assert_equal(flag, True, "ERR: PPPoEv6 obtain IPv6 address in DHCPv6 Automatic mode failed!")


# Assign Secondary WAN IPv6 through PPPoEv6 and Primary as Static
class TestPPPoE_TC013(Test):
    uuid = "SOSAIOT-TC-56653"
    description = show_testcase_info(
        TESTPLAN, '1530522', description=True)['title']
    res_for_tc21 = ContextVar('res_for_tc21')
    res_for_tc27_1 = ContextVar('res_for_tc27_1')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530522')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_as_static(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc1, True, "ERR: Config X1 to static failed")

    def test_02_config_X2_as_pppoe(self):
        x2_pppoe_opt_dynamic_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'test',
            'pppoe_servicename': '',
            'pppoe_passwd': 'test',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 2,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        res = interfaceapi.config_interface(**x2_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoe ip failed!")

    def test_03_config_X2_as_pppoev6(self):
        x2_v6_dict = {
            'name': 'x2',
            'mode': 'pppoe6',
            "listen_router_advertisement": True,
            'pppoe6': {
                'mode_assign': 'dhcpv6',
                'dhcp_mode': 'manual',
                'prefix_delegation': {
                    "preferred": {}
                },

                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
        res = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoev6 failed!")

    @repeat_method(5)
    def test_04_check_ppp_on_pc3(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
        print(ip_addr)

        if "192.168.3." not in str(ip_addr):
            interfaceapi.click_pppoe_connect('X2')

        time.sleep(10)
        res1 = PC3_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC3_login.send_command('timeout 5 systemctl restart pppoe-server')
            time.sleep(5)

            interfaceapi.click_pppoe_disconnect('X2')
            interfaceapi.click_pppoe_connect('X2')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
            print(ip_addr)
            res2 = PC3_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: check ppp on pc2 failed!")

    @repeat_method(5)
    def test_05_check_X2_pppoev6_address(self):
        start_dibbler_server(PC3_login)
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        flag = True if "2001:db8:333:" in str(ip_addr) else False
        self.res_for_tc21.set(flag)
        self.res_for_tc27_1.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X2 pppoe ip failed!")


#  Verify PPPoEv6 can obtain IPv6 address in DHCPv6 manual mode
class TestPPPoE_TC021(Test):
    uuid = "SOSAIOT-TC-56664"
    description = show_testcase_info(
        TESTPLAN, '1530550', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530550')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_X2_pppoev6_address(self):
        flag = TestPPPoE_TC013().res_for_tc21.get()
        Assertion.assert_equal(flag, True, "ERR: PPPoEv6 obtain IPv6 address in DHCPv6 manual mode failed!")


 # Assign both Primary and Secondary WAN IPv6 address through PPPoEv6
class TestPPPoE_TC014(Test):
    uuid = "SOSAIOT-TC-56654"
    description = show_testcase_info(
        TESTPLAN, '1530524', description=True)['title']

    res_for_tc54 = ContextVar('res_for_tc54')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530524')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_pppoev6(self):
        TestPPPoE_TC012().test_01_config_X1_as_pppoe()
        TestPPPoE_TC012().test_02_config_X1_as_pppoev6()

    @repeat_method(5)
    def test_02_check_ppp_on_pc2(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X1', version='v4')
        print(ip_addr)
        if "192.168.2." not in str(ip_addr):
            interfaceapi.click_pppoe_connect('X1')

        time.sleep(10)
        res1 = PC2_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC2_login.send_command('timeout 5 systemctl restart pppoe-server')
            time.sleep(5)

            interfaceapi.click_pppoe_disconnect('X1')
            interfaceapi.click_pppoe_connect('X1')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name='X1', version='v4')
            print(ip_addr)
            res2 = PC2_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: Check ppp on pc2 failed!")

    @repeat_method(5)
    def test_03_check_X1_pppoev6_address(self):
        start_dibbler_server(PC2_login)
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X1', version='v6')
        flag = True if "2001:db8:222:" in str(ip_addr) else False
        self.res_for_tc54.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X1 pppoe ip failed!")

    def test_04_export_exp_verify_tc058(self):
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")


# [FC][PPPoEv6 interface][16.4]Verify related AO can resolve correct address
# when PPPoEv6 interface get address thru DHCPv6 mode
class TestPPPoE_TC109(Test):
    uuid = "SOSAIOT-TC-56658"
    description = show_testcase_info(
        TESTPLAN, '1530544', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530544')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ao(self):
        res_ao = aoapi.get_addressobject_by_name(name='X2 IPv6 Primary Dynamic Address', version='ipv6')
        flag_ao = True if '2001:db8:333:0:' in str(res_ao) else False
        res_subnet = aoapi.get_addressobject_by_name(name='X2 IPv6 Primary Dynamic Address Subnet', version='ipv6')
        flag_subnet = True if "2001:db8:333::" in str(res_subnet) else False
        Assertion.assert_equal(flag_ao & flag_subnet, True, "ERR: related AO can't resolve correct address!")


# Verify IPv6 defualt route generated by PPPoEv6 pramary WAN interface.
class TestPPPoE_TC029(Test):
    uuid = "SOSAIOT-TC-56672"
    description = show_testcase_info(
        TESTPLAN, '1530558', description=True)['title']
    res_for_tc54 = ContextVar('res_for_tc54')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530558')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_route(self):
        flag = False
        res = routepolicyapi.show_route_policy_system(version='ipv6')
        logger.info(res)
        for route in res:
            if route['source'] == 'Any' and route['destination'] == '::/0' and 'fe80::' in route['gateway'] and route['interface'] == 'X1':
                flag = True
                break

        Assertion.assert_equal(flag, True, "ERR: Verify IPv6 defualt route generated by PPPoEv6 pramary WAN interface failed")


# [FC][Route table check][3.1]Verify the Route table when PPPoE IPv6 interface is the default WAN
class TestPPPoE_TC074(Test):
    uuid = "SOSAIOT-TC-56670"
    description = show_testcase_info(
        TESTPLAN, '1530567', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530567')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        lb_ipv6 = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group IPv6",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverapi.config_failover_groups_by_multi(**lb_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    @repeat_method(5)
    def test_02_check_route(self):
        time.sleep(25)
        flag = False
        res = routepolicyapi.show_route_policy_system(version='ipv6')
        logger.info(res)
        for route in res:
            if route['source'] == 'Any' and route['destination'] == '::/0' and 'fe80::' in route['gateway'] and route['interface'] == 'X2':
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Verify the Route table when PPPoE IPv6 interface is the default WAN failed")


# Change WAN IP assignment from static to PPPoEv6
class TestPPPoE_TC054(Test):
    uuid = "SOSAIOT-TC-56657"
    description = show_testcase_info(
        TESTPLAN, '1530542', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530542')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_get_pppoev6_address_change_from_static(self):
        flag = TestPPPoE_TC014().res_for_tc54.get()
        Assertion.assert_equal(flag, True, "ERR: Change WAN IP assignment from static to PPPoEv6 failed!")


#  PPPoEv6 information can be included in the Tech Support Report
class TestPPPoE_TC059(Test):
    uuid = "SOSAIOT-TC-56669"
    description = show_testcase_info(
        TESTPLAN, '1530562', description=True)['title']

    res_for_tc22 = ContextVar('res_for_tc22')
    res_for_tc23 = ContextVar('res_for_tc23')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530562')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_tsr(self):
        tsr_info = diagnosticapi.get_tsr_part('Network', 'Interfaces')
        x1_check_list = ['PPPoEv6', 'X1']
        x2_check_list = ['PPPoEv6', 'X2']
        x1_pppoev6_part = get_interface_part_in_tsr(tsr_info, x1_check_list)
        logger.info(x1_pppoev6_part)
        x2_pppoev6_part = get_interface_part_in_tsr(tsr_info, x2_check_list)
        logger.info(x2_pppoev6_part)
        flag = True if 'IA Addresses' in x1_pppoev6_part and 'IA Addresses' in x2_pppoev6_part else False
        self.res_for_tc22.set(x2_pppoev6_part)
        self.res_for_tc23.set(x1_pppoev6_part)
        Assertion.assert_equal(flag, True, "ERR: Get PPPoEv6 information in TSR failed")


# Verify DHCPv6 PD option can be obtained from PPPoEv6 server side
class TestPPPoE_TC022(Test):
    uuid = "SOSAIOT-TC-56665"
    description = show_testcase_info(
        TESTPLAN, '1530551', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530551')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_pd_info_from_tsr(self):
        x2_pppoev6_part = TestPPPoE_TC059().res_for_tc22.get()
        m = re.search(r'IA Prefixes:\s+(\d.+/56)', x2_pppoev6_part, re.M)
        if m:
            logger.info(f'get obtained Prefix in TSR file success.\n{m.group()}')
            logger.info(f'Prefix info:{m.group(1)}')
            flag = True if '2001:db8:3336:' in m.group(1) else False
        else:
            flag = False
        Assertion.assert_equal(flag, True, "ERR: check pd info from tsr failed")


#  check Send hints for renewing previous IP on startup can work fine when WAN ipv6 assignment in PPPOEv6 mode
class TestPPPoE_TC023(Test):
    uuid = "SOSAIOT-TC-86963"
    description = show_testcase_info(
        TESTPLAN, '1530552', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530552')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_pd_info_from_tsr(self):
        x2_pppoev6_part = TestPPPoE_TC059().res_for_tc23.get()
        m = re.search(r'IA Prefixes:\s+(\d.+/56)', x2_pppoev6_part, re.M)
        if m:
            logger.info(f'get obtained Prefix in TSR file success.\n{m.group()}')
            logger.info(f'Prefix info:{m.group(1)}')
            flag = True if '2001:db8:2226:21' in m.group(1) else False
        else:
            flag = False
        Assertion.assert_equal(flag, True, "ERR: check pd info from tsr failed")


# Verify disconnecting PPPoEv6 connection from SonicWALL
class TestPPPoE_TC039(Test):
    uuid = "SOSAIOT-TC-56656"
    description = show_testcase_info(
        TESTPLAN, '1530536', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530536')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disconnect_pppoe(self):
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        interfaceapi.click_pppoe_disconnect('X2')
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = False if "2001:db8:333:" in str(ip_addr) else True
        Assertion.assert_equal(flag, True, "ERR: Configure X1 pppoe ip failed!")


# Verify PPPoEv6 can obtain IPv6 address in Auto mode
class TestPPPoE_TC025(Test):
    uuid = "SOSAIOT-TC-56666"
    description = show_testcase_info(
        TESTPLAN, '1530554', description=True)['title']
    res_for_tc27_2 = ContextVar('res_for_tc27_2')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530554')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_as_pppoe_auto(self):
        x2_v6_dict = {
            'name': 'x2',
            'mode': 'pppoe6',
            'pppoe6': {
                'mode_assign': 'auto',
                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
        res = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        logger.info(f"configure X2 as PPPoeV6 auto mode {res}")

    @repeat_method(5)
    def test_02_check_ppp_on_pc3(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
        print(ip_addr)

        if "192.168.3." not in str(ip_addr):
            interfaceapi.click_pppoe_connect('X2')

        time.sleep(10)
        res1 = PC3_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC3_login.send_command('timeout 5 systemctl restart pppoe-server')
            time.sleep(5)

            interfaceapi.click_pppoe_disconnect('X2')
            interfaceapi.click_pppoe_connect('X2')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
            print(ip_addr)
            res2 = PC3_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: check ppp on pc2 failed!")


    @repeat_method(5)
    def test_03_check_X2_pppoev6_address(self):
        PC3_login.send_command('timeout 5 systemctl restart radvd')
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if '2001:db8:3333:2:' in str(ip_addr) and 'Autonomous' in str(ip_addr['ip_address']) else False
        self.res_for_tc27_2.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X2 pppoe ip failed!")


# Verify PPPoEv6 can obtain IPv6 address in Static mode
class TestPPPoE_TC026(Test):
    uuid = "SOSAIOT-TC-56667"
    description = show_testcase_info(
        TESTPLAN, '1530555', description=True)['title']
    res_for_tc27_3 = ContextVar('res_for_tc27_3')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530555')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_as_pppoe_static(self):
        x2_v6_dict = {
            'name': 'x2',
            'mode': 'pppoe6',
            'pppoe6': {
                'mode_assign': 'static',
                'ip': '2001:db8:3333:26::25',
                'gateway': '2001:db8::1',
                'prefix_length': 64,
                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
        res = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        logger.info(f"configure X2 as PPPoeV6 static mode {res}")
        time.sleep(20)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if "2001:db8:3333:26:" in str(ip_addr['ip_address']) and 'Static' in str(ip_addr['ip_address']) else False
        self.res_for_tc27_3.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Configure X2 pppoe ip failed!")


# Switch global address obtain ways of PPPOEv6 between Auto, Static, DHCPv6
class TestPPPoE_TC027(Test):
    uuid = "SOSAIOT-TC-56668"
    description = show_testcase_info(
        TESTPLAN, '1530556', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530556')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_pd_info_from_tsr(self):
        dhcp_res = TestPPPoE_TC013().res_for_tc27_1.get()
        auto_res = TestPPPoE_TC025().res_for_tc27_2.get()
        static_res = TestPPPoE_TC026().res_for_tc27_3.get()
        Assertion.assert_equal(static_res & auto_res & dhcp_res, True, "ERR: Switch global address obtain ways of PPPOEv6 between Auto, Static, DHCPv6 failed")


#  Boundary check for Inactivity Disconnect
class TestPPPoE_TC018(Test):
    uuid = "SOSAIOT-TC-56655"
    description = show_testcase_info(
        TESTPLAN, '1530528', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530528')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_invalid_inactivity(self):
        # 0 can accept in api as "inactivity": {}
        inactive_list = [-1, 1000]
        res_list = []
        for inactive_time in inactive_list:

            test_inactivity_dict = copy.deepcopy(x1_v6_dict)
            test_inactivity_dict['pppoe6']['inactivity'] = inactive_time
            res = interfacev6api.config_interface_ipv6(**test_inactivity_dict)
            res_list.append(True) if not res else res_list.append(False)

        flag = True if all(res_list) else False
        Assertion.assert_equal(flag, True, "ERR:  Boundary check for Inactivity Disconnect failed!")

    def test_02_config_X2_valid_inactivity(self):
        inactive_list = [999, 1]
        res_list = []
        for inactive_time in inactive_list:
            test_inactivity_dict = copy.deepcopy(x1_v6_dict)
            test_inactivity_dict['pppoe6']['inactivity'] = inactive_time
            res = interfacev6api.config_interface_ipv6(**test_inactivity_dict)
            res_list.append(res)

        flag = True if all(res_list) else False
        Assertion.assert_equal(flag, True, "ERR:  Boundary check for Inactivity Disconnect failed!")


# [FC][Boundary test for Inactivity Disconnect][10.3]Verify if set "Inactivity Disconnect" value<1 to see if FW can accept this value
class TestPPPoE_TC093(Test):
    uuid = "SOSAIOT-TC-56671"
    description = show_testcase_info(
        TESTPLAN, '1530570', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530570')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_invalid_inactivity(self):
        inactive_list = [0.1, 0.9, -3.6]
        res_list = []
        for inactive_time in inactive_list:
            test_inactivity_dict = copy.deepcopy(x1_v6_dict)
            test_inactivity_dict['pppoe6']['inactivity'] = inactive_time
            res = interfacev6api.config_interface_ipv6(**test_inactivity_dict)
            res_list.append(True) if not res else res_list.append(False)

        flag = True if all(res_list) else False
        Assertion.assert_equal(flag, True, "ERR:  Boundary check for Inactivity Disconnect failed!")


#  [CLI][19.5]Verify "Listening to RA" should be enabled when set an interface as PPPoEv6 DHCPv6 thru CLI
class TestPPPoE_TC123(Test):
    uuid = "SOSAIOT-TC-56660"
    description = show_testcase_info(
        TESTPLAN, '1530546', description=True)['title']
    res_for_tc128_1 = ContextVar('res_for_tc128_1')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530546')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_PPPoEv6_DHCPv6_via_cli(self):
        cmds = ['configure', 'interface ipv6 x2', 'ip-assignment pppoe6', ' mode-assignment dhcpv6', 'mode auto',
                'exit','listen-router-advertisement',
                'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)

        Assertion.assert_equal(rc, True, 'ERR: config PPPoEv6 DHCPv6 via CLI failed!!')

    @repeat_method(5)
    def test_02_check_ppp_on_pc3(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
        print(ip_addr)

        if "192.168.3." not in str(ip_addr):
            interfaceapi.click_pppoe_connect('X2')

        time.sleep(10)
        res1 = PC3_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC3_login.send_command('timeout 5 systemctl restart pppoe-server')
            time.sleep(5)

            interfaceapi.click_pppoe_disconnect('X2')
            interfaceapi.click_pppoe_connect('X2')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name='X2', version='v4')
            print(ip_addr)
            res2 = PC3_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: check ppp on pc3 failed!")

    @repeat_method(5)
    def test_03_check_X2_pppoev6_address(self):
        start_dibbler_server(PC3_login)
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if "2001:db8:333:" in str(ip_addr['ip_address']) else False
        self.res_for_tc128_1.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X2 pppoe ip failed!")

    def test_04_Listening_to_RA_via_cli(self):
        cmds = ['configure', 'interface ipv6 x2', 'no listen-router-advertisement',
                'commit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, False, 'ERR: disable Listening to RA via CLI failed!!')


#  [CLI][19.4]Verify an interface can be assigned as PPPoEv6 Static mode thru CLI commands without any error or issue
class TestPPPoE_TC119(Test):
    uuid = "SOSAIOT-TC-56659"
    description = show_testcase_info(
        TESTPLAN, '1530545', description=True)['title']
    res_for_tc128_2 = ContextVar('res_for_tc128_2')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530545')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_PPPoEv6_static_via_cli(self):
        cmds = ['configure', 'interface ipv6 x2', 'ip-assignment pppoe6',
                'mode-assignment static',
                'ip 2001:db8:3333:26::119',
                'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: config PPPoEv6 static via CLI failed!!')

    def test_02_check_X2_pppoev6_address(self):
        time.sleep(20)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if "2001:db8:3333:26:" in str(ip_addr['ip_address']) and 'Static' in str(ip_addr['ip_address']) else False
        self.res_for_tc128_2.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Configure X2 pppoe ip failed!")


#  [CLI][19.7]Verify "Show" command can display correct info for PPPoEv6 interface with Auto mode
class TestPPPoE_TC125(Test):
    uuid = "SOSAIOT-TC-56661"
    description = show_testcase_info(
        TESTPLAN, '1530547', description=True)['title']
    res_for_tc128_3 = ContextVar('res_for_tc128_3')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530547')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_PPPoEv6_auto_via_cli(self):
        cmds = ['configure', 'interface ipv6 x2', 'ip-assignment pppoe6', ' mode-assignment auto',
                'commit',
                'end', 'end']
        rc = fw_cli.do_cli_commands(cmds)

        Assertion.assert_equal(rc, True, 'ERR: config PPPoEv6 auto via CLI failed!!')

    def test_02_show_PPPoEv6_info_via_cli(self):
        rc = interfacecli.show_interface_status(interface='X2', version='ipv6')
        logger.info(rc)
        flag = True if 'ip-assignment pppoe6' in str(rc) and 'mode-assignment auto' in str(rc) else False
        Assertion.assert_equal(flag, True, 'ERR: show PPPoEv6 info via cli failed!!')

    @repeat_method(5)
    def test_03_check_X2_pppoev6_address(self):
        PC3_login.send_command('timeout 5 systemctl restart radvd')
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X2', version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if '2001:db8:3333:2:' in str(ip_addr) and 'Autonomous' in str(ip_addr['ip_address']) else False
        self.res_for_tc128_3.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Check X2 pppoe ip failed!")


# [CLI][19.10]Verify function can work well when change the PPPoEv6 mode using CLI commands
class TestPPPoE_TC128(Test):
    uuid = "SOSAIOT-TC-56662"
    description = show_testcase_info(
        TESTPLAN, '1530548', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530548')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_PPPoEv6_mode(self):
        dhcp_res = TestPPPoE_TC123().res_for_tc128_1.get()
        static_res = TestPPPoE_TC119().res_for_tc128_2.get()
        auto_res = TestPPPoE_TC125().res_for_tc128_3.get()
        Assertion.assert_equal(static_res & auto_res & dhcp_res, True,
                               "ERR: function can't work well when change the PPPoEv6 mode using CLI commands")


# pppoev6 can obtain IPv6 address with VLAN sub interface
class TestPPPoE_TC028(Test):
    uuid = "SOSAIOT-TC-56673"
    description = show_testcase_info(
        TESTPLAN, '1530557', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530557')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_vlan_as_pppoe(self):
        x3_pppoe_opt_dynamic_dict = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID,
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'test',
            'pppoe_servicename': '',
            'pppoe_passwd': 'test',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 2,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        res = interfaceapi.add_interface(**x3_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X3 pppoe ip failed!")

    def test_02_config_X3_as_pppoev6(self):
        x3_v6_dict = {
            'name': 'x3',
            'type': 'vlan',
            'vlan': X3_VLAN1_ID,
            'mode': 'pppoe6',
            "listen_router_advertisement": True,
            'pppoe6': {
                'mode_assign': 'dhcpv6',
                'dhcp_mode': 'manual',
                'prefix_delegation': {
                    "preferred": {}
                },
                'rapid_commit': False,
                'inactivity': 5,
                'lcp_echo_packets': False,
                'ncp_neg_retrans': 5,
                'reconnect': 5,
            }
        }
        res = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X1 pppoev6 failed!")

    @repeat_method(5)
    def test_03_check_ppp_on_pc2(self):
        time.sleep(10)
        ip_addr = interfaceapi.get_interface_address(name='X3', version='v4')
        print(ip_addr)
        if "192.168.1." not in str(ip_addr):
            interfaceapi.click_pppoe_connect(f'X3:V{X3_VLAN1_ID}')

        time.sleep(10)
        res1 = PC4_login.send_command("ifconfig")
        flag = True if 'ppp0' in res1 else False

        if not flag:
            PC4_login.send_command('timeout 5 systemctl restart pppoe-server')
            time.sleep(5)

            interfaceapi.click_pppoe_disconnect(f'X3:V{X3_VLAN1_ID}')
            interfaceapi.click_pppoe_connect(f'X3:V{X3_VLAN1_ID}')
            time.sleep(10)
            ip_addr = interfaceapi.get_interface_address(name=f'X3:V{X3_VLAN1_ID}', version='v4')
            print(ip_addr)
            res2 = PC4_login.send_command("ifconfig")
            flag = True if 'ppp0' in res2 else False

        Assertion.assert_equal(flag, True, "ERR: Check ppp on pc4 failed!")

    @repeat_method(5)
    def test_04_check_X3_pppoev6_address(self):
        start_dibbler_server(PC4_login)
        time.sleep(10)
        ip_addr = interfaceapi.get_vlan_interface_address(name='X3', vlan=str(X3_VLAN1_ID), version='v6')
        logger.info(ip_addr['ip_address'])
        flag = True if "2001:db8:444:" in str(ip_addr['ip_address']) and 'DHCPv6' in str(
            ip_addr['ip_address']) else False
        Assertion.assert_equal(flag, True, "ERR: Check X4 vlan pppoe ip failed!")


# Export/import preference file
class TestPPPoE_TC058(Test):
    uuid = "SOSAIOT-TC-56674"
    description = show_testcase_info(
        TESTPLAN, '1530561', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530561')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_tsr(self):
        tsr_info = diagnosticapi.get_tsr_part('Network', 'Interfaces')
        x1_check_list = ['PPPoEv6', 'X1']
        x2_check_list = ['PPPoEv6', 'X2']
        x3_check_list = ['PPPoEv6', 'X3']
        x1_pppoev6_part = get_interface_part_in_tsr(tsr_info, x1_check_list)
        logger.info(x1_pppoev6_part)
        x2_pppoev6_part = get_interface_part_in_tsr(tsr_info, x2_check_list)
        logger.info(x2_pppoev6_part)  
        x3_pppoev6_part = get_interface_part_in_tsr(tsr_info, x3_check_list)
        logger.info(x3_pppoev6_part)
        flag = True if x1_pppoev6_part and x2_pppoev6_part and x3_pppoev6_part else False
        Assertion.assert_equal(flag, True, "ERR: Get PPPoEv6 information in TSR failed")

    def test_02_import_exp_verify_tc014(self):
        res = settingapi.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_03_check_tsr(self):
        tsr_info = diagnosticapi.get_tsr_part('Network', 'Interfaces')
        x1_check_list = ['PPPoEv6', 'X1']
        x2_check_list = ['PPPoEv6', 'X2']
        x3_check_list = ['PPPoEv6', 'X3']
        x1_pppoev6_part = get_interface_part_in_tsr(tsr_info, x1_check_list)
        logger.info(x1_pppoev6_part)
        x2_pppoev6_part = get_interface_part_in_tsr(tsr_info, x2_check_list)
        logger.info(x2_pppoev6_part)
        x3_pppoev6_part = get_interface_part_in_tsr(tsr_info, x3_check_list)
        logger.info(x3_pppoev6_part)
        flag = True if x1_pppoev6_part and x2_pppoev6_part and not x3_pppoev6_part else False
        Assertion.assert_equal(flag, True, "ERR: Get PPPoEv6 information in TSR failed")
