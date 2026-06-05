from definition.settings import *
from definition.utils import *


class TestIPHelper_TC01(Test):
    uuid = "SOSAIOT-TC-55085"
    description = "IP Helper - Enable/Disable IP Helper"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'IPHelper_TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_enable_ip_helper_from_CLI(self):
        output = iphelper_cli.enable_IPhelper()
        Assertion.assert_equal(output, True, "ERR: enable ip helper from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc01_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc01_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc01_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc01_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_ip_helper_configure(self):
        output = iphelper_cli.disable_IPhelper()
        Assertion.assert_equal(output, True, "ERR: init ip helper configure failed")


class TestIPHelper_TC03(Test):
    uuid = "SOSAIOT-TC-55086"
    description = "IP Helper - Add a Relay Protocol"
    relay_protocol_name = 'auto_pro_v4'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'IPHelper_TC03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_relay_protocol_from_CLI(self):
        protocol_v4 = {
            'name': self.relay_protocol_name,
            'port1': '30',
            'port2': '40',
        }
        output = iphelper_cli.add_relay_protocol(**protocol_v4)
        Assertion.assert_equal(output, True, "ERR: add relay protocol from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc02_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc02_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc02_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc02_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_relay_protocol_configure(self):
        output = iphelper_cli.del_relay_protocol(name=self.relay_protocol_name)
        Assertion.assert_equal(output, True, "ERR: init relay_protocol configure failed")


class TestIPHelper_TC06(Test):
    uuid = "SOSAIOT-TC-55087"
    description = "IP Helper - Add a policy"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'IPHelper_TC06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_relay_policy_from_CLI(self):
        output = iphelper_cli.add_policy(**relay_policy_dict)
        Assertion.assert_equal(output, True, "ERR: add relay policy from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc06_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc06_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc06_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc06_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestIPHelper_TC08(Test):
    uuid = "SOSAIOT-TC-55088"
    description = "IP Helper - Edit policies"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'IPHelper_TC08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_edit_relay_policy_from_CLI(self):
        org_policy = {
            'protocol': 'DHCP',
            'from': 'interface X0',
        }
        change_policy = {'to-new': 'name "X2 IP"'}
        output = iphelper_cli.edit_relay_policies(org_policy=org_policy, change_policy=change_policy)
        Assertion.assert_equal(output, True, "ERR: edit relay policy from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc08_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc08_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc08_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc08_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_relay_policy_from_CLI(self):
        org_policy = {
            'protocol': 'DHCP',
            'from': 'interface X0',
        }
        change_policy = {'to-new': 'name "X1 IP"'}
        output = iphelper_cli.edit_relay_policies(org_policy=org_policy, change_policy=change_policy)
        Assertion.assert_equal(output, True, "ERR: init relay policy from cli failed")


class TestWebProxy_TC13(Test):
    uuid = "SOSAIOT-TC-55089"
    description = "Web Proxy - Configure Automatic Proxy Forwarding (Web Only)"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'WebProxy_TC13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_edit_proxy_forwarding_from_CLI(self):
        webproxy_dict = {
            'server': '1.1.1.1',
            'port': '3128',
        }
        output = webproxy_cli.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: edit proxy forwarding from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc13_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc13_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc13_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc13_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_proxy_forwarding_from_CLI(self):
        webproxy_dict = {
            'server': '0.0.0.0',
            'port': '0',
        }
        output = webproxy_cli.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: init proxy forwarding from cli failed")


class TestWebProxy_TC15(Test):
    uuid = "SOSAIOT-TC-55090"
    description = "Web Proxy - Edit User Proxy Servers"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'WebProxy_TC15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_edit_user_proxy_servers_from_CLI(self):
        output = webproxy_cli.add_user_proxy_server('2.2.2.2')
        Assertion.assert_equal(output, True, "ERR: edit User Proxy Servers from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc15_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc15_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc15_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc15_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_user_proxy_servers_from_CLI(self):
        output = webproxy_cli.del_user_proxy_server('2.2.2.2')
        Assertion.assert_equal(output, True, "ERR: init User Proxy Servers from cli failed")


class TestDDNS_TC20(Test):
    uuid = "SOSAIOT-TC-55091"
    description = "Dynamic DNS - Add a DDNS profile - dyn.com"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DDNS_TC20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_ddns_profile_from_CLI(self):
        profile_dict = {
            'name': 'auto_test01',
            'domain': 'test.dyn.com',
            'password': 'test1234',
            'user-name': 'automation',
            'bound-to': 'any',
            'provider': 'dyn',
        }
        output = ddns_cli.add_ddns_profile(**profile_dict)
        Assertion.assert_equal(output, True, "ERR: add ddns profile from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc20_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc20_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc20_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc20_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_ddns_profile_from_CLI(self):
        output = ddns_cli.del_ddns_profile(name='auto_test01')
        Assertion.assert_equal(output, True, "ERR: init ddns profile from cli failed")


class TestDDNS_TC24(Test):
    uuid = "SOSAIOT-TC-55092"
    description = "Dynamic DNS - Edit DDNS profiles - Advanced"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DDNS_TC24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_edit_ddns_profile_from_CLI(self):
        ddns_edit = {
            'name': 'auto_test01',
            'user-name-new': 'test_user01',
            'password-new': 'test_password01',
            'domain-new': 'test.auto.com',
        }
        output = ddns_cli.edit_ddns_profile(**ddns_edit)
        Assertion.assert_equal(output, True, "ERR: edit ddns profile from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc24_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc24_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc24_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc24_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_ddns_profile_from_CLI(self):
        ddns_edit = {
            'name': 'auto_test01',
            'user-name-new': 'automation',
            'password-new': 'test1234',
            'domain-new': 'test.dyn.com',
        }
        output = ddns_cli.edit_ddns_profile(**ddns_edit)
        Assertion.assert_equal(output, True, "ERR: init ddns profile from cli failed")


class TestDDNS_TC27(Test):
    uuid = "SOSAIOT-TC-55093"
    description = "Dynamic DNS - Edit DDNS profiles - Profiles Settings - IPv6"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DDNS_TC27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_ipv6_ddns_profile_from_CLI(self):
        profile_dict = {
            'version': 'ipv6',
            'name': 'auto_test02',
            'domain': 'v6.dyn.com',
            'password': 'testv61234',
            'user-name': 'root02',
            'bound-to': 'any',
            'provider': 'dyn',
        }
        output = ddns_cli.add_ddns_profile(**profile_dict)
        Assertion.assert_equal(output, True, "ERR: add ipv6 ddns profile from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc27_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc27_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc27_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc27_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_ipv6_ddns_profile_from_CLI(self):
        output = ddns_cli.del_ddns_profiles(version='ipv6')
        Assertion.assert_equal(output, True, "ERR: init ipv6 ddns profile from cli failed")


class TestNetworkMonitor_TC36(Test):
    uuid = "SOSAIOT-TC-55094"
    description = "Network Monitor - Add a policy - Ping(ICMP)"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NetworkMonitor_TC36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_network_monitor_from_CLI(self):
        nm_dict = {
            'name': 'auto_nm_ping',
            'probe-target': 'name "X1 IP"',
            'outbound-interface': 'X1',
            'next-hop': 'name "X0 IP"',
            'probe-type': 'ping explicit',
        }
        output = networkmonitor_cli.add_nm_policy(**nm_dict)
        Assertion.assert_equal(output, True, "ERR: add network monitor from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc36_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc36_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc36_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc36_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestNetworkMonitor_TC43(Test):
    uuid = "SOSAIOT-TC-55095"
    description = "Network Monitor - Edit a policy - TCP-Explicit Route"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NetworkMonitor_TC43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_edit_network_monitor_from_CLI(self):
        nm_dict = {
            'name': 'auto_nm_ping',
            'probe-type': 'tcp explicit',
            'port': '3456',
            'next-hop': 'name "X2 IP"',
        }
        output = networkmonitor_cli.edit_nm_policy(**nm_dict)
        Assertion.assert_equal(output, True, "ERR: edit network monitor from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc43_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc43_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc43_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc43_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestNetworkMonitor_TC46(Test):
    uuid = "SOSAIOT-TC-55096"
    description = "Network Monitor - Add a policy - IPv6 - TCP"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NetworkMonitor_TC46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_ipv6_network_monitor_from_CLI(self):
        nm_dict = {
            'version': 'ipv6',
            'name': 'auto_nm_tcp_v6',
            'probe-target': 'group "X1 IPv6 Addresses"',
            'probe-type': 'tcp',
            'port': '2345',
        }
        output = networkmonitor_cli.add_nm_policy(**nm_dict)
        Assertion.assert_equal(output, True, "ERR: add ipv6 network monitor from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc46_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc46_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc46_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc46_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestNetworkMonitor_TC52(Test):
    uuid = "SOSAIOT-TC-55097"
    description = "Network Monitor - Delete one/multiple policies"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NetworkMonitor_TC52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_del_network_monitor_policies_from_CLI(self):
        output1 = networkmonitor_cli.del_nm_policy(name='auto_nm_ping', version='ipv4')
        output2 = networkmonitor_cli.del_nm_policy(name='auto_nm_tcp_v6', version='ipv6')
        logger.info(f'del ipv4: {output1}, del ipv6: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: del network monitor policies from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc52_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc52_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc52_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc52_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestMatchObjectsDynamicGroup_TC63(Test):
    uuid = "SOSAIOT-TC-55099"
    description = "Dynamic External Objects - Add an Address Group - FTP"
    dynamic_object_name = 'autotest01'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MatchObjectsDynamicGroup_TC63')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_ftp_match_objects_dynamic_group_from_CLI(self):
        object_dict = {
            "name": self.dynamic_object_name,
            "type": "address-group",
            "zone": "LAN",
            "fqdn": True,
            "periodic_download": "interval 1-hour",
            "protocol": "ftp",
            "server": "10.11.11.11",
            "login": "autoroot",
            "password": "autopassword",
            "directory": "/tmp/test",
            "filename": "autofiles"
        }
        output = MatchObjectsDynamicGroup_cli.add_dynamic_external_object(**object_dict)
        Assertion.assert_equal(output, True, "ERR: add ftp match objects dynamic group from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc63_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc63_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc63_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc63_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_del_match_objects_dynamic_group_from_CLI(self):
        output = MatchObjectsDynamicGroup_cli.del_dynamic_external_object(self.dynamic_object_name)
        Assertion.assert_equal(output, True, "ERR: del match objects dynamic group from cli failed")


class TestMatchObjectsDynamicGroup_TC64(Test):
    uuid = "SOSAIOT-TC-55100"
    description = "Dynamic External Objects - Add an Address Group - HTTPS"
    dynamic_object_name = 'autotest02'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MatchObjectsDynamicGroup_TC64')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_https_match_objects_dynamic_group_from_CLI(self):
        object_dict = {
            "name": self.dynamic_object_name,
            "protocol": "http",
            "url": "https://10.12.12.12",
        }
        output = MatchObjectsDynamicGroup_cli.add_dynamic_external_object(**object_dict)
        Assertion.assert_equal(output, True, "ERR: add https match objects dynamic group from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc64_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc64_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc64_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc64_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestMatchObjectsDynamicGroup_TC67(Test):
    uuid = "SOSAIOT-TC-55101"
    description = "Dynamic External Objects - Download the entry manually"
    dynamic_object_name = 'autotest02'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MatchObjectsDynamicGroup_TC67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_download_https_match_objects_dynamic_group_from_CLI(self):
        output = MatchObjectsDynamicGroup_cli.download_dynamic_external_object(self.dynamic_object_name)
        Assertion.assert_equal(output, False, "ERR: download https match objects dynamic group from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        Assertion.assert_regular(str(syslog), 'Download Dynamic Group Object', "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        with os.popen('cat /var/log/messages', 'r') as file:
            syslog = file.read()
        Assertion.assert_regular(str(syslog),  'Download Dynamic Group Object', "ERR: check auditing log failed")

    def test_05_verify_log(self):
        output = log_api.export_log_txt()
        Assertion.assert_regular(str(output), 'Download Dynamic Group Object', "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        output = PC2_login.send_command(
            'cat /var/log/messages | grep snmptrapd')
        Assertion.assert_regular(str(output), 'Download Dynamic Group Object', "ERR: check snmp log failed")

    def test_07_del_match_objects_dynamic_group_from_CLI(self):
        output = MatchObjectsDynamicGroup_cli.del_dynamic_external_object(self.dynamic_object_name)
        Assertion.assert_equal(output, True, "ERR: del match objects dynamic group from cli failed")