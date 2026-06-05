from definition.settings import *
from definition.utils import *


#  Verify that the maximum items of Split DNS entries is 32
class TestSplitDNS_TC067(Test):
    uuid = "SOSAIOT-TC-51764"
    description = show_testcase_info(
        TESTPLAN, '067', description=True)['title']
    res_for_tc65 = ContextVar('res_for_tc65')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '067')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_dns_cache(self):
        dns_setting = {
            'enforce_all_dns_requests': False,
            'dns_cache': False,
        }
        rc = dnsproxyapi.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: enforce_all_dns_requests failed.")

    def test_02_add_split_DNS(self):
        rc = True
        for i in range(1,33):
            split_dns_dict = {
                'domain': str(i)+ '.baidu.com',
                'ipv4': {
                    'primary': '13.13.1.100',
                    'secondary': Parameter.X1_GW,
                    'tertiary': Parameter.REM_X3_GW,
                },
                'local_interface': 'X2',
            }
            rc &= splitdnsapi.add_split_dns(**split_dns_dict)
        self.res_for_tc65.set(rc)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_03_add_split_DNS(self):
        split_dns_dict = {
            'domain': 'pc1.baidu.com',
            'ipv4': {
                'primary': '13.13.1.100',
            },
            'local_interface': 'X2',
        }
        rc = splitdnsapi.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, False, "ERR: add split DNS entry failed.")

    def test_04_show_all_split_DNS(self):
        split_entries = splitdnsapi.show_dns_proxy_entries()
        max_count= len(split_entries["dns"]["split_entry"])
        logger.info(f"the maximum items of Split DNS entries is {str(max_count)}")
        Assertion.assert_equal(max_count, 32, "ERR: maximum items of Split DNS entries is not correct.")


