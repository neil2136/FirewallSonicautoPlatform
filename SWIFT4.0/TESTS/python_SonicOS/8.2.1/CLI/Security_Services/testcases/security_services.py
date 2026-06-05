from definition.settings import *


def check_syslog(old_value, new_value,special_value=None):
    output = pc1.send_command('cat /var/log/messages')
    if special_value != None:
        if special_value in output:
            resp = True
        assert resp == True, "Failed to check logs in syslog server."
    else:
        Assertion.assert_regular(output, f'oldValue="{old_value}" newValue="{new_value}"', "Failed to check logs in syslog server.")

def check_snmp_traps(value):
    output = pc2.send_command('cat /var/log/messages | grep snmptrapd')
    if value in output:
        resp = True
    assert resp == True, "Failed to check snmp traps"

def check_audit_log(value):
    output = audit_logobj.export_audit_log_txt()
    Assertion.assert_regular(output, value, "Failed to check audit logs.")

def check_logs(value):
    output = log_obj.export_log_txt()
    if value in output:
        resp = True
    assert resp == True, "Failed to check system logs."

def clear_log_and_snmp_msg():
    log_obj.clear_log()
    out1 =pc1.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out2 =pc2.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out1,out2 = out1.replace(' ','').replace('\n',''),out2.replace(' ','').replace('\n','')
    if out1 == '' and out2 == '':
        rc = True
        logger.info('clear log and snmp server message successful!')
    else:
        rc = False
        logger.info(f'out1:{out1}')
        logger.info(f'out2:{out2}')
        logger.info('clear log and snmp server message Failed!')
    return rc

class TC_01_Security_Services(Test):
    uuid = "SOSAIOT-TC-55102"
    description = show_testcase_info(Parameter.TESTPLAN, '1522522', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522522')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_modify_block_web_features(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring Content filter services  ')
        commands = ['conf', 'content-filter','websense','block activex','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled')
        check_snmp_traps('"Configuration succeeded:  \'Websense Block ActiveX\' , changed from [disabled], changed to [enabled]')
        check_audit_log("\'Websense Block ActiveX\'     disabled            enabled")
        check_logs("Configuration succeeded:  \'Websense Block ActiveX\' , changed from [disabled], changed to [enabled]")


