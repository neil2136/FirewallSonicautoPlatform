from definition.settings import *
from definition.guestservicestep import *


# make sure transparent info not show in lan/dmz/custom zone for interface x2.
@paramunittest.parametrized(
    {'uuid': '1527023', 'zone': 'LAN', 'interface': 'X2', "protocol": "https"},
    {'uuid': '1527023', 'zone': 'DMZ', 'interface': 'X3', "protocol": "https"},
    {'uuid': '1527029', 'zone': 'cus_trust', 'interface': 'X4', "protocol": "https"},
    {'uuid': '1527029', 'zone': 'cus_public', 'interface': 'X4', "protocol": "https"},
    {'uuid': '1527036', 'zone': 'LAN', 'interface': 'X2', "protocol": "https"},
    {'uuid': '1527036', 'zone': 'DMZ', 'interface': 'X3', "protocol": "https"},
    {'uuid': '1527034', 'zone': 'LAN', 'interface': 'X2', "protocol": "http"},
    {'uuid': '1527034', 'zone': 'DMZ', 'interface': 'X3', "protocol": "http"},
)
class Test01_EnableGuest(Test):
    def setParameters(self, uuid, zone, interface, protocol):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.protocol = protocol
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface, protocol=self.protocol)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_08_verify_guest_login_status(self):
        self.guesttest.verify_guest_login_status()

    def test_09_verify_guest_user_login_success_log(self):
        pattern = '"user_name": "guest".*"message": "User login from an internal zone allowed"'
        self.guesttest.verify_guest_user_login_success_log(pattern)

    def test_10_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


@paramunittest.parametrized(
    {'uuid': '1527037', 'zone': 'LAN', 'interface': 'X2'},
    {'uuid': '1527037', 'zone': 'DMZ', 'interface': 'X3'},
    {'uuid': '1527037', 'zone': 'cus_public', 'interface': 'X4'}
)
class Test02_DisableGuestOnLanDmz_TC1527037(Test):
    def setParameters(self, uuid, zone, interface):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_guest_service(self):
        self.guesttest.disable_guest_service()

    def test_02_verify_guest_service_disabled(self):
        self.guesttest.verify_guest_service_disabled()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("redirect")


@paramunittest.parametrized(
    {'zone': 'LAN', 'interface': 'X2'},
    {'zone': 'DMZ', 'interface': 'X3'},
    {'zone': 'cus_public', 'interface': 'X4'}
)
class Test03_EnableGuestServiceFromLocalUser_TC1527044(Test):
    uuid = "SOSAIOT-TC-56115"

    def setParameters(self, zone, interface):
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface, zone_obj=zonecusadmin_api)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_02_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_03_disable_guest_service(self):
        self.guesttest.disable_guest_service()

    def test_04_verify_guest_service_disabled(self):
        self.guesttest.verify_guest_service_disabled()


@paramunittest.parametrized(
    {'uuid': '1527038', 'user': 'disable_guest','password':'password',
     'pattern': '"user_name":\s"disable_guest".*?"message":\s*"Guest account .*disable_guest.* disabled"'},
    {'uuid': '1527039', 'user': 'expire_guest','password':'password',
     'pattern': '"user_name":\s*"expire_guest".*?"message":\s*"Guest Account Timeout"'},
    {'uuid': '1527045', 'user': 'notguest','password':'S0nic@uto',
     'pattern': '"user_name":\s*"notguest".*?"message":\s*"User login denied - User has no privileges for guest service"'}
)
class Test04_LoginWithNotValidUser(Test):

    def setParameters(self, uuid, user,password, pattern):
        self.uuid = uuid
        self.user = user
        self.pattern = pattern
        self.password=password
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep('LAN', 'X2', username=self.user,password=self.password)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc_expect_fail("login_page")

    def test_08_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_09_verify_log_info(self):
        self.guesttest.verify_guest_user_login_success_log(self.pattern)


class Test05_LoginWithLocalGuestUser(Test):
    uuid = "SOSAIOT-TC-56117"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('LAN', 'X2', username='localguest',password="S0nic@uto")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_08_verify_guest_login_status(self):
        self.guesttest.verify_guest_login_status()

    def test_08_verify_log_info(self):
        pattern = '"user_name": "localguest".*"message": "User login from an internal zone allowed"'
        self.guesttest.verify_guest_user_login_success_log(pattern)

    def test_09_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


@paramunittest.parametrized(
    {'uuid': '1527050', 'username': 'localguest','password':'S0nic@uto'},
    {'uuid': '1527049', 'username': 'guest','password':'password'}
)
class Test06_LogoutLocalGuestUser(Test):

    def setParameters(self, uuid, username,password):
        self.uuid = uuid
        self.user = username
        self.password=password
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep('LAN', 'X2', username=self.user,password=self.password)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_and_logout_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("logout")

    def test_08_verify_guest_login_status(self):
        self.guesttest.verify_user_not_in_status_page()


