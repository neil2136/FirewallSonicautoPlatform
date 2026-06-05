from settings import *
from utils import *


class TC01_Add_Radius_Server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55150"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_add_radius_server_via_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add RADIUS SERVER via CLI')
        commands = ['con', 'user radius', 'server 192.168.168.51', 'shared-secret password',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Adding RADIUS Server via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_radius_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_radius_server])
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_radius_server])
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_radius_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Adding RADIUS Server via CLI Log message not received")


class TC02_Add_LDAP_Server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55151"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add LDAP SERVER via CLI')
        commands = ['con', 'user ldap', 'server 192.168.168.52',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Adding LDAP Server via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_ldap_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: Config Adding RADIUS Server via CLI Log message not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Adding RADIUS Server via CLI Log message not received")


class TC03_Add_SSO_Agent_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55152"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add SSO Agent via CLI')
        commands = ['con', 'user sso', 'agent 192.168.168.53 80',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Adding SSO Agent via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_sso_agent], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Agent via CLI Log Message is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Agent via CLI Log Message is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Agent via CLI Log Message is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add SSO Agent via CLI Log Message is not received")


class TC04_Add_Tacacs_server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55153"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add TACACS+ SERVER via CLI')
        commands = ['con', 'user tacacs', 'server 192.168.168.54',
                    'port 49', 'shared-secret password',
                    'no through-vpn', 'enable',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add TACACS+ SERVER via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_tacacs_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ SERVER via CLI log message not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ SERVER via CLI log message not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ SERVER via CLI log message not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add TACACS+ SERVER via CLI log message not received")


class TC05_Delete_Radius_server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55154"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete RADIUS SERVER via CLI')
        commands = ['con', 'user radius',
                    'no server 192.168.168.51',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete RADIUS SERVER via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_radius_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete RADIUS SERVER via CLI log message is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_radius_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete RADIUS SERVER via CLI log message is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_radius_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete RADIUS SERVER via CLI log message is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_radius_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete RADIUS SERVER via CLI log message is not received")


class TC06_Delete_LDAP_server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55155"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete LDAP SERVER via CLI')
        commands = ['con', 'user ldap',
                    'no server 192.168.168.52',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete LDAP SERVER via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_ldap_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete LDAP SERVER via CLI log message is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete LDAP SERVER via CLI log message is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete LDAP SERVER via CLI log message is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_ldap_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete LDAP SERVER via CLI log message is not received")


class TC07_Delete_SSO_Agent_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55156"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete SSO Agent via CLI')
        commands = ['con', 'user sso',
                    'no agent 192.168.168.53 80',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete SSO Agent via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_sso_agent], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete SSO Agent via CLI log message is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Delete SSO Agent via CLI log message is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Delete SSO Agent via CLI log message is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_sso_agent])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete SSO Agent via CLI log message is not received")


class TC08_Delete_Tacacs_server_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55157"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete TACACS+ SERVER via CLI')
        commands = ['con', 'user tacacs',
                    'no server 192.168.168.54',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete TACACS+ SERVER via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_tacacs_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete TACACS+ SERVER via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete TACACS+ SERVER via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: Config Delete TACACS+ SERVER via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_tacacs_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete TACACS+ SERVER via CLI log messages not received")


class TC09_Add_SSO_Agent_Terminal_Service_Agents_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55158"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add SSO Terminal Services Agent via CLI')
        commands = ['con', 'user sso', 'terminal-services-agent 192.168.168.55 80',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add SSO Terminal Services Agent via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_sso_ts_agent], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Terminal Services Agent via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_sso_ts_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Terminal Services Agent via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_sso_ts_agent])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO Terminal Services Agent via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_sso_ts_agent])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add SSO Terminal Services Agent via CLI log messages not received")


class TC10_Add_SSO_Agent_Radius_Accounting_Client_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55159"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add SSO RADIUS Accounting Client via CLI')
        commands = ['con', 'user sso', 'radius-accounting-client 192.168.168.56',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add SSO RADIUS Accounting Client via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_sso_ra_client], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO RADIUS Accounting Client via CLI log message is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_sso_ra_client])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO RADIUS Accounting Client via CLI log message is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_sso_ra_client])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO RADIUS Accounting Client via CLI log message is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_sso_ra_client])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add SSO RADIUS Accounting Client via CLI log message is not received")