# Add a Split DNS entry
class TestSplitDNS_TC065(Test):
    uuid = "SOSAIOT-TC-51761"
    description = show_testcase_info(
        TESTPLAN, '065', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '065')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_split_dns_proxy_function(self):
        res = TestSplitDNS_TC067().res_for_tc65.get()
        logger.info('Add a Split DNS entry: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Add a Split DNS entry failed")


# check TSR about split dns setting
class TestSplitDNS_TC095(Test):
    uuid = "SOSAIOT-TC-51771"
    description = show_testcase_info(
        TESTPLAN, '095', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '095')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_TSR(self):
        tsr = diagnosticapi.get_tsr_part('Network', 'Split DNS')
        logger.info(f"The split dns part in TSR is {tsr}")
        count = str(tsr).count("Entry")
        logger.info(f"The split dns count in TSR is {count}")
        Assertion.assert_equal(count, 32, "ERR: check Split DNS entries in tsr failed.")


#Reboot test for split DNS function (configure multiple split DNS servers and maximum split DNS entries)
class TestSplitDNS_TC105(Test):
    uuid = "SOSAIOT-TC-51772"
    description = show_testcase_info(
        TESTPLAN, '105', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '105')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_reboot(self):
        rc = settingapi.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    def test_03_show_all_split_DNS(self):
        split_entries = splitdnsapi.show_dns_proxy_entries()
        max_count = len(split_entries["dns"]["split_entry"])
        logger.info(f"the maximum items of Split DNS entries is {str(max_count)}")
        Assertion.assert_equal(max_count, 32, "ERR: maximum items of Split DNS entries is not correct.")

    def test_04_delete_all_split_DNS(self):
        domain_list = []
        for i in range(1,33):
            domain_list.append(str(i)+ '.baidu.com')
        logger.info(domain_list)
        rc = splitdnsapi.delete_all_split_dns(domain_list=domain_list)
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")


# Non-VPN: Function test of split dns with local interface from LAN/DMZ/WAN/CUSTOM zone, dns proxy mode : 4to6
class TestSplitDNS_TC069(Test):
    uuid = "SOSAIOT-TC-51765"
    description = show_testcase_info(
        TESTPLAN, '069', description=True)['title']
    zone_name = 'LAN'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '069')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': self.zone_name,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        Assertion.assert_equal(rc1, True, "ERR: Config X1 to static failed")

    def test_02_add_dns_proxy_policy(self):
        dns_proxy_4to6 = {
            "from": self.zone_name,
            "source": {"address":{"any":True}},
            "name": "dns_proxy_4_to_6",
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dnspolicyapi.add_dns_proxy_policy(**dns_proxy_4to6)
        Assertion.assert_equal(rc, True, "ERR: Add dns proxy failed.")

    def test_03_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv6': {
                'primary': Parameter.X1_GW_IPV6,
            },
            'local_interface': 'X1',
        }
        rc = splitdnsapi.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_04_dns_query_and_check_packet(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)
        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC69}')
        logger.info(f"dns query result is {digres}")

        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)

        expectpkt1 = (Parameter.X3_GW, Parameter.X3_IP, Parameter.QUERY_DOMAIN_TC69, 'Domain Name System (query)')
        expectpkt2 = (Parameter.X1_GW_IPV6, Parameter.QUERY_DOMAIN_TC69, 'Domain Name System (query)')
        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        Assertion.assert_equal(checkres1&checkres2, True, "ERR: check packet failed")

    def test_05_export_exp_verify_tc110(self):
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_06_delete_dns_proxy_policy(self):
        uuid = dnspolicyapi.get_dns_policy_uuid("dns_proxy_4_to_6")
        rc = dnspolicyapi.del_dns_policy_uuid(uuid)
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")

    def test_07_config_interface_X3(self):
        self.zone_name = "DMZ"
        self.test_01_config_interface_X3()

    def test_08_add_dns_proxy_policy(self):
        self.zone_name = "DMZ"
        self.test_02_add_dns_proxy_policy()

    def test_09_dns_query_and_check_packet(self):
        self.test_04_dns_query_and_check_packet()

    def test_10_delete_dns_proxy_policy(self):
        self.test_06_delete_dns_proxy_policy()

    def test_11_add_custom_zone(self):
        base_dict = {
            'name': 'custom',
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        (res, msg) = zonesapi .add_zone_object(msg=True, **trusted_dict)
        if res is False:
            res = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(res, True, "ERR: add custom zone failed")

    def test_12_config_interface_X3(self):
        self.zone_name = "custom"
        self.test_01_config_interface_X3()

    def test_13_add_dns_proxy_policy(self):
        self.zone_name = "custom"
        self.test_02_add_dns_proxy_policy()

    def test_14_dns_query_and_check_packet(self):
        self.test_04_dns_query_and_check_packet()

    def test_15_delete_dns_proxy_policy(self):
        self.test_06_delete_dns_proxy_policy()

    def test_16_delete_split_DNS(self):
        rc = splitdnsapi.delete_split_dns(domain='*.baidu.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")


#Non-VPN: Function test of split dns with local interface from LAN/DMZ/WAN/CUSTOM zone, dns proxy mode : 4to4
class TestSplitDNS_TC068(Test):
    uuid = "SOSAIOT-TC-51762"
    description = show_testcase_info(
        TESTPLAN, '068', description=True)['title']
    zone_name = "LAN"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '068')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': self.zone_name,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        Assertion.assert_equal(rc1, True, "ERR: Config X1 to static failed")

    def test_02_add_dns_proxy_policy(self):
        dns_proxy_4to4 = {
            "from": self.zone_name,
            "source": {"address": {"any": True}},
            "name": "dns_proxy_4_to_4",
            "proxy_mode": "ipv4-ipv4"
        }
        rc = dnspolicyapi.add_dns_proxy_policy(**dns_proxy_4to4)
        Assertion.assert_equal(rc, True, "ERR: Add dns proxy failed.")

    def test_03_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.X1_PC,
            },
            'local_interface': 'X1',
        }
        rc = splitdnsapi.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_04_dns_query_and_check_packet(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)
        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC68}')
        logger.info(f"dns query result is {digres}")
        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)
        expectpkt1 = (Parameter.X3_GW, Parameter.X3_IP, Parameter.QUERY_DOMAIN_TC68, 'Domain Name System (query)')
        expectpkt2 = (Parameter.X1_IP,Parameter.X1_PC, Parameter.QUERY_DOMAIN_TC68, 'Domain Name System (query)')
        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        Assertion.assert_equal(checkres1 & checkres2, True, "ERR: check packet failed")

    def test_05_delete_dns_proxy_policy(self):
        uuid = dnspolicyapi.get_dns_policy_uuid("dns_proxy_4_to_4")
        rc = dnspolicyapi.del_dns_policy_uuid(uuid)
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")

    def test_06_config_interface_X3(self):
        self.zone_name = "DMZ"
        self.test_01_config_interface_X3()

    def test_07_add_dns_proxy_policy(self):
        self.zone_name = "DMZ"
        self.test_02_add_dns_proxy_policy()

    def test_08_dns_query_and_check_packet(self):
        self.test_04_dns_query_and_check_packet()

    def test_09_delete_dns_proxy_policy(self):
        self.test_05_delete_dns_proxy_policy()

    def test_10_config_interface_X3(self):
        self.zone_name = "custom"
        self.test_01_config_interface_X3()

    def test_12_add_dns_proxy_policy(self):
        self.zone_name = "custom"
        self.test_02_add_dns_proxy_policy()

    def test_12_dns_query_and_check_packet(self):
        self.test_04_dns_query_and_check_packet()


