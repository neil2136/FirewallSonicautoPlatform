from definition.settings import *


def check_syslog(old_value, new_value, special_value=None):
    output = pc1.send_command('cat /var/log/messages')
    logger.info(output)
    if special_value != None:
        if special_value in output:
            resp = True
        assert resp == True, "Failed to check logs in syslog server."
    else:
        Assertion.assert_regular(output, f'oldValue="{old_value}" newValue="{new_value}"',
                                 "Failed to check logs in syslog server.")


def check_snmp_traps(value):
    output = pc2.send_command('cat /var/log/messages | grep snmptrapd')
    logger.info(output)
    if value in output:
        resp = True
    assert resp == True, "Failed to check snmp traps"


def check_audit_log(value):
    output = audit_logobj.export_audit_log_txt()
    logger.info(output)
    Assertion.assert_regular(output, value, "Failed to check audit logs.")


def check_logs(value):
    output = log_obj.export_log_txt()
    logger.info(output)
    if value in output:
        resp = True
    assert resp == True, "Failed to check system logs."


def clear_log_and_snmp_msg():
    log_obj.clear_log()
    out1 = pc1.send_commands(["echo '' > /var/log/messages", "cat /var/log/messages"])
    out2 = pc2.send_commands(["echo '' > /var/log/messages", "cat /var/log/messages"])
    out1, out2 = out1.replace(' ', '').replace('\n', ''), out2.replace(' ', '').replace('\n', '')
    if out1 == '' and out2 == '':
        rc = True
        logger.info('clear log and snmp server message successful!')
    else:
        rc = False
        logger.info(f'out1:{out1}')
        logger.info(f'out2:{out2}')
        logger.info('clear log and snmp server message Failed!')
    return rc


class TC_01_SSL_VPN_and_Virtual_Assist(Test):
    uuid = "SOSAIOT-TC-55115"
    description = show_testcase_info(Parameter.TESTPLAN, '1514821', description=True)

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514821')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_zone_object(self):
        zone_obj_json = {
            "zones": [
                {
                    "name": "custom_zone",
                    "security_type": "Trusted",
                    "ssl_control": False,

                }
            ]
        }
        rc = zone_obj.add_zone_object(**zone_obj_json)
        Assertion.assert_equal(rc, True, "ERR: Add Zone object Failed.")

    def test_02_Enable_SSL_VPN_Status_on_Zones(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring SSLVPN status on zone  ')
        commands = ['conf', 'zone LAN', 'sslvpn-access', 'exit', 'zone WAN', 'sslvpn-access', 'exit', 'zone DMZ',
                    'sslvpn-access', 'exit',
                    'zone custom_zone', 'sslvpn-access', 'exit', 'commit', 'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_03_check_logs(self):
        check_syslog('disabled', 'enabled')
        check_snmp_traps(
            '"Configuration succeeded:  \'Enable SSLVPN Access\' , LAN, changed from [disabled], changed to [enabled]')
        check_audit_log(
            "Zone Object                   LAN                            \'Enable SSLVPN Access\'       disabled            enabled")
        check_logs(
            "Configuration succeeded:  \'Enable SSLVPN Access\' , LAN, changed from [disabled], changed to [enabled]")


class TC_02_SSL_VPN_and_Virtual_Assist(Test):
    uuid = "SOSAIOT-TC-55116"
    description = show_testcase_info(Parameter.TESTPLAN, '1514822', description=True)

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514822')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_general_settings_in_virtual_assist(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring SSLVPN status on zone  ')
        commands = ['conf', 'ssl-vpn virtual-office', 'bookmark "test"', 'host 10.5.6.3', 'service ssh', 'commit',
                    'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled',
                     special_value='"Configuration succeeded:  \'SSL VPN Bookmark Service Name\' , test')
        check_snmp_traps('"Configuration succeeded:  \'SSL VPN Bookmark Service Name\' , test, changed to [test]')
        check_audit_log("\'SSL VPN Bookmark Service Name\'                     test")
        check_logs("Configuration succeeded:  \'SSL VPN Bookmark Service Name\' , test")


class TC_03_SSL_VPN_and_Virtual_Assist(Test):
    uuid = "SOSAIOT-TC-55118"
    description = show_testcase_info(Parameter.TESTPLAN, '1514824', description=True)

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514824')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_SSL_VPN_Server_Settings(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring SSLVPN status on zone  ')
        commands = ['conf', 'ssl-vpn server', 'management ssh', 'commit', 'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled')
        check_snmp_traps(
            '"Configuration succeeded:  \'Enable SSH Management over SSL VPN\' , changed from [disabled], changed to [enabled]')
        check_audit_log("\'Enable SSH Management over SSL VPN\' disabled            enabled")
        check_logs(
            "Configuration succeeded:  \'Enable SSH Management over SSL VPN\' , changed from [disabled], changed to [enabled]")


class TC_04_SSL_VPN_and_Virtual_Assist(Test):
    uuid = "SOSAIOT-TC-55119"
    description = show_testcase_info(Parameter.TESTPLAN, '1514825', description=True)

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514825')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_SSL_VPN_Client_Settings(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring SSLVPN status on zone  ')
        commands = ['conf', 'ssl-vpn profile', 'device-profile "Default Device Profile"', 'client',
                    'dns primary 10.5.6.9', 'commit', 'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('0.0.0.0', '10.5.6.9')
        check_snmp_traps('"Configuration succeeded:  \'NAC attr primary DNS\' , Default Device Profile')
        check_audit_log(
            "Default Device Profile for Windows \'NAC attr primary DNS\'       0.0.0.0             10.5.6.9")
        check_logs("Configuration succeeded: Modified \'NAC attr name\' , Default Device Profile for Windows")


class TC_05_SSL_VPN_and_Virtual_Assist(Test):
    uuid = "SOSAIOT-TC-55120"
    description = show_testcase_info(Parameter.TESTPLAN, '1514826', description=True)

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514826')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_custom_address_object(self):
        address_object = {
            "object_type": "host",
            "name": "sslvpn_test",
            "zone": "SSLVPN",
            "value": "10.15.6.53"
        }
        resp = LAddrOBJ.config_addressobject(**address_object)

    def test_03_Modify_SSL_VPN_Client_Settings(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring SSLVPN status on zone  ')
        commands = ['conf', 'ssl-vpn profile', 'device-profile "Default Device Profile"',
                    'network-address ipv4 name sslvpn_test ', 'commit', 'exit']

        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_04_check_logs(self):
        check_syslog('disabled', 'enabled',
                     special_value='"Configuration succeeded:  \'NAC attr address object\' , Default Device Profile for SonicPointN, changed')
        check_snmp_traps(
            '"Configuration succeeded:  \'NAC attr address object\' , Default Device Profile for SonicPointN')
        check_audit_log("Default Device Profile for SonicPointN \'NAC attr address object\'")
        check_logs(
            "Configuration succeeded:  \'NAC attr address object\' , Default Device Profile for SonicPointN, changed")