class TC11_Add_SSO_Agent_Third_Party_API_Clients_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55160"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add SSO 3rd Party API Client via CLI')
        commands = ['con', 'user sso', 'third-party-api',
                    'client 192.168.168.56', 'enable',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add SSO 3rd Party API Client via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_sso_tp_client], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO 3rd Party API Client via CLI log messages is not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_sso_tp_client])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO 3rd Party API Client via CLI log messages is not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_sso_tp_client])
        Assertion.assert_equal(rc, True, "ERR: Config Add SSO 3rd Party API Client via CLI log messages is not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_sso_tp_client])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add SSO 3rd Party API Client via CLI log messages is not received")


class TC12_Add_Radius_Accounting_Servers_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55161"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add RADIUS Accounting Server via CLI')
        commands = ['con', 'user radius',
                    'accounting', 'server 192.168.168.57',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add RADIUS Accounting Server via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_radius_acct_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add RADIUS Accounting Server via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_radius_acct_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add RADIUS Accounting Server via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_radius_acct_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add RADIUS Accounting Server via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_radius_acct_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add RADIUS Accounting Server via CLI log messages not received")


class TC13_Add_Tacacs_Accounting_Servers_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55162"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add TACACS+ Accounting Server via CLI')
        commands = ['con', 'user tacacs',
                    'accounting', 'server 192.168.168.58',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add TACACS+ Accounting Server via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_tacacs_acct_server], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ Accounting Server via CLI log message not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_tacacs_acct_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ Accounting Server via CLI log message not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_tacacs_acct_server])
        Assertion.assert_equal(rc, True, "ERR: Config Add TACACS+ Accounting Server via CLI log message not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_tacacs_acct_server])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add TACACS+ Accounting Server via CLI log message not received")


class TC14_Add_Authentication_Partitions_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55163"
    system_model = "TZ"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):

        rc = status_api.show_status()
        self.system_model = rc["model"]
        if "TZ" not in self.system_model:
            logger.info('Clear related logs')
            clear_log_message()
            flag = False
            logger.info('Add Authentication Partitioning via CLI')
            commands = ['con', 'user partitioning', 'enable',
                        'partition default', 'name tempPartition',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: Add Authentication Partitioning via CLI FAILED")
        else:
            logger.info("Authentication Partition Feature is only available in NSA")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        if "TZ" not in self.system_model:
            syslog = get_syslog()
            rc = check_result(check_list=[added_auth_part], output=syslog, mode='syslog')
            Assertion.assert_equal(rc, True, "ERR: Config Add Authentication Partitioning via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        if "TZ" not in self.system_model:
            rc = verify_result('audit', [added_auth_part])
            Assertion.assert_equal(rc, True, "ERR: Config Add Authentication Partitioning via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        if "TZ" not in self.system_model:
            rc = verify_result('log', [added_auth_part])
            Assertion.assert_equal(rc, True, "ERR: Config Add Authentication Partitioning via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        if "TZ" not in self.system_model:
            rc = verify_result('snmp', [added_auth_part])
            Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Authentication Partitioning via CLI log messages not received")


class TC15_Add_Partition_Selection_Policies_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55164"
    system_model = "TZ"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        rc = status_api.show_status()
        self.system_model = rc["model"]
        if "TZ" not in self.system_model:
            logger.info('Clear related logs')
            clear_log_message()
            flag = False
            logger.info('Add Partition Selection Policy via CLI')
            commands = ['con', 'user partitioning', 'policy interface X0 zone LAN address-object any',
                        'commit', 'exit']
            rc = fw_cli.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: Add Partition Selection Policy via CLI FAILED")
        else:
            logger.info("Authentication Partition Feature is only available in NSA")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        if "TZ" not in self.system_model:
            syslog = get_syslog()
            rc = check_result(check_list=[added_part_policy], output=syslog, mode='syslog')
            Assertion.assert_equal(rc, True, "ERR: Config Add Partition Selection Policy via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        if "TZ" not in self.system_model:
            rc = verify_result('audit', [added_part_policy])
            Assertion.assert_equal(rc, True, "ERR: Config Add Partition Selection Policy via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        if "TZ" not in self.system_model:
            rc = verify_result('log', [added_part_policy])
            Assertion.assert_equal(rc, True, "ERR: Config Add Partition Selection Policy via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        if "TZ" not in self.system_model:
            rc = verify_result('snmp', [added_part_policy])
            Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Partition Selection Policy via CLI log messages not received")


class TC16_Add_Local_Users_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55165"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add Local Users via CLI')
        commands = ['con', 'user local',
                    'user testuser1', 'password Testp@ssw0rd',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add Local Users via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_local_user], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Users via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_local_user])
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Users via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_local_user])
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Users via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_local_user])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Local Users via CLI log messages not received")


class TC17_Delete_Local_Users_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55166"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete Local Users via CLI')
        commands = ['con', 'user local',
                    'no user testuser1',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete Local Users via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_local_user], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete Local Users via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_local_user])
        Assertion.assert_equal(rc, True, "ERR: Config Delete Local Users via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_local_user])
        Assertion.assert_equal(rc, True, "ERR: Config Delete Local Users via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_local_user])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete Local Users via CLI log messages not received")


class TC18_Add_Local_Groups_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55167"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add Local Group via CLI')
        commands = ['con', 'user local',
                    'group testgroup1',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add Local Group via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_local_group], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Group via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_local_group])
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Group via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_local_group])
        Assertion.assert_equal(rc, True, "ERR: Config Add Local Group via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_local_group])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Local Group via CLI log messages not received")