# Split DNS proxy : function test with enforce DNS Proxy option enabled.
class TestSplitDNS_TC079(Test):
    uuid = "SOSAIOT-TC-51763"
    description = show_testcase_info(
        TESTPLAN, '079', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '049')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enforce_all_dns_requests(self):
        dns_setting = {
            'enforce_all_dns_requests': True,
            'dns_cache': False,
        }
        rc = dnsproxyapi.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: enforce_all_dns_requests failed.")

    @repeat_method(5)
    def test_03_dns_query_and_check_packet(self):
        rtres = PC3_login.send_command(f"route add -net 8.8.8.0/24 gw {Parameter.X3_IP} dev eth2")
        logger.info(f"add route result is {rtres}")
        fw_packet_monitor_clear_start(pkgmonitorapi)
        digres = PC3_login.send_command(f'dig @8.8.8.8 {Parameter.QUERY_DOMAIN_TC79}')
        logger.info(f"dns query result is {digres}")
        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)
        expectpkt1 = (Parameter.X3_GW, '8.8.8.8', Parameter.QUERY_DOMAIN_TC79, 'Domain Name System (query)')
        expectpkt2 = (Parameter.X1_IP,Parameter.X1_PC, Parameter.QUERY_DOMAIN_TC79, 'Domain Name System (query)')
        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        Assertion.assert_equal(checkres1 & checkres2, True, "ERR: check packet failed")

    def test_04_delete_dns_proxy_policy(self):
        TestSplitDNS_TC068().test_05_delete_dns_proxy_policy()

    def test_05_delete_split_DNS(self):
        TestSplitDNS_TC069().test_16_delete_split_DNS()

    def test_06_dns_query_and_check_packet(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)
        digres = PC3_login.send_command(f'dig @8.8.8.8 {Parameter.QUERY_DOMAIN_TC79}')
        logger.info(f"dns query result is {digres}")
        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)
        expectpkt1 = (Parameter.X3_GW,'8.8.8.8', Parameter.QUERY_DOMAIN_TC79, 'Domain Name System (query)')
        expectpkt2 = (Parameter.X1_IP,'8.8.8.8', Parameter.QUERY_DOMAIN_TC79, 'Domain Name System (query)')
        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        Assertion.assert_equal(checkres1 & checkres2, True, "ERR: check packet failed")

    def test_07_config_interface_X3(self):
        self.zone_name = "LAN"
        TestSplitDNS_TC069().test_01_config_interface_X3()


