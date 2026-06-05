from definition.settings import *
from definition.utils import *


# check check X2 configure info in auditing records log successful.
class TestUI_01(Test):
    uuid = "SOSAIOT-TC-55276"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_check_auditing_records_option_in_diag(self):
        diag_cfs = {'stream': 'enableCfgAuditing=on'}
        output = diagapi.get_diag_info()
        res = True if output['data']['auditing_records']['enableCfgAuditing'] == 'CHECKED' else False
        if not res:
            res = diagapi.config_raw_api(**diag_cfs)
        Assertion.assert_equal(res, True, "ERR: check diag auditing_records option failed")

    def test_02_check_X2_configure_in_auditing_log(self):
        output = auditapi.show_audit_records()
        res = compare_dict_contained(output, audit_contain_dict)
        Assertion.assert_equal(res, True, "ERR: check X2 configure auditing records log failed")


# check X2 Interface info in mail letter successful
class TestBaseMail_04(Test):
    uuid = "SOSAIOT-TC-55277"
    description = show_testcase_info(TESTPLAN, '04', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_automation_email_setting(Test):
        mail_server_dict = {
            "mail_server": mail_server_ip,
            "mail_from": 'root@sonicauto.com',
        }
        res1 = logautomationapi.cfg_mail_server(**mail_server_dict)
        logger.info(f'config mail server settings: {res1}')

        res2 = logautomationapi.email_audit_settings(**{'audit': 'test@sonicauto.com'})
        logger.info(f'config audit mail addr: {res1}')
        Assertion.assert_equal(res1 & res2, True, "ERR: config mail server successfully")

    @repeat_method(3)
    def test_02_send_check_audit_log_content_in_mail(self):
        send_email = auditapi.email_audit_records()
        logger.info(f"Send email result = {send_email}")
        chk_email = False
        for i in range(5):
            if not chk_email:
                logger.info(f"Sleep 30s before checking emails in loop {i+1}.")
                time.sleep(30)
                pop3logres = mail.get_mail_contents_via_letters()
                if pop3logres:
                    mailed_log = '\n'.join(pop3logres)
                    logger.info('get audit log list:{}'.format(mailed_log))
                    for log in pop3logres:
                        checkres = [x in log for x in audit_contain_dict.values()]
                        logger.info(f'check audit log result: {checkres}')
                        if all(checkres):
                            chk_email = True
                            logger.info(f'get the march log: {log}')
                            break
                else:
                    logger.info('get latest mail content failed.')
        logger.info(f"Check email result = {chk_email}")
        res = send_email & chk_email
        logger.info(f"Case result = {res}")
        Assertion.assert_equal(res, True, "ERR: check audit log in mail failed")


# check the X2 interface configure in export csv.
class TestBaseExport_06(Test):
    uuid = "SOSAIOT-TC-55278"
    description = show_testcase_info(TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_export_audit_log_csv(self):
        res = False
        output = auditapi.export_audit_log_csv()
        for log in output.split('\n'):
            checkres = [x in log for x in audit_contain_dict.values()]
            logger.info(f'check audit log result: {checkres}')
            if all(checkres):
                res = True
                logger.info(f'get the march log: {log}')
                break
        Assertion.assert_equal(res, True, "ERR: check x2 interface info in export csv failed")


# only check console configure in audit log, only support 7.1.1
class TestBaseConsole_08(Test):
    uuid = "SOSAIOT-TC-55279"
    description = show_testcase_info(TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_enable_display_auditing_records_on_console(self):
        supplemental_dict = {
            "log": {
                "audit": {
                    "display_on_console": True,
                    "enable": True,
                    "supplemental_changes": False
                }
            }
        }
        output = auditapi.configure_audit_log(**supplemental_dict)
        Assertion.assert_equal(output, True, "ERR: enable display auditing records on console failed")

    def test_02_check_enable_display_in_auditing_log(self):
        contain_dict = {
            'description': " 'Enable Auditing Records Notification on Console' ",
            'old_value': 'disabled',
            'new_value': 'enabled',
            'user': 'admin',
            'status': 'Succeeded',
        }
        time.sleep(5)
        output = auditapi.show_audit_records()
        res = compare_dict_contained(output, contain_dict)
        Assertion.assert_equal(res, True, "ERR: check supplemental auditing records failed")


# check snmp configure in audit log.
class TestBaseLog_30(Test):
    uuid = "SOSAIOT-TC-55281"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_enable_snmp_for_X2(self):
        static_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
        }
        res = interfacev4api.config_interface(**static_dict)
        Assertion.assert_equal(res, True, "ERR: enable snmp for x2 failed")

    def test_02_check_x2_config_info_in_auditing_log(self):
        contain_dict = {
            'description': " 'Enable SNMP management on this interface' ",
            'old_value': 'disabled',
            'new_value': 'enabled',
        }
        time.sleep(5)
        output = auditapi.show_audit_records()
        res = compare_dict_contained(output, contain_dict)
        Assertion.assert_equal(res, True, "ERR: check snmp in auditing records failed")


# check disable the auditing records in diag.
class TestBaseDisable_41(Test):
    uuid = "SOSAIOT-TC-55283"
    description = show_testcase_info(TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_disable_auditing_records_in_diag(self):
        diag_cfs = {'stream': 'enableCfgAuditing='''}
        res = diagapi.config_raw_api(**diag_cfs)
        Assertion.assert_equal(res, True, "ERR: disable auditing records in diag failed")

    def test_02_disable_snmp_for_X2(self):
        static_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_snmp': False,
        }
        res = interfacev4api.config_interface(**static_dict)
        Assertion.assert_equal(res, True, "ERR: disable snmp for x2 failed")

    def test_03_check_x2_config_info_in_auditing_log(self):
        contain_dict = {
            'description': " 'Disable SNMP management on this interface' ",
            'old_value': 'enable',
            'new_value': 'disable',
        }
        time.sleep(5)
        output = auditapi.show_audit_records()
        res = compare_dict_contained(output, contain_dict)
        Assertion.assert_equal(res, False, "ERR: check snmp in auditing records failed")


# check enable audit in cli.
class TestBaseEnable_44(Test):
    uuid = "SOSAIOT-TC-55284"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_enable_auditing_records_in_cli(self):
        res = auditlogscli.enable_audit_log()
        Assertion.assert_equal(res, True, "ERR: enable auditing records in cli failed")

    def test_02_check_auditing_records_option_in_diag(self):
        output = diagapi.get_diag_info()
        res = True if output['data']['auditing_records']['enableCfgAuditing'] == 'CHECKED' else False
        Assertion.assert_equal(res, True, "ERR: check diag auditing_records option failed")


# check X2 configure info after reboot
class TestBaseReboot_47(Test):
    uuid = "SOSAIOT-TC-55285"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_restart_DUT(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_02_check_snmp_configure_in_audit_log(self):
        TestBaseDisable_41().test_03_check_x2_config_info_in_auditing_log()


# check exp configure in audit log
class TestBaseEXP_56(Test):
    uuid = "SOSAIOT-TC-55286"
    jira = 'GEN8-5560'
    description = show_testcase_info(TESTPLAN, '56', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '56')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_enable_snmp_for_X4(self):
        static_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mgmt_snmp': True,
        }
        output = interfacev4api.config_interface(**static_dict)
        Assertion.assert_equal(output, True, "ERR: enable snmp for x4 failed")

    def test_02_export_fw_settings(self):
        output = settingapi.export_setting_exp()
        Assertion.assert_equal(output, True, "ERR: export fw settings failed")

    def test_03_unassign_for_X4(self):
        output = interfacev4api.unassign_interface(interface='X4')
        Assertion.assert_equal(output, True, "ERR: unassigned x4 failed")

    def test_04_import_fw_settings(self):
        output = settingapi.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(output, True, "ERR: import settings failed")

    @repeat_method(3)
    def test_05_check_import_config_in_auditing_log(self):
        contain_dict = {
            'description': "Import Settings",
            'new_value': 'test.exp',
            'status': 'Succeeded',
            'user': 'admin',
        }
        time.sleep(10)
        output = auditapi.show_audit_records()
        logger.info(output)
        res = compare_dict_contained(output, contain_dict)
        Assertion.assert_equal(res, True, "ERR: check import config in auditing records failed")