class TC19_Add_Guest_Profiles_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55168"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add Guest Profile via CLI')
        commands = ['con', 'user guest',
                    'profile testprofile1',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add Guest Profile via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_guest_profile], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Profile via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_guest_profile])
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Profile via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_guest_profile])
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Profile via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_guest_profile])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Guest Profile via CLI log messages not received")


class TC20_Add_Guest_Accounts_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55169"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Add Guest Accounts via CLI')
        commands = ['con', 'user guest',
                    'user guestuser1', 'password guestuser1',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Add Guest Accounts via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[added_guest_accounts], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Accounts via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [added_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Accounts via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [added_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Add Guest Accounts via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [added_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Add Guest Accounts via CLI log messages not received")


class TC21_Generate_Guest_Accounts_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55170"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Generate Guest Accounts via CLI')
        commands = ['con', 'user guest',
                    'generate', 'num 1',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Generate Guest Accounts via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[generate_guest_accounts], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Generate Guest Accounts via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [generate_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Generate Guest Accounts via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [generate_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Generate Guest Accounts via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [generate_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Generate Guest Accounts via CLI log messages not received")


class TC22_Exports_Guest_Accounts_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55171"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Export Guest Accounts via CLI')
        commands = ['con', 'user guest',
                    'user guestuser2', 'password guestuser2', 'commit', 'exit',
                    'export guest-accounts scp scp://root@192.168.168.169/tmp',
                    'yes', 'password', 'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Export Guest Accounts via CLI FAILED")
        time.sleep(10)

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[export_guest_accounts], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Export Guest Accounts via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [export_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Export Guest Accounts via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [export_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Export Guest Accounts via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [export_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Export Guest Accounts via CLI log messages not received")


class TC23_Delete_Guest_Accounts_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55172"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Delete Guest Accounts via CLI')
        commands = ['con', 'user guest',
                    'user guestuser2', 'password guestuser2', 'commit', 'exit',
                    'no user guestuser2',
                    'commit', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Delete Guest Accounts via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[deleted_guest_accounts], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Delete Guest Accounts via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [deleted_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Delete Guest Accounts via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [deleted_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: Config Delete Guest Accounts via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [deleted_guest_accounts])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Delete Guest Accounts via CLI log messages not received")


class TC24_Logout_Users_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55173"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Logout Users via CLI')
        commands = ['con', 'logout users', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Logout Users via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[logout_users], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Logout Users via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [logout_users])
        Assertion.assert_equal(rc, True, "ERR: Config Logout Users via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [logout_users])
        Assertion.assert_equal(rc, True, "ERR: Config Logout Users via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [logout_users])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Logout Users via CLI log messages not received")


class TC25_Logout_Guest_Users_Via_CLI(Test):
    uuid = "SOSAIOT-TC-55174"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        flag = False
        logger.info('Logout Guests via CLI')
        commands = ['con', 'logout guests', 'exit']
        rc = fw_cli.do_cli_commands(commands, tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Logout Guests via CLI FAILED")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=[logout_guests], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: Config Logout Guests via CLI log messages not found in Syslog")

    @repeat_method(5)
    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', [logout_guests])
        Assertion.assert_equal(rc, True, "ERR: Config Logout Guests via CLI log messages not found in Audit Logs")

    @repeat_method(5)
    def test_04_verify_log(self):
        rc = verify_result('log', [logout_guests])
        Assertion.assert_equal(rc, True, "ERR: Config Logout Guests via CLI log messages not found in Log Messages")

    @repeat_method(5)
    def test_05_verify_snmp(self):
        rc = verify_result('snmp', [logout_guests])
        Assertion.assert_equal(rc, True, "ERR: SNMP Trap for Config Logout Guests via CLI log messages not received")