# site to site VPN: Function test of split dns with local interface from LAN/DMZ/WAN/CUSTOM zone, dns proxy mode : 4to4
class TestSplitDNS_TC070(Test):
    uuid = "SOSAIOT-TC-51766"
    description = show_testcase_info(
        TESTPLAN, '070', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '070')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_s2s_vpn(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = vpnapi.add_vpn_policy(**local_vpn_dict)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc &= rmtvpnapi.add_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")

    def test_02_add_dns_proxy_policy(self):
        dns_proxy_s2s = {
            "from": "LAN",
            "source": {"address":{"any":True}},
            "name": "dns_proxy_s2s_vpn",
            "proxy_mode": "ipv4-ipv4"
        }
        rc = dnspolicyapi.add_dns_proxy_policy(**dns_proxy_s2s)
        Assertion.assert_equal(rc, True, "ERR: Add dns proxy failed.")

    def test_03_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.REM_X3_GW,
            },
            'local_interface': 'X3',
        }
        rc = splitdnsapi.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_04_add_acl(self):
        rc = aclapi.add_ipv4_access_rule(**acl_dict)
        rc &= rmtaclapi.add_ipv4_access_rule(**acl_dict)
        Assertion.assert_equal(rc, True, 'ERR: add acl allow vpn to lan ipv4 failed!')

    @repeat_method(5)
    def test_05_dns_query_and_check_packet(self):
        cmds = [f"route add -net 13.13.1.0/24 gw {Parameter.REM_X3_IP} dev eth2",
                "route del default",
                "route del default",
                f"route add default gw {Parameter.REM_X3_IP} dev eth2","route -4"]
        rtres = PC4_login.send_commands(cmds)
        logger.info(f"add route result is {rtres}")

        fw_packet_monitor_clear_start(pkgmonitorapi)
        fw_packet_monitor_clear_start(rmtpkgmonitorapi)

        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC70}')
        logger.info(f"dns query result is {digres}")

        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)
        expectpkt1 = (Parameter.X3_GW, Parameter.X3_IP, Parameter.QUERY_DOMAIN_TC70,"Domain Name System (query)")
        checkres1 = check_packets(filteredpackets, expectpkt1)

        filteredpackets2 = fw_packet_monitor_stop_export(rmtpkgmonitorapi, PC1_login)
        expectpkt2 = (Parameter.X3_IP, Parameter.REM_X3_GW, Parameter.QUERY_DOMAIN_TC70, "Domain Name System (query)")
        checkres2 = check_packets(filteredpackets2, expectpkt2)
        Assertion.assert_equal(checkres1&checkres2, True, "ERR: check packet failed")

    def test_06_delete_split_DNS(self):
        rc = splitdnsapi.delete_split_dns(domain='*.baidu.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")

    def test_07_delete_s2s_vpn(self):
        rc = vpnapi.del_s2svpn_policy(name='local_vpn_1')
        rc &= rmtvpnapi.del_s2svpn_policy(name='remote_vpn_1')
        Assertion.assert_equal(rc, True, "ERR: delete vpn policies failed")


# nunbered tunnel VPN: Function test of split dns with nunbered tunnel VPN, dns proxy mode : 4to4
class TestSplitDNS_TC072(Test):
    uuid = "SOSAIOT-TC-51767"
    description = show_testcase_info(
        TESTPLAN, '072', description=True)['title']
    res_for_tc76 = ContextVar('res_for_tc76')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '072')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_tunnel_vpn(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = vpnapi.add_vpn_policy(**Lvpn)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = rmtvpnapi.add_vpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_add_Tunnel_interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] = Parameter.VPN_IF_IP_LOCAL
        ref2["ip"] = Parameter.VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
        rc = interfaceapi.add_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Add Remote Vpn Tunnel Interface'))
        rc &= rmtinterfaceapi.add_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

    def test_03_add_route_policy(self):
        rc = routeapi.add_route_policy(**route_policy_dict)
        rc &= rmtrouteapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")

    def test_04_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.REM_X3_GW,
            },
            'local_interface': 'Ni',
        }
        rc,msg = splitdnsapi.add_split_dns(msg=True, **split_dns_dict)
        if rc is False:
            rc = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_05_dns_query_and_check_packet(self):
        rtres = PC4_login.send_commands([f"route add -net 72.1.1.0/24 gw {Parameter.REM_X3_IP} dev eth2", "route -4"])
        logger.info(f"add route result is {rtres}")

        fw_packet_monitor_clear_start(pkgmonitorapi)

        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC72}')
        logger.info(f"dns query result is {digres}")

        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)

        expectpkt1 = (Parameter.X3_GW, Parameter.X3_IP, Parameter.QUERY_DOMAIN_TC72,"Domain Name System (query)")
        expectpkt2 = (Parameter.VPN_IF_IP_LOCAL, Parameter.REM_X3_GW,Parameter.QUERY_DOMAIN_TC72, "Domain Name System (query)")

        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        self.res_for_tc76.set(checkres1&checkres2)
        Assertion.assert_equal(checkres1&checkres2, True, "ERR: check packet failed")


