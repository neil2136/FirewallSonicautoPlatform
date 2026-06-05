from settings import *
from utils import *


class TestConfig_Auditing_CLI_Selected_TC01(Test):
    uuid = "SOSAIOT-TC-55216"
    description = show_testcase_info(TESTPLAN, '1512822', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512822')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Disable_Wireless_LAN_and_IPv6_from_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        admini_cli.ipv6(enable=False)
        admini_cli.wireless_lan(enable=False)
        rc = admini_cli.show_admin_setting()
        if 'no wireless-lan' in str(rc) and 'no ipv6' in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Disable_Wireless_LAN_and_IPv6_from_CLI failed.")
    
    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=check_info_dict['tc1_disablesyslog'],output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: test_02_verify_syslog_on_PC1 failed")

    @repeat_method(15)
    def test_03_verify_auditing_log(self):
        time.sleep(100)
        rc = verify_result('audit', check_info_dict['tc1_disableauditlog'])
        Assertion.assert_equal(rc, True, "ERR: test_03_verify_auditing_log failed")

    # def test_04_verify_log(self):
    #     rc = verify_result('log', check_info_dict['tc1_disablelog'])
        # Assertion.assert_equal(rc, True, "ERR: test_04_verify_log failed")

    def test_05_verify_snmp(self):
        rc = verify_result('snmp',check_info_dict['tc1_disablesnmplog'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_06_Enable_Wireless_LAN_and_IPv6_from_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = True
        admini_cli.ipv6(enable=True)
        admini_cli.wireless_lan(enable=True)
        rc = admini_cli.show_admin_setting()
        if 'no wireless-lan' in str(rc) or 'no ipv6' in str(rc):
            flag = False
        Assertion.assert_equal(flag, True, "ERR: test_06_Enable_Wireless_LAN_and_IPv6_from_CLI failed.")

    def test_07_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=check_info_dict['tc1_enablesyslog'],output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: test_07_verify_syslog_on_PC1 failed")

    @repeat_method(15)
    def test_08_verify_auditing_log(self):
        time.sleep(100)
        rc = verify_result('audit', check_info_dict['tc1_enableauditlog'])
        Assertion.assert_equal(rc, True, "ERR: test_08_verify_auditing_log failed")

    # def test_09_verify_log(self):
    #     rc = verify_result('log', check_info_dict['tc1_enablelog'])
        # Assertion.assert_equal(rc, True, "ERR: test_09_verify_log failed")

    def test_10_verify_snmp(self):
        rc = verify_result('snmp',check_info_dict['tc1_enablesnmplog'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestConfig_Auditing_CLI_Selected_TC02(Test):
    uuid = "SOSAIOT-TC-55233"
    description = show_testcase_info(TESTPLAN, '1512841', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512841')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Enable_General_Settings_from_CLI_Client_SSL_General(self):
        logger.info('Clear related logs')
        clear_log_message()
        dpissl_dict = {
            'enable': True,
            'application-firewall': True,
        }
        rc = dpissl_obj.config_general_settings(**dpissl_dict)
        Assertion.assert_equal(rc, True, "ERR: test_01_Enable_General_Settings_from_CLI_Client_SSL_General failed.")

    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=check_info_dict['tc2_enablesyslog'],output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', check_info_dict['tc2_enableauditlog'])
        Assertion.assert_equal(rc, True, "ERR: test_03_verify_auditing_log failed")

    def test_04_verify_log(self):
        rc = verify_result('log', check_info_dict['tc2_enablelog'])
        Assertion.assert_equal(rc, True, "ERR: test_04_verify_log failed")

    def test_05_verify_snmp(self):
        rc = verify_result('snmp',check_info_dict['tc2_enablesnmplog'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_06_disable_General_Settings_from_CLI_Client_SSL_General(self):
        logger.info('Clear related logs')
        clear_log_message()
        dpissl_dict = {
            'enable': False,
            'application-firewall': False,
        }
        rc = dpissl_obj.config_general_settings(**dpissl_dict)
        Assertion.assert_equal(rc, True, "ERR: test_06_disable_General_Settings_from_CLI_Client_SSL_General failed.")

    def test_07_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=check_info_dict['tc2_disablesyslog'],output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_08_verify_auditing_log(self):
        rc = verify_result('audit', check_info_dict['tc2_disableauditlog'])
        Assertion.assert_equal(rc, True, "ERR: test_08_verify_auditing_log failed")

    def test_09_verify_log(self):
        rc = verify_result('log', check_info_dict['tc2_disablelog'])
        Assertion.assert_equal(rc, True, "ERR: test_09_verify_log failed")

    def test_10_verify_snmp(self):
        rc = verify_result('snmp',check_info_dict['tc2_disablesnmplog'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")


class TestConfig_Auditing_CLI_Selected_TC03(Test):
    uuid = "SOSAIOT-TC-55226"
    description = show_testcase_info(TESTPLAN, '1512834', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512834')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_global_settings_of_app_control(self):
        logger.info('[App Control]Modify global settings of app control  ')
        commands = ['con', 'app-control','enable','log-all','log-filename',
                        'commit','exit']                       
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Modify_global_settings_of_app_control failed")

class TestConfig_Auditing_CLI_Selected_TC04(Test):
    uuid = "SOSAIOT-TC-55228"
    description = show_testcase_info(TESTPLAN, '1512836', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512836')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DDNS_profile(self):
        logger.info('Dynamic DNS - Add a DDNS profile - dyn.com  ')
        commands = ['con', 'dynamic-dns','dynamic-dns profile hhhddns','user-name testddns',
                    'password password','domain a.com','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Add_a_DDNS_profile failed")


class TestConfig_Auditing_CLI_Selected_TC05(Test):
    uuid = "SOSAIOT-TC-55229"
    description = show_testcase_info(TESTPLAN, '1512837', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512837')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Delete_Custom_Zones_via_CLI(self):
        logger.info('Dynamic DNS - Add a DDNS profile - dyn.com  ')
        commands = ['con', 'zone name newaddzone','security-type public','commit',
                    'exit','no zone name newaddzone','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Delete_Custom_Zones_via_CLI failed")



class TestConfig_Auditing_CLI_Selected_TC06(Test):
    uuid = "SOSAIOT-TC-55230"
    description = show_testcase_info(TESTPLAN, '1512838', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512838')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_tcp_setting_from_CLI(self):
        logger.info('[FW setting-flood protection/tcp]Modify tcp setting from CLI ')
        commands = ['con', 'tcp','default-connection-timeout','blacklist-threshold',
                    'checksum-enforcement','syn-flood-blacklisting','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Modify_tcp_setting_from_CLI failed")


class TestConfig_Auditing_CLI_Selected_TC07(Test):
    uuid = "SOSAIOT-TC-55231"
    description = show_testcase_info(TESTPLAN, '1512839', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512839')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_SSLControl_setting_from_CLI(self):
        logger.info('[FW setting/SSL Control]Modify Configuration from CLI ')
        commands = ['con', 'ssl-control','detect expired','detect ssl-v3',
                    'detect weak-ciphers','commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Modify_SSLControl_setting_from_CLI failed")


class TestConfig_Auditing_CLI_Selected_TC08(Test):
    uuid = "SOSAIOT-TC-55232"
    description = show_testcase_info(TESTPLAN, '1512840', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512840')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Modify_DPI_SSH_Inclusion_Exclusion(self):
        logger.info('Modify DPI-SSH Inclusion/Exclusion')
        commands = ['con', 'dpi-ssh','exclude service name NTP','exclude service name BGP',
                    'commit','exit']
    
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_Modify_DPI_SSH_Inclusion_Exclusion failed")


@paramunittest.parametrized(
    {'uuid': '1512823', 
                    'syslog_check':check_info_dict['tc3_syslog_check'],
                    'auditlog_check': check_info_dict['tc3_auditlog_check'],
                    'log_check':check_info_dict['tc3_log_check'] ,
                    'snmplog_check': check_info_dict['tc3_snmplog_check']},
    {'uuid': '1512824', 
                    'syslog_check':check_info_dict['tc4_syslog_check'],
                    'auditlog_check': check_info_dict['tc4_auditlog_check'],
                    'log_check':check_info_dict['tc4_log_check'] ,
                    'snmplog_check': check_info_dict['tc4_snmplog_check']},
    {'uuid': '1512825', 
                    'syslog_check':check_info_dict['tc5_syslog_check'],
                    'auditlog_check': check_info_dict['tc5_auditlog_check'],
                    'log_check':check_info_dict['tc5_log_check'] ,
                    'snmplog_check': check_info_dict['tc5_snmplog_check']},
    {'uuid': '1512826', 
                    'syslog_check':check_info_dict['tc6_syslog_check'],
                    'auditlog_check': check_info_dict['tc6_auditlog_check'],
                    'log_check':check_info_dict['tc6_log_check'] ,
                    'snmplog_check': check_info_dict['tc6_snmplog_check']},
    {'uuid': '1512827', 
                    'syslog_check':check_info_dict['tc7_syslog_check'],
                    'auditlog_check': check_info_dict['tc7_auditlog_check'],
                    'log_check':check_info_dict['tc7_log_check'] ,
                    'snmplog_check': check_info_dict['tc7_snmplog_check']},
    {'uuid': '1512828', 
                    'syslog_check':check_info_dict['tc8_syslog_check'],
                    'auditlog_check': check_info_dict['tc8_auditlog_check'],
                    'log_check':check_info_dict['tc8_log_check'] ,
                    'snmplog_check': check_info_dict['tc8_snmplog_check']},
    {'uuid': '1512831', 
                    'syslog_check':check_info_dict['tc9_syslog_check'],
                    'auditlog_check': check_info_dict['tc9_auditlog_check'],
                    'log_check':check_info_dict['tc9_log_check'] ,
                    'snmplog_check': check_info_dict['tc9_snmplog_check']},
    {'uuid': '1512832', 
                    'syslog_check':check_info_dict['tc10_syslog_check'],
                    'auditlog_check': check_info_dict['tc10_auditlog_check'],
                    'log_check':check_info_dict['tc10_log_check'] ,
                    'snmplog_check': check_info_dict['tc10_snmplog_check']},
    {'uuid': '1512833', 
                    'syslog_check':check_info_dict['tc11_syslog_check'],
                    'auditlog_check': check_info_dict['tc11_auditlog_check'],
                    'log_check':check_info_dict['tc11_log_check'] ,
                    'snmplog_check': check_info_dict['tc11_snmplog_check']},
    {'uuid': '1512835', 
                    'syslog_check':check_info_dict['tc12_syslog_check'],
                    'auditlog_check': check_info_dict['tc12_auditlog_check'],
                    'log_check':check_info_dict['tc12_log_check'] ,
                    'snmplog_check': check_info_dict['tc12_snmplog_check']},
 )

class TestConfig_Auditing_CLI_Selected_TC10_18(Test):
    def setParameters(self, uuid, syslog_check, auditlog_check,log_check,snmplog_check):
        self.uuid = uuid
        self.syslog_check = syslog_check
        self.auditlog_check = auditlog_check
        self.log_check = log_check
        self.snmplog_check = snmplog_check
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN,self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message() 
        flag = False
        if self.uuid == '1512823':
            logger.info('Add a VPN policy - Tunnel Interface - Preshared Secret')
            commands = ['con', 'vpn policy tunnel-interface VPNpolicy_TunnelInterPreshared',
                         'enable', 'gateway primary 3.3.2.6','auth-method shared-secret',
                         'shared-secret 123456','exit','proposal ipsec encryption aes-128',
                         'proposal ipsec authentication sha-1','keep-alive','no suppress-trigger-packet',
                         'bound-to interface X1','commit', 'exit',]
        if self.uuid == '1512824':
            logger.info('Add a VPN policy - Auto Provisioning Client')
            commands = ['con', 'vpn policy provision-client VPNpolicy_AutoProvisioningClient',
                         'gateway primary 2.5.4.6','enable',
                         'user-name qa','user-password 123456','auth-method shared-secret',
                         'shared-secret 123456','ap-client-id abc',
                         'commit','exit']
        if self.uuid == '1512825':
            logger.info('Add or Delete RADIUS SERVER via CLI ')
            commands = ['con', 'user radius','server 12.12.3.3','shared-secret password',
                         'commit','exit',
                         'no server 12.12.3.3',
                         'commit','exit']
        if self.uuid == '1512826':
            logger.info('Modify RADIUS SERVER via CLI ')
            commands = ['con', 'user radius','server 10.10.10.10','shared-secret password',
                         'commit',
                         'host 10.10.10.9',
                         'commit','exit']
        if self.uuid == '1512827':
            logger.info('Enable SSL VPN Access on Zones from CLI  ')
            commands = ['con', 'zone LAN','sslvpn-access',
                         'commit','exit']
        if self.uuid == '1512828':
            logger.info('Add a portal bookmark with service SSHv2 in Virtual Office from CLI  ')
            commands = ['con', 'ssl-vpn virtual-office','bookmark test','host 10.10.10.10',' service sshv2',
                         'commit','exit']
        if self.uuid == '1512831':
            logger.info('[Access Rules]Delete an access rule of IPv4 type  ')
            commands = ['con', 'no access-rule ipv4 from DMZ to LAN action deny',
                         'commit','exit']
        if self.uuid == '1512832':
            logger.info('[Match Objects]Add a match object from CLI  ')
            commands = ['con', 'match-object testmatchobject','type email-to','content-entry abc',
                         'commit','exit']
        if self.uuid == '1512833':
            logger.info('[Add System Schedules from CLI  ')
            commands = ['con', 'schedule name testSystemSchedules','occurs once','event 2024:08:01:00:00 2024:08:02:00:00',
                         'commit','exit']
        if self.uuid == '1512835':
            logger.info('IP Helper - Edit policies  ')
            commands = ['con', 'ip-helper','enable','policy protocol DHCP source zone WAN',
                        'destination host 8.96.4.3','comment new_add_policy','commit','exit',
                        'policy protocol DHCP source zone WAN','comment new_add_policy111',
                         'commit','exit']
            
                         

        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_config_fw_use_CLI failed")

    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=self.syslog_check,output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', self.auditlog_check)
        Assertion.assert_equal(rc, True, "ERR: test_03_verify_auditing_log failed")

    def test_04_verify_log(self):
        rc = verify_result('log', self.log_check)
        Assertion.assert_equal(rc, True, "ERR: test_04_verify_log failed")

    def test_05_verify_snmp(self):
        rc = verify_result('snmp',self.snmplog_check)
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")