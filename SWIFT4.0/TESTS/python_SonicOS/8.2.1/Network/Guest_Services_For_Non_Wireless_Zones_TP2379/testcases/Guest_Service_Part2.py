from definition.settings import *
from definition.guestservicestep import *


@paramunittest.parametrized(
    {'uuid': '1527009', 'zone': 'LAN', 'interface': 'X4'},
    {'uuid': '1527016', 'zone': 'DMZ', 'interface': 'X4'},
    {'uuid': '1527028', 'zone': 'cus_public', 'interface': 'X4'},
)
class Test01_ByPassAuthentication(Test):
    def setParameters(self, uuid, zone, interface):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_add_pc5_eth1_mac(self):
        self.guesttest.add_mac_ao(Parameter.PC5_ETH1_MAC)

    def test_04_verify_pc4_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_05_verify_pc5_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(pc_tag="pc5")

    def test_06_enable_zone_with_gs_pass_all_mac(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "bypass_guest_auth": {
                            "all": True
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_07_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_08_verify_pc4_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_09_verify_pc5_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(pc_tag="pc5")

    def test_10_enable_zone_with_gs_pass_pc5_mac(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "bypass_guest_auth": {
                            "name": "mac_ao_bypass"
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_11_verify_pc4_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_12_verify_pc5_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(pc_tag="pc5")

    def test_13_enable_zone_with_gs_pass_disabled(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "bypass_guest_auth": {}
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_14_verify_pc4_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_15_verify_pc5_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed(pc_tag="pc5")

    def test_16_delete_mac_bypass(self):
        self.guesttest.delete_mac_ao()


@paramunittest.parametrized(
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "deny_ao": "dns_ip_host"},
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "deny_ao": "dns_ip_range"},
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "deny_ao": "dns_ip_network"},
    {'uuid': '1527011', 'zone': 'LAN', 'interface': 'X2', "deny_ao": "dns_group"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "deny_ao": "dns_ip_host"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "deny_ao": "dns_ip_range"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "deny_ao": "dns_ip_network"},
    {'uuid': '1527017', 'zone': 'DMZ', 'interface': 'X3', "deny_ao": "dns_group"},
)
class Test02_DenyNetwork(Test):
    def setParameters(self, uuid, zone, interface, deny_ao):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.deny_ao = deny_ao
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(des='10.103.202.200')

    def test_04_enable_gs_with_deny_network(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "deny_networks": {
                            "name": self.deny_ao
                        }
                    }
                }
            ]
        }
        if "group" in self.deny_ao:
            payload = {
                "zones": [
                    {
                        "name": self.zone,
                        "guest_services": {
                            "enable": True,
                            "deny_networks": {
                                "group": self.deny_ao
                            }
                        }
                    }
                ]
            }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_08_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_09_verify_traffic_to_dns_failed(self):
        log_api.clear_log()
        self.guesttest.verify_pc_traffic_to_internet_failed(des='10.103.202.200')

    def test_10_verify_guest_service_deny_network_log(self):
        pattern = '"dst_ip": "10.103.202.200".*"user_name": "guest".*"message": "Guest Services drop traffic to deny network"'
        self.guesttest.verify_guest_user_login_success_log(pattern)

    def test_11_disable_deny_network(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "deny_networks": {}
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_12_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_13_verify_traffic_to_dns_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(des='10.103.202.200')

    def test_14_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


@paramunittest.parametrized(
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "passao": "dns_ip_host"},
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "passao": "dns_ip_range"},
    {'uuid': 'NonTC', 'zone': 'LAN', 'interface': 'X2', "passao": "dns_ip_network"},
    {'uuid': '1527012', 'zone': 'LAN', 'interface': 'X2', "passao": "dns_group"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "passao": "dns_ip_host"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "passao": "dns_ip_range"},
    {'uuid': 'NonTC', 'zone': 'DMZ', 'interface': 'X3', "passao": "dns_ip_network"},
    {'uuid': '1527018', 'zone': 'DMZ', 'interface': 'X3', "passao": "dns_group"},
    {'uuid': 'NonTC', 'zone': 'cus_trust', 'interface': 'X4', "passao": "dns_ip_host"},
    {'uuid': 'NonTC', 'zone': 'cus_trust', 'interface': 'X4', "passao": "dns_ip_range"},
    {'uuid': 'NonTC', 'zone': 'cus_trust', 'interface': 'X4', "passao": "dns_ip_network"},
    {'uuid': '1527024', 'zone': 'cus_trust', 'interface': 'X4', "passao": "dns_group"},
)
class Test03_PassNetwork(Test):
    def setParameters(self, uuid, zone, interface, passao):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.passao = passao
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_dns_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(des='10.103.202.200')

    def test_04_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_05_enable_gs_with_pass_network(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "pass_networks": {
                            "name": self.passao
                        }
                    }
                }
            ]
        }
        if "group" in self.passao:
            payload = {
                "zones": [
                    {
                        "name": self.zone,
                        "guest_services": {
                            "enable": True,
                            "pass_networks": {
                                "group": self.passao
                            }
                        }
                    }
                ]
            }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_06_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_07_verify_pc_traffic_to_dns_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(des='10.103.202.200')

    def test_08_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("redirect_success")

    def test_09_disable_pass_network(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "pass_networks": {}
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_10_verify_traffic_to_dns_denied(self):
        self.guesttest.verify_pc_traffic_to_internet_failed(des='10.103.202.200')


@paramunittest.parametrized(
    {'uuid': '1527053', 'zone': 'LAN', 'interface': 'X2'},
    {'uuid': '1527027', 'zone': 'cus_public', 'interface': 'X4'},
    {'uuid': '1527021', 'zone': 'cus_trust', 'interface': 'X4'},
)
class Test04_PostAuth(Test):
    def setParameters(self, uuid, zone, interface):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface, protocol='http')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc4_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_gs_with_post_auth(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "post_auth": "http://172.17.1.10"
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login", postauth=1)

    def test_08_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()

    def test_09_disable_post_auth(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "post_auth": ""
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_10_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_11_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


@paramunittest.parametrized(
    {'uuid': '1527052', 'zone': 'LAN', 'interface': 'X2'},
    {'uuid': '1527015', 'zone': 'DMZ', 'interface': 'X3'},
    {'uuid': '1527026', 'zone': 'cus_public', 'interface': 'X4'},
    {'uuid': '2019131', 'zone': 'LAN', 'interface': 'X2'},
)
class Test05_CustomAuthenticationPage(Test):
    def setParameters(self, uuid, zone, interface):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface, protocol='http')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc4_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_gs_with_custom_auth_url(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "custom_auth_page": {
                            "enable": True,
                            "footer": {
                                "url": "http://172.17.1.10"
                            },
                            "header": {
                                "url": "http://172.17.1.10"
                            }
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_07_verify_custom_authentication_url(self):
        self.guesttest.login_guest_user_from_pc("custom_auth_url")

    def test_08_enable_gs_with_custom_auth_text(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "custom_auth_page": {
                            "enable": True,
                            "footer": {
                                "text": "autotest_guest2"
                            },
                            "header": {
                                "text": "autotest_guest1"
                            }
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    @repeat_method(3)
    def test_09_verify_custom_authentication_text(self):
        self.guesttest.login_guest_user_from_pc("custom_auth_text")

    def test_10_disable_post_auth(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "custom_auth_page": {
                            "enable": False,
                            "footer": {},
                            "header": {}
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_11_verify_custom_authentication_text(self):
        self.guesttest.login_guest_user_from_pc("disable_custom_auth")

class Test06_RedirectAfterAuthentication(Test):
    uuid = "SOSAIOT-TC-56106"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('LAN', 'X2', protocol='http')

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

    def test_08_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


class Test07_ExportImportSettings(Test):
    uuid = "SOSAIOT-TC-56105"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('LAN', 'X2', protocol='http')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_04_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_05_export_exp(self):
        res = setting_api.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: Export Exp File Failed")

    def test_06_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_07_import_exp(self):
        res = setting_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: Import Exp File Failed")

    def test_08_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()


class Test08_EnableInterGuestCommunication(Test):
    uuid = "SOSAIOT-TC-56118"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('LAN', 'X4')
    guesttest1 = guestteststep('LAN', 'X2', username='localguest',password="S0nic@uto")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface_x4(self):
        self.guesttest.configure_interface()
    
    def test_03_configure_interface_x2(self):
        self.guesttest1.configure_interface()

    def test_04_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_05_enable_zone_with_guest_service(self):
        payload = {
            "zones": [
                {
                    "name": "LAN",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": True,
                        "inter_guest": False
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_06_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_07_verify_pc_traffic_to_internet_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed()

    def test_08_login_guest_user_from_pc4(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_09_login_guest_user_from_pc2(self):
        self.guesttest1.login_guest_user_from_pc("login")

    def test_10_verify_traffic_between_pc4_and_pc2_failed(self):
        self.guesttest.verify_pc_traffic_to_internet_failed(des=PC2_ETH1_IP)

    def test_11_enable_inter_guest_communication(self):
        payload = {
            "zones": [
                {
                    "name": "LAN",
                    "guest_services": {
                        "enable": True,
                        "inter_guest": True
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_12_verify_traffic_between_pc4_and_pc2_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed(des=PC2_ETH1_IP)

    def test_13_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()


class Test09_CheckTsrConfigure(Test):
    uuid = "SOSAIOT-TC-56104"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    guesttest = guestteststep('LAN', 'X2')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_enable_zone_with_guest_service(self):
        self.guesttest.enable_zone_with_guest_service()

    def test_04_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_05_get_tsr_for_lan_guest(self):
        out = False
        diag_api.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        lab1_match = re.search(r"#Network : Zones_START\n(.*)\n#Network : Zones_END", tsr_content, re.I | re.S | re.M)
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
            logger.info(f"tsr_part1 is {tsr_part1}")
            lab2_match = re.search(r'LAN\(LAN\)\s*-*\n(.*)\n-*\s*WAN\(WAN\)', tsr_part1, re.S | re.M)
            if lab2_match:
                tsr_part2 = lab2_match.group(1)
                logger.info(f"tsr_part2 is {tsr_part2}")
                pattern3 = "Enable Guest Services:\s+On"
                lab3_match = re.search(r'' + pattern3 + '', tsr_part2)
                if lab3_match:
                    out = True
        Assertion.assert_equal(out, True, "ERR: Guest enable status wrong in tsr")