class TC_02_Security_Services(Test):
    uuid = "SOSAIOT-TC-55103"
    description = show_testcase_info(Parameter.TESTPLAN, '1522523', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522523')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_modify_block_web_features(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring Content filter services  ')
        commands = ['conf', 'content-filter','filter-type websense','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('SonicWALL CFS', 'Websense Enterprise')
        check_snmp_traps('"Configuration succeeded:  \'CFS method\' , changed from [SonicWALL CFS], changed to [Websense Enterprise]')
        check_audit_log("\'CFS method\'                 SonicWALL CFS       Websense Enterprise")
        check_logs("Configuration succeeded:  \'CFS method\' , changed from [SonicWALL CFS], changed to [Websense Enterprise]")


class TC_03_Security_Services(Test):
    uuid = "SOSAIOT-TC-55104"
    description = show_testcase_info(Parameter.TESTPLAN, '1522524', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522524')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_modify_block_web_features(self):
        clear_log_and_snmp_msg()
        logger.info('Configuring Content filter services  ')
        commands = ['conf', 'rbl','enable','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled')
        check_snmp_traps('"Configuration succeeded:  \'Enable Real-time Black List Blocking\' , changed from [disabled], changed to [enabled]')
        check_audit_log("\'Enable Real-time Black List Blocking\' disabled            enabled")
        check_logs("Configuration succeeded:  \'Enable Real-time Black List Blocking\' , changed from [disabled], changed to [enabled]")


class TC_04_Security_Services(Test):
    uuid = "SOSAIOT-TC-55105"
    description = show_testcase_info(Parameter.TESTPLAN, '1522525', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522525')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_rbl_services(self):
        logger.info('Adding RBL services  ')
        commands = ['conf', 'rbl','service domain test.com','blocked-responses open-relay','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")
    
    def test_02_delete_rbl_services(self):
        clear_log_and_snmp_msg()
        logger.info('Deleting RBL services  ')
        commands = ['conf', 'rbl','no service domain test.com','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_03_check_logs(self):
        check_syslog('disabled', 'enabled',special_value='"Configuration succeeded: Deleted \'RBL Domain\' , test.com')
        check_snmp_traps('"Configuration succeeded: Deleted \'RBL Domain\' , test.com')
        check_audit_log("Deleted \'RBL Domain\'          test.com")
        check_logs("Configuration succeeded: Deleted \'RBL Domain\' , test.com")


class TC_05_Security_Services(Test):
    uuid = "SOSAIOT-TC-55106"
    description = show_testcase_info(Parameter.TESTPLAN, '1522526', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522526')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_custom_address_object(self):
        address_object = {
            "object_type": "host",
            "name": "custom_ao",
            "zone": "LAN",
            "value": "50.30.26.52"
        }
        resp = LAddrOBJ.config_addressobject(**address_object)

    def test_02_add_geo_ip_custom_list(self):
        clear_log_and_snmp_msg()
        logger.info('Adding GeoIP custom list ')
        commands = ['conf', 'geo-ip','custom-list','address name "custom_ao"','country Afghanistan','comment testcomment','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_03_check_logs(self):
        check_syslog('disabled', 'enabled',special_value="Configuration succeeded:  \'User specified address object for custom country list\' , custom_ao, changed to [custom_ao]")
        check_snmp_traps('"Configuration succeeded:  \'User specified address object for custom country list\' , custom_ao, changed to [custom_ao]')
        check_audit_log("Geo-Ip location               custom_ao                      \'User specified address object for custom country list\'                     custom_ao")
        check_logs("Configuration succeeded:  \'User specified address object for custom country list\' , custom_ao, changed to [custom_ao]")


class TC_06_Security_Services(Test):
    uuid = "SOSAIOT-TC-55107"
    description = show_testcase_info(Parameter.TESTPLAN, '1522527', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522527')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_security_service_summary(self):
        clear_log_and_snmp_msg()
        logger.info('Modifying security service summary  ')
        commands = ['conf', 'security-services','proxy-server','enable','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled')
        check_snmp_traps('"Configuration succeeded:  \'GAV download signaturation via proxy\' , changed from [disabled], changed to [enabled]')
        check_audit_log("\'GAV download signaturation via proxy\' disabled            enabled")
        check_logs("Configuration succeeded:  \'GAV download signaturation via proxy\' , changed from [disabled], changed to [enabled]")


class TC_07_Security_Services(Test):
    uuid = "SOSAIOT-TC-55108"
    description = show_testcase_info(Parameter.TESTPLAN, '1522528', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522528')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_botnet_list(self):
        clear_log_and_snmp_msg()
        logger.info('Adding Custom Botnet List  ')
        commands = ['conf', 'botnet','custom-list','address name custom_ao','enable','comment testcomment','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled',special_value="Configuration succeeded:  \'User specified address object for custom botnet list\' , custom_ao, changed to [custom_ao]")
        check_snmp_traps('"Configuration succeeded:  \'User specified address object for custom botnet list\' , custom_ao, changed to [custom_ao]')
        check_audit_log("Botnet element                custom_ao                      \'User specified comment for custom botnet list\'                     testcomment")
        check_logs("Configuration succeeded:  \'User specified address object for custom botnet list\' , custom_ao, changed to [custom_ao]")


class TC_08_Security_Services(Test):
    uuid = "SOSAIOT-TC-55109"
    description = show_testcase_info(Parameter.TESTPLAN, '1522529', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522529')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_custom_botnet_list(self):
        clear_log_and_snmp_msg()
        logger.info('Modifying Custom Botnet List  ')
        commands = ['conf', 'botnet','custom-list','address name custom_ao','no enable','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('enabled', 'disabled')
        check_snmp_traps('"Configuration succeeded:  \'User specified country id for custom botnet list\' , custom_ao, changed from [enabled], changed to [disabled]')
        check_audit_log("Botnet element                custom_ao                      \'User specified country id for custom botnet list\' enabled             disabled")
        check_logs("Configuration succeeded:  \'User specified country id for custom botnet list\' , custom_ao, changed from [enabled], changed to [disabled]")


class TC_09_Security_Services(Test):
    uuid = "SOSAIOT-TC-55110"
    description = show_testcase_info(Parameter.TESTPLAN, '1522530', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522530')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_custom_botnet_list(self):
        clear_log_and_snmp_msg()
        logger.info('Deleting Custom Botnet List  ')
        commands = ['conf', 'botnet','custom-list','no address name custom_ao','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled',special_value="Configuration succeeded: Deleted \'User specified address object for custom botnet list\' , custom_ao, changed from [custom_ao]")
        check_snmp_traps('"Configuration succeeded: Deleted \'User specified address object for custom botnet list\' , custom_ao, changed from [custom_ao]')
        check_audit_log("Botnet element                custom_ao                     Deleted \'User specified address object for custom botnet list\' custom_ao")
        check_logs("Configuration succeeded: Deleted \'User specified address object for custom botnet list\' , custom_ao, changed from [custom_ao]")


class TC_10_Security_Services(Test):
    uuid = "SOSAIOT-TC-55111"
    description = show_testcase_info(Parameter.TESTPLAN, '1522531', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522531')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_flush_dynamic_botnet(self):
        clear_log_and_snmp_msg()
        logger.info('Flush Dynamic Botnet')
        commands = ['conf', 'botnet','dynamic-list','botnet-flush','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('disabled', 'enabled',special_value="Configuration succeeded: flush dynamic botnet")
        check_snmp_traps('"Configuration succeeded: flush dynamic botnet')
        check_audit_log("flush dynamic botnet")
        check_logs("Configuration succeeded: flush dynamic botnet")


class TC_11_Security_Services(Test):
    uuid = "SOSAIOT-TC-55112"
    description = show_testcase_info(Parameter.TESTPLAN, '1522532', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522532')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_web_block_page(self):
        clear_log_and_snmp_msg()
        logger.info('Modify web block page')
        commands = ['conf', 'botnet','no include block-details','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('enabled', 'disabled')
        check_snmp_traps('"Configuration succeeded:  \'Botnet Include Block Details\' , changed from [enabled], changed to [disabled]')
        check_audit_log("\'Botnet Include Block Details\' enabled             disabled")
        check_logs("Configuration succeeded:  \'Botnet Include Block Details\' , changed from [enabled], changed to [disabled]")


class TC_12_Security_Services(Test):
    uuid = "SOSAIOT-TC-55113"
    description = show_testcase_info(Parameter.TESTPLAN, '1522533', description=True)
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522533')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_security_services(self):
        clear_log_and_snmp_msg()
        logger.info('Deleting Custom Botnet List  ')
        commands = ['conf', 'security-services','security maximum','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")

    def test_02_check_logs(self):
        check_syslog('Performance Optimized', 'Maximum Security')
        check_snmp_traps('"Configuration succeeded:  \'Security Services DPI Setting\' , changed from [Performance Optimized], changed to [Maximum Security]')
        check_audit_log("\'Security Services DPI Setting\' Performance OptimizedMaximum Security")
        check_logs("Configuration succeeded:  \'Security Services DPI Setting\' , changed from [Performance Optimized], changed to [Maximum Security]")