class Test07_GuestStatusShowCorrectInformation(Test):
    uuid = "SOSAIOT-TC-56114"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('cus_trust', 'X4', username='guest')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_08_verify_guest_login_status(self):
        self.guesttest.verify_user_info_correct_status_page()

    def test_09_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


class Test08_RedirectHttpWithDHCP(Test):
    uuid = "SOSAIOT-TC-56107"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('cus_trust', 'X4', username='guest', protocol="http")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_Enable_DHCP_Server(self):
        dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable": True
                }
            }
        }
        ret = dhcpserver_api.config_dhcp_server_settings(**dhcp_server_settings)
        Assertion.assert_equal(ret, True, "ERR: Enable DHCP Server failed")

    def test_04_add_dynamic_entry_to_X4(self):
        dynamic_entry1 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.4.10",
                                "to": "192.168.4.20",
                                "enable": True,
                                "lease_time": 1,
                                "default_gateway": "192.168.4.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret1 = dhcpserver_api.add_dhcp_server_scope_dynamic(**dynamic_entry1)
        Assertion.assert_equal(ret1, True, "ERR: Add dynamic entries failed")

    def test_05_verify_client_can_get_correct_lease(self):
        rc = False
        PC4_host.send_command("ifconfig eth1 0.0.0.0")
        output = PC4_host.send_commands(["dhclient -r",
                                         "dhclient -v eth1"])
        logger.info(output)
        m = re.search(r'bound to (192\.168\.4\.\d+).*renewal in', output, re.I)
        if m:
            logger.info("PC1 eth1 successfully get ip address {}".format(m.group(1)))
            Parameter.pc4eth1_ip = m.group(1)
            rc = True
        else:
            logger.info("failed to get ip address for PC1 eth1")
        Assertion.assert_equal(rc, True, "ERR: Verify multiple clients can get correct leases failed")

    @repeat_method(3)
    def test_06_add_static_route_to_pc(self):
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X4_IP}',
                'ip -4 r']
        output = PC4_host.send_commands(cmds)
        rc = True if f'{Parameter.https_server_ip} via {Parameter.X4_IP}' in output else False
        Assertion.assert_equal(rc, True, "ERR: Config PCs Route Failed")

    def test_07_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_08_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_09_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_10_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_11_verify_guest_login_status(self):
        self.guesttest.verify_user_info_correct_status_page()

    def test_12_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


class Test09_RedirectHttpsWithDHCP(Test):
    uuid = "SOSAIOT-TC-56109"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('cus_trust', 'X4', username='guest')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_02_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_03_verify_guest_login_status(self):
        self.guesttest.verify_user_info_correct_status_page()

    def test_04_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()

    def test_05_delete_dynamic_entry_to_X4(self):
        ret1 = dhcpserver_api.delete_dhcp_server_scope_v4(scope='dynamic', p1='192.168.4.10', p2='192.168.4.20')
        Assertion.assert_equal(ret1, True, "ERR: delete dynamic entries failed")

    def test_06_change_ip_to_static(self):
        rc = False
        PC4_host.send_command("killall dhclient")
        PC4_host.send_command("ifconfig eth1 0.0.0.0")
        output = PC4_host.send_commands(["ifconfig eth1 192.168.4.30 netmask 255.255.255.0",
                                         "ifconfig eth1"])
        logger.info(f"configure ip result is {output}")
        m = re.search(r'inet (192\.168\.4\.30)', output, re.I)
        if m:
            logger.info("PC4 eth1 successfully set ip address {}".format(m.group(1)))
            Parameter.pc4eth1_ip = m.group(1)
            rc = True
        else:
            logger.info("failed to set ip address for PC4 eth1")
        Assertion.assert_equal(rc, True, "ERR: failed to set ip address for PC4 eth1")

    def test_07_add_route_to_pc4(self):
        cmds = [f'route add -host {Parameter.https_server_ip} gw {Parameter.X4_IP}',
                f'route add -host 10.103.202.200 gw {Parameter.X4_IP}',
                f'route add -host 172.17.1.10 gw {Parameter.X4_IP}',
                f'route add -host 192.168.2.20 gw {Parameter.X4_IP}',
                'ip -4 r']
        output = PC4_host.send_commands(cmds)
        res = True if (f'{Parameter.https_server_ip} via {Parameter.X4_IP}' in output
                       and f'10.103.202.200 via {Parameter.X4_IP}' in output
                       and f'172.17.1.10 via {Parameter.X4_IP}' in output
                       and f'192.168.2.20 via {Parameter.X4_IP}' in output) else False
        Assertion.assert_equal(res, True, "ERR: ERR: Config PCs Route Failed")