#Split DNS Proxy function when local interface is numbered tunnel interface.
class TestSplitDNS_TC076(Test):
    uuid = "SOSAIOT-TC-51768"
    description = show_testcase_info(
        TESTPLAN, '076', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '076')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_split_dns_proxy_function(self):
        res = TestSplitDNS_TC072().res_for_tc76.get()
        logger.info(
            'Verify Split DNS Proxy function when local interface is numbered tunnel interface: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: check Split DNS Proxy failed")


# Split DNS proxy: function test when local interface is numbered tunnel interface and modify the tunnel interface's IP address.
class TestSplitDNS_TC077(Test):
    uuid = "SOSAIOT-TC-51769"
    description = show_testcase_info(
        TESTPLAN, '077', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '077')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_Tunnel_interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] = Parameter.VPN_IF_IP_LOCAL_MODIFY
        ref2["ip"] = Parameter.VPN_IF_IP_REMOTE_MODIFY
        logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
        rc = interfaceapi.config_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Add Remote Vpn Tunnel Interface'))
        rc &= rmtinterfaceapi.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

    def test_03_dns_query_and_check_packet(self):
        rtres = PC4_login.send_commands([f"route add -net 72.2.1.0/24 gw {Parameter.REM_X3_IP} dev eth2", "route -4"])
        logger.info(f"add route result is {rtres}")

        fw_packet_monitor_clear_start(pkgmonitorapi)

        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC77}')
        logger.info(f"dns query result is {digres}")

        filteredpackets = fw_packet_monitor_stop_export(pkgmonitorapi, PC1_login)

        expectpkt1 = (Parameter.X3_GW, Parameter.X3_IP, Parameter.QUERY_DOMAIN_TC77,"Domain Name System (query)")
        expectpkt2 = (Parameter.VPN_IF_IP_LOCAL_MODIFY, Parameter.REM_X3_GW,"out:Ni",Parameter.QUERY_DOMAIN_TC77, "Domain Name System (query)")

        checkres1 = check_packets(filteredpackets, expectpkt1)
        checkres2 = check_packets(filteredpackets, expectpkt2)
        Assertion.assert_equal(checkres1&checkres2, True, "ERR: check packet failed")


# Test option manual TTL setting for split DNS entry
class TestSplitDNS_TC094(Test):
    uuid = "SOSAIOT-TC-51770"
    description = show_testcase_info(
        TESTPLAN, '094', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '094')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.REM_X3_GW,
                # 'secondary': Parameter.X1_GW_IPV6,
            },
            'local_interface': 'Ni',
            'manual_ttl': 1234
        }
        rc,msg = splitdnsapi.edit_split_dns(msg=True, **split_dns_dict)
        if rc is False:
            rc = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    @repeat_method(5)
    def test_03_dns_query_and_check_packet(self):
        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC94}')
        logger.info(f"dns query result is {digres}")
        check_list = ["pc5.baidu.com.", "1234", "192.16.2.140"]
        checkres = [x in str(digres) for x in check_list]
        logger.info(f'check result: {checkres}')
        flag = True if all(checkres) else False
        Assertion.assert_equal(flag, True, "ERR: check ttl failed.")


# prefs export and import about split DNS
class TestSplitDNS_TC110(Test):
    uuid = "SOSAIOT-TC-51773"
    description = show_testcase_info(
        TESTPLAN, '110', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_import_exp_verify_tc25(self):
        res = settingapi.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_03_dns_query_and_check_packet(self):
        digres = PC3_login.send_command(f'dig @{Parameter.X3_IP} {Parameter.QUERY_DOMAIN_TC69}')
        logger.info(f"dns query result is {digres}")
        check_list = ["pc1.baidu.com.",  "192.16.2.100"]
        checkres = [x in str(digres) for x in check_list]
        logger.info(f'check result: {checkres}')
        flag = True if all(checkres) else False
        Assertion.assert_equal(flag, True, "ERR: check ttl failed.")
