from settings import *
import os
from utils import *
import time
import datetime


# Expected: Import certificate can be audit successfully
class TestAudit_TC01(Test):
    uuid = "SOSAIOT-TC-55234"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_cert(self):
        global cert_name
        cert_name = 'dovecot_1k'
        clear_log_message()
        ret = cert_api.import_cert_local(
            cert_path='@' + CERT_PATH,
            name=cert_name,
            password='password')
        Assertion.assert_equal(
            ret, True, "ERR: Import SSL Certificate into Firewall failed.")

    def test_02_verify_syslog_on_PC1(self):
        with open('/var/log/messages', 'r', encoding='gb2312', errors='ignore') as file:
            syslog = file.read()
        logger.info(syslog)
        rc = check_result(
            check_list=check_info_dict['tc1'],
            output=syslog,
            mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_audit_log(self):
        rc = verify_result(1, 'audit', ['Import 3rd Cert'])
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_04_verify_log(self):
        rc = verify_result(1, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_05_del_cert(self):
        rc = cert_api.delete_local_cert(cert_name)
        Assertion.assert_equal(rc, True, "ERR: delete SSL Certificate failed.")


# Expected: Configure SNMP>General Settings can be audit successfully
class TestAudit_TC02(Test):
    uuid = "SOSAIOT-TC-55235"
    description = show_testcase_info(TESTPLAN, '02', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_snmp_general(self):
        snmp_new_dict = {
            "snmp": {
                "enable": True,
                "system_name": "test",
                "get_community_name": "public",
                "trap_community_name": "public",
                "host_1": PC2_ETH1_IP,
                "host_2": "1.1.1.1",
                "host_3": "2.2.2.2",
                "host_4": "3.3.3.3",
                "system_contact": "test",
                "system_location": "test",
            }
        }
        clear_log_message()
        ret = snmp_api.configure_snmp(**snmp_new_dict)
        Assertion.assert_equal(ret, True, "ERR: Config SNMP failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(2, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(2, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'System Name',
            'System Location',
            'System Contact',
            'Host 2',
            'Host 3',
            'Host 4']
        rc = verify_result(2, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(2, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_restore_snmp(self):
        rc = snmp_api.configure_snmp(**snmp_dict)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')


# Expected: Configure LAN static can be audit successfully
class TestAudit_TC03(Test):
    uuid = "SOSAIOT-TC-55236"
    description = show_testcase_info(TESTPLAN, '03', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_LAN_zone_static_IP(self):
        global x3_static_dict
        x3_static_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '1.1.1.1',
        }
        clear_log_message()
        ret = interface_api.config_interface(**x3_static_dict)
        Assertion.assert_equal(ret, True, "ERR: Config X3 failed.")

    def test_02_verify_syslog_on_PC1(self):
        time.sleep(3)
        rc = verify_result(3, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        time.sleep(3)
        rc = verify_result(3, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'X3.*?LAN/DMZ/WLAN IP Address.*?0.0.0.0.*?1.1.1.1',
            'X3.*?Interface zone.*?LAN']
        rc = verify_result(3, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        time.sleep(3)
        rc = verify_result(3, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_restore_X3_unassign(self):
        ret = interface_api.unassign_interface(interface='X3')
        Assertion.assert_equal(ret, True, "ERR: Config X3 unassigned failed.")


# Expected: Add a route policy can be audit successfully
class TestAudit_TC04(Test):
    uuid = "SOSAIOT-TC-55237"
    description = show_testcase_info(TESTPLAN, '04', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_standard_route(self):
        route_dict = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": {"any": True},
                        'destination': {'any': True},
                        'service': {'group': 'Ping'},
                        'gateway': {'name': 'X2 IP'},
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {"auto": True},
                        "name": "route_policy_tc4",
                        "type": "standard",
                        "priority": 1,
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                    }
                }
            ]
        }
        clear_log_message()
        ret = route_api.add_route_policy(**route_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Add custom route policy failed.")

    def test_02_verify_syslog_on_PC1(self):
        ret = verify_result(4, 'syslog')
        Assertion.assert_equal(ret, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(4, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'Policy Name',
            'The Interface for the route policy',
            'The Gateway for the route policy',
            'The associated service for the route policy']
        rc = verify_result(4, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(4, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_delete_route(self):
        rc = route_api.del_route_policy_by_name('route_policy_tc4')
        Assertion.assert_equal(rc, True, 'ERR: Delete route policy failed!')


# Expected: Add a dhcp dynamic server scope can be audit successfully
class TestAudit_TC05(Test):
    uuid = "SOSAIOT-TC-55238"
    description = show_testcase_info(TESTPLAN, '05', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_DHCP_Server_Scope(self):
        dynamic_entry1_dict = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "14.1.1.10",
                                "to": "14.1.1.167",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "14.1.1.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {"server": {"inherit": True}}
                            }
                        ]
                    }
                }
            }
        }
        clear_log_message()
        ret = dhcp_api.add_dhcp_server_scope_dynamic(**dynamic_entry1_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Add DHCP server dynamic scope failed")

    def test_02_verify_syslog_on_PC1(self):
        ret = verify_result(5, 'syslog')
        Assertion.assert_equal(ret, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(5, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['DHCP Dynamic Ranges']
        rc = verify_result(5, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(5, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_Delete_DHCP_Scope(self):
        ret = dhcp_api.delete_dhcp_server_scope_v4(
            scope='dynamic', p1='14.1.1.10', p2='14.1.1.167')
        Assertion.assert_equal(ret, True, "ERR: Delete DHCP Scope failed")



# Expected: Configure wireless settings can be audit successfully
# @unittest.skipIf('W' not in Parameter.platform,
#                  'This platform cannot support wireless settings.')
class TestAudit_TC06(Test):
    uuid = "SOSAIOT-TC-55239"
    description = show_testcase_info(TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # case not support G8, API endpoint is incomplete.
    # def test_01_config_Wireless_Settings(self):
    #     wireless_dict = {
    #         "wireless": {
    #             "radio_role": {
    #                 "access_point": {
    #                     "aggregation": True,
    #                     "channel": {
    #                         "primary": "auto",
    #                         "secondary": "auto"
    #                     },
    #                     "country_code": "United States-US",
    #                     "enable": True,
    #                     "radio": {
    #                         "band": "auto",
    #                         "mode": {
    #                             "ngb_mixed": True
    #                         }
    #                     },
    #                     "schedule": {
    #                         "always_on": True
    #                     },
    #                     "short_guard_interval": True,
    #                     "ssid": "sonicwall_test",
    #                     "virtual_access_point": {
    #                         "group": ""
    #                     },
    #                     "wds": False
    #                 }
    #             }
    #         }
    #     }
    #     clear_log_message()
    #     rc = wireless_api.wireless_settings(**wireless_dict)
    #     Assertion.assert_equal(
    #         rc, True, "ERR: Config internal wireless-settings failed.")

    # def test_02_verify_syslog_on_PC1(self):
    #     rc = verify_result(6, 'syslog')
    #     Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    # def test_03_verify_snmp(self):
    #     rc = verify_result(6, 'snmp')
    #     Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    # def test_04_verify_audit_log(self):
    #     check = ['WLAN Ssid', 'Enable WLAN']
    #     rc = verify_result(6, 'audit', check)
    #     Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    # def test_05_verify_log(self):
    #     rc = verify_result(6, 'log')
    #     Assertion.assert_equal(rc, True, "ERR: check log failed")

    # def test_06_restore_wireless(self):
    #     wireless_restore_dict = {
    #         "wireless": {
    #             "radio_role": {
    #                 "access_point": {
    #                     "aggregation": True,
    #                     "channel": {
    #                         "primary": "auto",
    #                         "secondary": "auto"
    #                     },
    #                     "country_code": "United States-US",
    #                     "enable": False,
    #                     "radio": {
    #                         "band": "auto",
    #                         "mode": {
    #                             "ngb_mixed": True
    #                         }
    #                     },
    #                     "short_guard_interval": True,
    #                     "ssid": "sonicwall",
    #                     "virtual_access_point": {
    #                         "group": ""
    #                     },
    #                     "wds": False
    #                 }
    #             }
    #         }
    #     }
    #     rc = wireless_api.wireless_settings(**wireless_restore_dict)
    #     Assertion.assert_equal(
    #         rc, True, "ERR: Restore internal wireless-settings failed.")


# Expected: Configure AP settings can be audit successfully
class TestAudit_TC07(Test):
    uuid = "SOSAIOT-TC-55240"
    description = show_testcase_info(TESTPLAN, '07', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_Access_Points_Settings(self):
        sonicwave_dict = {
            "sonicpoint": {
                "profile": [
                    {
                        "wave2": {
                            "name_prefix": "SonicWave"
                        },
                        "radio_5000mhz": {
                            "ssid": "sonicwall_test",
                            "short_guard_interval": True,
                            "aggregation": True}
                    }]
            }
        }
        clear_log_message()
        rc = ap_api.config_sonicpoint_profile(
            name='SonicWave', **sonicwave_dict)
        Assertion.assert_equal(rc, True, "ERR: Config access point failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(7, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(7, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['SonicPointN SSID', "Modified 'SonicPointN name' "]
        rc = verify_result(7, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(7, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")


# Expected: Add a virtual access point can be audit successfully
class TestAudit_TC08(Test):
    uuid = "SOSAIOT-TC-55241"
    description = show_testcase_info(TESTPLAN, '08', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_Virtual_Access_Points(self):
        global vap_dict
        vap_dict = {
            'name': 'test',
            'ssid': 'sonicwall'
        }
        clear_log_message()
        rc = vap_api.add_VAP_Object(**vap_dict)
        Assertion.assert_equal(
            rc, True, "ERR: add Virtual Access Point failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(8, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(8, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['Vap Object']
        rc = verify_result(8, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(8, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_del_vap(self):
        rc = vap_api.del_VAP_Object(vap_dict['name'])
        Assertion.assert_equal(
            rc, True, "ERR: Delete Virtual Access Point failed.")


# Expected: Edit SSLVPN client settings can be audit successfully
class TestAudit_TC09(Test):
    uuid = "SOSAIOT-TC-55242"
    description = show_testcase_info(TESTPLAN, '09', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '09')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Edit_SSLVPN_Client_Settings(self):
        ssl_vpn_dict = {
            'ipv4_network_address_zone': 'SSLVPN',
            'ipv4_network_address_name': 'test_09',
        }
        clear_log_message()
        ret = clientset_api.edit_default_device_profile(**ssl_vpn_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Edit SSLVPN Client Settings failed")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(9, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(9, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['Default Device Profile']
        rc = verify_result(8, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(9, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")


# Expected: Add a portal bookmark can be audit successfully
class TestAudit_TC10(Test):
    uuid = "SOSAIOT-TC-55243"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_snmp_general(self):
        global virtualset_dict
        virtualset_dict = {
            'name': 'RDP1',
            'host': '10.5.252.115',
            'service_type': 'rdp',
            'redirect_clipboard': True,
            'redirect_audio': False,
            'auto_reconnection': True,
            'desktop_background': False,
            'window_drag': False,
            'animation': False,
            'screen_size': 'full-screen',
            'colors': '16bit',
            'application_path': '',
            'start_in_folder': '',
            'automatic_login': {},
            'display_on_mobile': False
        }
        clear_log_message()
        ret = virtualset_api.configure_bookmark(**virtualset_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Add a portal bookmark with service RDP failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(10, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(10, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'Bookmark Service Name',
            'RDP Server IP',
            'RDP Service Type',
            'Display connection bar',
            'Redirect clipboard',
            'Auto reconnection']
        rc = verify_result(10, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(10, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_del_bookmark(self):
        rc = virtualset_api.delete_bookmark(**virtualset_dict)
        Assertion.assert_equal(
            rc, True, 'ERR: Delete a portal bookmark failed!')


# Expected: Add a s2s vpn can be audit successfully
class TestAudit_TC11(Test):
    uuid = "SOSAIOT-TC-55244"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_s2s_vpn(self):
        global local_s2svpn_dict
        local_s2svpn_dict = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'pri_gate': '2.2.2.2',
            'edit_auth': False,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '4.4.4.4',
            'peer_ike_id': '4.4.4.4',

            'edit_network': False,
            'local_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_vpn_net',
            'keep_alive': True,
        }
        clear_log_message()
        ret = vpn_api.add_vpn_policy(**local_s2svpn_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Add a Site to Site VPN policy failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(11, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(11, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'IPsec Name',
            'IPsec Gateway Address',
            'Type of VPN Policy',
            'Authentication Method',
            'Local Networks',
            'Destination Networks',
            'Local IKE ID',
            'Peer IKE ID',
            'Encryption Key',
            'Enable Keep Alive']
        rc = verify_result(11, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(11, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_del_bookmark(self):
        rc = vpn_api.del_s2svpn_policy(**local_s2svpn_dict)
        Assertion.assert_equal(
            rc, True, 'ERR: Delete a Site to Site VPN policy failed!')


# Expected: Delete vpn policies can be audit successfully
class TestAudit_TC12(Test):
    uuid = "SOSAIOT-TC-55245"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_two_s2s_vpn(self):
        global local_s2svpn_dict2
        local_s2svpn_dict2 = {
            'type': 'site_to_site',
            'name': 'localvpn2',
            'pri_gate': '3.3.3.3',
            'edit_auth': False,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',

            'peer_ike_type': 'ipv4',
            'local_ike_id': '5.5.5.5',
            'peer_ike_id': '5.5.5.5',

            'edit_network': False,
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_vpn_net',
            'keep_alive': True,
        }
        clear_log_message()
        rc = True
        for vpn in [local_s2svpn_dict, local_s2svpn_dict2]:
            rc &= vpn_api.add_vpn_policy(**vpn)
        Assertion.assert_equal(
            rc, True, "ERR: Add twp Site to Site VPN policies failed.")

    def test_02_delete_two_s2s_vpn(self):
        rc = True
        for vpn in [local_s2svpn_dict, local_s2svpn_dict2]:
            rc &= vpn_api.del_s2svpn_policy(**vpn)
        Assertion.assert_equal(
            rc, True, 'ERR: Delete two Site to Site VPN policies failed!')

    def test_03_verify_syslog_on_PC1(self):
        rc = verify_result(12, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_04_verify_snmp(self):
        rc = verify_result(12, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_verify_audit_log(self):
        check = [
            "Deleted 'IPsec Name'.*?localvpn",
            "Deleted 'IPsec Name'.*?localvpn2"]
        rc = verify_result(12, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_06_verify_log(self):
        rc = verify_result(12, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")


# Expected: Add ldap server can be audit successfully
class TestAudit_TC13(Test):
    uuid = "SOSAIOT-TC-55246"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        global ldapserver_dict
        ldapserver_dict = {
            'role': 'primary',
            'host': '2.2.2.2',
            'enable': True,
            'port_num': 636,
            'use_tls': False,
            'timeout': True,
            'servertimeout': 10,
            'overalloperationtimeout': 6,
            'send_start_tls_request': True,
            'bind': 'distinguished_name',
            'distinguished_name': 'test',
            'bind_password': Params.G_NEW_PASSWORD,
            'referred_bind_with_account': 'other-servers',
            'primary_domain': 'testdomain1.com',
            'users_tree': ['testdomain1.com/users'],
            'user_groups_tree': ['testdomain1.com/groups'],
            'directory': True,
            'schema': 'microsoft-active-directory/network-information-service'
        }
        clear_log_message()
        ret = ldap_api.add_ldap_server(**ldapserver_dict)
        Assertion.assert_equal(ret, True, "ERR: Add a LDAP server failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(13, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(13, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = [
            'LDAP user groups tree',
            "Added 'LDAP user groups tree'",
            'LDAP users tree',
            "Added 'LDAP users tree'",
            'LDAP timeout',
            'Use TLS \\(SSL\\)',
            'LDAP server bind  password',
            'LDAP server login type',
            'LDAP server name/address',
            "Added 'LDAP server name/address",
        ]
        rc = verify_result(13, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(13, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_del_LDAP_server(self):
        rc = ldap_api.del_ldap_server(ldapserver_dict['host'])
        Assertion.assert_equal(rc, True, 'ERR: Delete LDAP server failed!')


# Expected: Modify user settings can be audit successfully
class TestAudit_TC14(Test):
    uuid = "SOSAIOT-TC-55247"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_user_settings(self):
        global user_settings_dict
        user_settings_dict = {
            "apply_password_constraints": False,
            "prune_on_expiry": False
        }
        clear_log_message()
        ret = usersettings_api.local_settings(**user_settings_dict)
        Assertion.assert_equal(ret, True, "ERR: Modify User Settings failed.")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(14, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(14, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['Apply password constraints', 'Prune Expired user accounts']
        rc = verify_result(14, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(14, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_restore_user_settings(self):
        user_settings_dict['apply_password_constraints'] = True
        user_settings_dict['prune_on_expiry'] = True
        ret = usersettings_api.local_settings(**user_settings_dict)
        Assertion.assert_equal(ret, True, "ERR: Restore User Settings failed.")


# Expected: Modify Certificate re-signing Authority can be audit successfully
class TestAudit_TC15(Test):
    uuid = "SOSAIOT-TC-55248"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_cert(self):
        ret = cert_api.import_cert_local(
            cert_path='@' + CERT_PATH,
            name=cert_name,
            password='password')
        clear_log_message()
        Assertion.assert_equal(
            ret, True, "ERR: Import SSL Certificate into Firewall failed.")

    def test_02_modify_Client_SSL_Cert(self):
        global cert_dict
        cert_dict = {
            'certificate': cert_name
        }
        ret = ssl_cert_api.config_cert(**cert_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Modify Client SSL Certificate failed.")

    def test_03_verify_syslog_on_PC1(self):
        with open('/var/log/messages', 'r', encoding='gb2312', errors='ignore') as file:
            syslog = file.read()
        logger.info(syslog)
        rc = verify_result(15, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_04_verify_snmp(self):
        rc = verify_result(15, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_verify_audit_log(self):
        check = ['SSL proxy Ca cert']
        rc = verify_result(15, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_06_verify_log(self):
        rc = verify_result(15, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_07_restore_ssl_cert(self):
        cert_dict['certificate'] = '2048-bit'
        ret = ssl_cert_api.config_cert(**cert_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Restore Client SSL Certificate failed.")

    def test_08_del_cert(self):
        rc = cert_api.delete_local_cert(cert_name)
        Assertion.assert_equal(rc, True, "ERR: delete SSL Certificate failed.")


# Expected: Modify SSL Servers can be audit successfully
class TestAudit_TC16(Test):
    uuid = "SOSAIOT-TC-55249"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_cert(self):
        ret = cert_api.import_cert_local(
            cert_path='@' + CERT_PATH,
            name=cert_name,
            password='password')
        clear_log_message()
        Assertion.assert_equal(
            ret, True, "ERR: Import SSL Certificate into Firewall failed.")

    def test_02_modify_SSL_server(self):
        global ssl_server_dict
        ssl_server_dict = {
            'ssl_server': 'X1 IP',
            'certificate': cert_name,
            'cleartext': True,
        }
        ret = server_ssl_api.add_sslserver(**ssl_server_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Add a Serve_SSL Server failed.")

    def test_03_verify_syslog_on_PC1(self):
        rc = verify_result(16, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_04_verify_snmp(self):
        rc = verify_result(16, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_verify_audit_log(self):
        check = ['SSL server certs config']
        rc = verify_result(16, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_06_verify_log(self):
        rc = verify_result(16, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_07_del_SSL_server(self):
        ret = server_ssl_api.del_sslserver(**ssl_server_dict)
        Assertion.assert_equal(
            ret, True, "ERR: Delete Server SSL Certificate failed.")

    def test_08_del_cert(self):
        rc = cert_api.delete_local_cert(cert_name)
        Assertion.assert_equal(rc, True, "ERR: delete SSL Certificate failed.")


# Expected: Add a acl can be audit successfully
class TestAudit_TC17(Test):
    uuid = "SOSAIOT-TC-55250"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_IPv4_Access_Rule(self):
        global access_rules_dict
        access_rules_dict = {
            "name": "my_access_rule1",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "FTP"
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
        }
        clear_log_message()
        rc = access_rules_api.config_accessrule(**access_rules_dict)
        logger.info(rc)
        Assertion.assert_equal(
            rc, True, "ERR: add access rule from WAN to LAN failed")

    def test_02_verify_syslog_on_PC1(self):
        rc = verify_result(17, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_snmp(self):
        rc = verify_result(17, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_04_verify_audit_log(self):
        check = ['Firewall Access Rules']
        rc = verify_result(17, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_05_verify_log(self):
        rc = verify_result(17, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_06_del_policy(self):
        rc = access_rules_api.delete_accessrule_by_name(
            access_rules_dict['name'])
        logger.info(rc)
        Assertion.assert_equal(
            rc, True, "ERR: Delete access rule from WAN to LAN failed")


# Expected: Add a app control policy can be audit successfully
class TestAudit_TC18(Test):
    uuid = "SOSAIOT-TC-55251"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_match_obj(self):
        global match_obj_dict
        match_obj_dict = {
            "object_type": "application-signature-list",
            "name": "TC18_Application_List",
            "signature": [
                {'category': {'id': 74}, 'app': {'id': 1284}, 'sig': {'id': 5193}}
            ]
        }
        rc = match_object_api.config_matchobject(**match_obj_dict)
        clear_log_message()
        Assertion.assert_equal(rc, True, "ERR: Add a match object failed.")

    def test_02_add_app_control_policy(self):
        global apprule_dict
        apprule_dict = {
            "name": "TC18_App_Rule",
            "type": {"app_control": True},
            "source": {
                "address": {"any": True},
                "service": {"any": True}
            },
            "destination": {
                "address": {"any": True},
                "service": {"any": True}
            },
            "exclusion": {"address": {}},
            "match_object": {'included': 'TC18_Application_List', 'excluded': ''},
            "action_object": "Reset/Drop",
            "users": {
                "included": {"all": True},
                "excluded": {}
            },
            "schedule": {"always_on": True},
            "flow_reporting": False,
            "logging": True,
            "log": {'individual': False, 'redundancy': {'global': True}},
            "app_control_message_format": True,
            "zone": {'any': True}
        }
        rc = app_rule_api.add_apprule_object(**apprule_dict)
        Assertion.assert_equal(rc, True, "ERR: Add a APP rule failed.")

    def test_03_verify_syslog_on_PC1(self):
        rc = verify_result(18, 'syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_04_verify_snmp(self):
        rc = verify_result(18, 'snmp')
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_verify_audit_log(self):
        check = ['TC18_App_Rule', 'App Rules']
        rc = verify_result(18, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_06_verify_log(self):
        rc = verify_result(18, 'log')
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_07_del_mo_policy(self):
        rc = app_rule_api.delete_apprule_object_byname(apprule_dict['name'])
        rc &= match_object_api.del_match_object_by_name(match_obj_dict['name'])
        Assertion.assert_equal(
            rc, True, "ERR: Delete a APP rule and a match object failed.")


# Expected: Failed configuration can be audit successfully
class TestAudit_TC19(Test):
    uuid = "SOSAIOT-TC-55252"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']
    jira = 'GEN7-33277'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_cert(self):
        ret = cert_api.import_cert_local(
            cert_path='@' + CERT_PATH,
            name=cert_name,
            password='password')
        clear_log_message()
        Assertion.assert_equal(
            ret, True, "ERR: Import SSL Certificate into Firewall failed.")

    def test_02_import_same_cert(self):
        ret = cert_api.import_cert_local(
            cert_path='@' + CERT_PATH,
            name=cert_name,
            password='password')
        Assertion.assert_equal(
            ret, False, "ERR: The same cert can be loaded successfully.")

    def test_03_verify_audit_log(self):
        check = ['Import 3rd Cert.*?Failed']
        rc = verify_result(19, 'audit', check)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_04_del_cert(self):
        rc = cert_api.delete_local_cert(cert_name)
        Assertion.assert_equal(rc, True, "ERR: delete SSL Certificate failed.")


# Expected:  E-mail Audit Records Automation successfully
class TestAudit_TC20(Test):
    uuid = "SOSAIOT-TC-55253"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Cfg_Mail_Server(self):
        global mail_server_dict
        mail_server_dict = {
            'mail_server': '1.1.1.1',
            'mail_from': 'kelly@kelly.com',
        }
        res = log_auto_api.cfg_mail_server(**mail_server_dict)
        Assertion.assert_equal(res, True, "ERR: configiure mail server failed")

    def test_02_Cfg_Audit_Automation(self):
        global audit_auto_dict
        audit_auto_dict = {
            'audit': 'kelly@kelly.com',
            "send_audit": "daily",
            "email_format_audit": "plain_text",
            'hour': 10,
            'minute': 20
        }
        cur_time = datetime.datetime.now()
        audit_auto_dict['hour'] = cur_time.hour
        audit_auto_dict['minute'] = cur_time.minute + 3
        if audit_auto_dict['minute'] >= 60:
            audit_auto_dict['hour'] += 1
            audit_auto_dict['minute'] = audit_auto_dict['minute'] - 60
        res = log_auto_api.email_audit_settings(**audit_auto_dict)
        Assertion.assert_equal(
            res, True, "ERR: configiure audit automation failed")

    def test_03_Capture_SMTP_Packet(self):
        clearres = pkgmonitor_api.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))

        startres = pkgmonitor_api.start_capture()
        logger.info('start capture result:{}'.format(startres))

        time.sleep(200)
        stopres = pkgmonitor_api.stop_capture()
        logger.info('stop capture result:{}'.format(stopres))
        exportres = pkgmonitor_api.export_captured_packets()
        logger.info('packet result:{}'.format(exportres))
        checkres, packet = check_smpt_packet(
            Parameter.X1_IP, mail_server_dict['mail_server'], exportres)
        logger.info(packet)

        Assertion.assert_equal(checkres, True, "ERR: FW send Email fail")


# Expected:  Export Audit Records as CSV file successfully
class TestAudit_TC22(Test):
    uuid = "SOSAIOT-TC-55255"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_audit_to_csv_format(self):
        output = audit_log_api.export_audit_log_csv()
        time.sleep(10)
        res = False
        if re.search('192.168.168.169.*?admin.*?API', output):
            res = True
        Assertion.assert_equal(
            res, True, "ERR: Export Audit Records as CSV file failed")


# Expected:  Display Audit Records on Console successfully
class TestAudit_TC23(Test):
    uuid = "SOSAIOT-TC-55256"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_audit_records_on_console(self):
        flag = False
        cmds = ['show log audit view']
        (rc, output) = fw_console.do_cli_commands(cmds, 1)
        if not rc:
            logger.info(output)
        else:
            if re.search(r'Configuration Audit View', output, re.I):
                flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Show Audit Records via console Failed!")


# Expected:  Audit Records are inluded in TSR successfully
class TestAudit_TC25(Test):
    uuid = "SOSAIOT-TC-55258"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_tsr(self):
        diag_api.download_tsr()
        rc = False
        with os.popen('cat /tmp/techSupport', 'r') as file:
            tsr = file.read()
        if re.search('Configuration Audit_START', tsr):
            rc = True
        Assertion.assert_equal(
            rc, True, "ERR: check the Audit Records are inluded in TSR failed")


# Expected:  the records shoud be persist after reboot
class TestAudit_TC27(Test):
    uuid = "SOSAIOT-TC-86251"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_persistent_after_reboot(self):
        logger.info('Get audit log before reboot')
        output1 = audit_log_api.show_audit_records()

        reboot_res = os_obj.reboot_node()
        logger.info('Reboot FW result: {}'.format(reboot_res))

        res = False
        if reboot_res:
            logger.info('Get audit log after reboot')
            output2 = audit_log_api.show_audit_records()
            if output2 == output1:
                res = True & reboot_res

        Assertion.assert_equal(
            res, True, "ERR: Check audit log persistence fail after reboot")


# Expected:  Show Audit Records on CLI
class TestAudit_TC28(Test):
    uuid = "SOSAIOT-TC-55259"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_audit_records_in_cli(self):
        flag = False
        cmds = ['show log audit view']
        (rc, output) = fw_cli.do_cli_commands(cmds, 1)
        if not rc:
            logger.info(output)
        else:
            if re.search(r'Configuration Audit View', output, re.I):
                flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Show Audit Records in CLI Failed!")


# Expected:  Disable/Enable Configuration Auditing on diag page
class TestAudit_TC29(Test):
    uuid = "SOSAIOT-TC-55260"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_Config_Auditing_on_diag_page(self):
        put_json = {
            "log": {
                "audit": {
                    "enable": False,
                    "display_on_console": False,
                    "supplemental_changes": False}}}
        ret = audit_log_api.configure_audit_log(**put_json)
        try:
            output = audit_log_api.get_audit_log_config()
            logger.info(output)
            ret &= (output['log']['audit']['enable'] == False)
        except BaseException:
            logger.error("get config audit log config  failed")
        Assertion.assert_equal(
            ret, True, "ERR: Disable Config Auditing on diag page failed")

    def test_02_enable_Config_Auditing_on_diag_page(self):
        put_json = {
            "log": {
                "audit": {
                    "enable": True,
                    "display_on_console": False,
                    "supplemental_changes": False}}}
        ret = audit_log_api.configure_audit_log(**put_json)
        try:
            output = audit_log_api.get_audit_log_config()
            logger.info(output)
            ret &= (output['log']['audit']['enable'])
        except BaseException:
            logger.error("get config audit log config  failed")
        Assertion.assert_equal(
            ret, True, "ERR: Enable Config Auditing on diag page failed")
