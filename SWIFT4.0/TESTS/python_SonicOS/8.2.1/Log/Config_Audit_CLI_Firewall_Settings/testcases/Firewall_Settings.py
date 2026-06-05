from definition.settings import *
from definition.utils import *


class TestFloodProtection_TC30(Test):
    uuid = "SOSAIOT-TC-55003"
    description = "[FW setting-flood protection/udp]Choose View IP Version as ipv6 from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtection_TC30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_enable_flood_protection_from_CLI(self):
        cmds = ['con', 'udp ipv6', 'flood protection', 'commit','end', 'exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: enable flood protection from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc30_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc30_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc30_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc30_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_disable_flood_protection_from_CLI(self):
        cmds = ['con', 'udp ipv6', 'no flood protection', 'commit','end', 'exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: disable flood protection from cli failed")


class TestFloodProtection_TC37(Test):
    uuid = "SOSAIOT-TC-55004"
    description = "[FW setting-flood protection/icmp]Choose View IP Version as ipv6 from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtection_TC37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_enable_flood_protection_from_CLI(self):
        cmds = ['con', 'icmp ipv6', 'flood protection', 'commit','end', 'exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: enable flood protection from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc37_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc37_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc37_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc37_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_disable_flood_protection_from_CLI(self):
        cmds = ['con', 'icmp ipv6', 'no flood protection', 'commit','end', 'exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: disable flood protection from cli failed")


class TestAddVLANTranslation_TC72(Test):
    uuid = "SOSAIOT-TC-55032"
    description = "Add VLAN Translation via CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'AddVLANTranslation_TC72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_interface_to_wiremode(self):
        X3_wiremode_dict = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'wire-mode',
            'type': 'secure',
            'wire_paired_interface': 'X4',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        output = interface_api.config_interface(**X3_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X3 to wiremode failed")

    def test_03_add_vlan_translation_from_CLI(self):
        cmds = ['con', 'vlan-translation ingress interface X3 vlan 666 egress interface X4 vlan 777', 'commit','end', 'exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: add vlan translation from cli failed")

    def test_04_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc72_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_05_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc72_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_06_verify_log(self):
        rc = verify_result('log', check_info_dict['tc72_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_07_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc72_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestDelVLANTranslation_TC74(Test):
    uuid = "SOSAIOT-TC-55033"
    description = "Delete VLAN Translation via CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DelVLANTranslation_TC74')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_del_vlan_translation_from_CLI(self):
        cmds = ['con', 'no vlan-translation ingress interface X3 vlan 666 egress interface X4 vlan 777', 'commit','exit']
        output = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: delete vlan translation from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc74_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc74_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc74_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc74_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    


class TestDetectionPrevention_TC01(Test):
    uuid = "SOSAIOT-TC-54996"
    description = "[FW setting-Advanced]Modify Detection Prevention from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DetectionPrevention_TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_enable_all_detection_prevention_from_CLI(self):
        decection_dict = {
            'stealth-mode': True,
            'randomize-id': True,
            'decrement ttl': True,
            'icmp time-exceeded-packets': False
        }
        output = advanced_cli.config_advanced(**decection_dict)
        Assertion.assert_equal(output, True, "ERR: enable Detection Prevention from cli failed")

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

    def test_07_init_detection_prevention_configure_from_CLI(self):
        decection_dict = {
            'stealth-mode': False,
            'randomize-id': False,
        }
        output = advanced_cli.config_advanced(**decection_dict)
        Assertion.assert_equal(output, True, "ERR: init Detection Prevention configure failed")


class TestDynamicPorts_TC61(Test):
    uuid = "SOSAIOT-TC-55013"
    description = "[FW setting-Advanced]Modify Dynamic Ports from telnet"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DynamicPorts_TC61')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_dynamic_ports_to_ftp_from_CLI(self):
        dynamic_dict = {
            'ftp-transforms-in-service-object-type': 'name',
            'ftp-transforms-in-service-object': 'Telnet',
        }
        output = advanced_cli.config_advanced(**dynamic_dict)
        Assertion.assert_equal(output, True, "ERR: config dynamic ports to ftp from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc61_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc61_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc61_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc61_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_dynamic_ports_to_ftp_from_CLI(self):
        dynamic_dict = {
            'ftp-transforms-in-service-object-type': 'name',
            'ftp-transforms-in-service-object': 'FTP',
        }
        output = advanced_cli.config_advanced(**dynamic_dict)
        Assertion.assert_equal(output, True, "ERR: init dynamic ports to ftp from cli failed")


class TestBWM_TC16(Test):
    uuid = "SOSAIOT-TC-54997"
    description = "[FW setting-BWM]Modify Guaranteed options within range from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'BWM_TC16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_bwm_object_from_CLI(self):
        dynamic_dict = {
            'name': 'auto bwm test',
            'guaranteed_kbps': '0',
            'maximum_kbps': '20',
        }
        output = bwobject_cli.add_bandwidth_object(**dynamic_dict)
        Assertion.assert_equal(output, True, "ERR:add bwm object from cli failed")

    def test_03_edit_bwm_guaranteed_from_CLI(self):
        dynamic_dict = {
            'name': 'auto bwm test',
            'guaranteed_kbps': '123',
            'maximum_kbps': '456',
        }
        output = bwobject_cli.add_bandwidth_object(**dynamic_dict)
        Assertion.assert_equal(output, True, "ERR:edit bwm Guaranteed from cli failed")

    def test_04_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc16_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_05_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc16_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_06_verify_log(self):
        rc = verify_result('log', check_info_dict['tc16_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_07_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc16_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestBWM_TC18(Test):
    uuid = "SOSAIOT-TC-54998"
    description = "[FW setting-BWM]Modify Guaranteed options within range from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'BWM_TC18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc18_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_02_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc18_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_03_verify_log(self):
        rc = verify_result('log', check_info_dict['tc18_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_04_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc18_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_del_bwm_object_from_CLI(self):
        output = bwobject_cli.del_bandwidth_object('auto bwm test')
        Assertion.assert_equal(output, True, "ERR:del bwm object from cli failed")


class TestFloodProtectionTCP_TC20(Test):
    uuid = "SOSAIOT-TC-54999"
    description = "[FW setting-flood protection/tcp]Fail to modify Flood Protection from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtectionTCP_TC20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_tcp_settings_from_CLI(self):
        dynamic_dict = {
            'maximum-segment-lifetime': '66',
        }
        output = floodprotection_cli.config_tcp(**dynamic_dict)
        # UI or CLI error configure no longer logged to logs. skip check
        Assertion.assert_equal(output, False, "ERR: config tcp settings from cli failed")


class TestFloodProtectionTCP_TC22(Test):
    uuid = "SOSAIOT-TC-55000"
    description = "[FW setting-flood protection/tcp]Fail to modify Attack threshold from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtectionTCP_TC22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_tcp_settings_from_CLI(self):
        dynamic_dict = {
            'syn-attack-threshold': '1234567',
        }
        output = floodprotection_cli.config_tcp(**dynamic_dict)
        # UI or CLI error configure no longer logged to logs. skip check
        Assertion.assert_equal(output, False, "ERR: config tcp settings from cli failed")


class TestFloodProtectionTCP_TC25(Test):
    uuid = "SOSAIOT-TC-55001"
    description = "[FW setting-flood protection/tcp]Clear TCP Traffic Statistics from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtectionTCP_TC25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_clear_tcp_statistics_from_CLI(self):
        output = floodprotection_cli.clear_tcp_stats()
        Assertion.assert_equal(output, True, "ERR: clear tcp statistics from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc25_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc25_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc25_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc25_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestFloodProtectionUDP_TC28(Test):
    uuid = "SOSAIOT-TC-55002"
    description = "[FW setting-flood protection/udp]Fail to modify UDP Flood Protection from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'FloodProtectionUDP_TC28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_udp_settings_from_CLI(self):
        dynamic_dict = {
            'default-connection-timeout': '8765432',
        }
        output = floodprotection_cli.config_udp(**dynamic_dict)
        # UI or CLI error configure no longer logged to logs. skip check
        Assertion.assert_equal(output, False, "ERR: config udp settings from cli failed")


class TestQoSMapping_TC45(Test):
    uuid = "SOSAIOT-TC-55006"
    description = "[FW setting/QoS Mapping]Modify all options of QoS Mapping"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'QoSMapping_TC45')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_config_qos_mapping_from_CLI(self):
        qos_dict = {
            'qos-index': '0',
            'to-dscp-value': '4',
            'from-dscp-value': '5 6',
        }
        output = qosmapping_cli.config_qos_setting(**qos_dict)
        Assertion.assert_equal(output, True, "ERR: config qos mapping from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc45_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc45_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc45_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc45_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_qos_mapping_from_CLI(self):
        output = qosmapping_cli.reset_qos_setting()
        Assertion.assert_equal(output, True, "ERR: init qos mapping from cli failed")


class TestQoSMapping_TC47(Test):
    uuid = "SOSAIOT-TC-55007"
    description = "[FW setting/QoS Mapping]Click reset qos settings from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'QoSMapping_TC47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_reset_qos_settings_from_CLI(self):
        output = qosmapping_cli.reset_qos_setting()
        Assertion.assert_equal(output, True, "ERR: reset qos setting from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc47_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc47_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc47_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc47_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestSSLControl_TC48(Test):
    uuid = "SOSAIOT-TC-55008"
    description = "[FW setting/SSL Control]Modify General Settings from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SSLControl_TC48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_enable_ssl_control_settings_from_CLI(self):
        set_dict = {
            'enable': True,
        }
        output = sslcontrol_cli.set_ssl_control(**set_dict)
        Assertion.assert_equal(output, True, "ERR: enable ssl control setting from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc48_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc48_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc48_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc48_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_disable_ssl_control_settings_from_CLI(self):
        set_dict = {
            'enable': False,
        }
        output = sslcontrol_cli.set_ssl_control(**set_dict)
        Assertion.assert_equal(output, True, "ERR: disable ssl control setting from cli failed")


class TestSSLControl_TC49(Test):
    uuid = "SOSAIOT-TC-55009"
    description = "[FW setting/SSL Control]Modify Action from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SSLControl_TC49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_modify_action_settings_from_CLI(self):
        action_dict = {
            'action-type': 'log',
        }
        output = sslcontrol_cli.set_ssl_control_action(**action_dict)
        Assertion.assert_equal(output, True, "ERR:modify action setting from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc49_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc49_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc49_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc49_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_action_settings_from_CLI(self):
        action_dict = {
            'action-type': 'block',
        }
        output = sslcontrol_cli.set_ssl_control_action(**action_dict)
        Assertion.assert_equal(output, True, "ERR: init action setting from cli failed")


class TestSSLControl_TC51(Test):
    uuid = "SOSAIOT-TC-55010"
    description = "[FW setting/SSL Control]Add black/white list from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SSLControl_TC51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_add_black_white_list_from_CLI(self):
        config_dict = {
            'action': 'add',
            'black_name': ['auto_black_test'],
        }
        output = sslcontrol_cli.config_ssl_customlists(**config_dict)
        Assertion.assert_equal(output, True, "ERR: add black white from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc51_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc51_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc51_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc51_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_07_init_black_white_list_from_CLI(self):
        config_dict = {
            'action': 'delete',
            'black_name': ['auto_black_test'],
        }
        output = sslcontrol_cli.config_ssl_customlists(**config_dict)
        Assertion.assert_equal(output, True, "ERR: init black white from cli failed")


class TestCipherControl_TC55(Test):
    uuid = "SOSAIOT-TC-55011"
    description = "[FW setting/Cipher Control]Modify some ciphers block/unblock from CLI"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'CipherControl_TC55')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_all_log_records(self):
        clear_log_message()

    def test_02_modify_ciphers_block_from_CLI(self):
        output = ciphercontrol_cli.config_tls_control(cipher='TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384', block='block')
        Assertion.assert_equal(output, True, "ERR: modify ciphers block from cli failed")

    def test_03_verify_syslog_on_PC1(self):
        time.sleep(5)
        syslog = get_syslog_via_pc1()
        rc = check_result(check_list=check_info_dict['tc55_syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog on pc1 failed")

    def test_04_verify_auditing_log(self):
        time.sleep(5)
        rc = verify_result('audit', check_info_dict['tc55_auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: check auditing log failed")

    def test_05_verify_log(self):
        rc = verify_result('log', check_info_dict['tc55_log_check'])
        Assertion.assert_equal(rc, True, "ERR: check fw log failed")

    def test_06_verify_snmp(self):
        rc = verify_result('snmp', check_info_dict['tc55_snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")
