from definition.settings import *


class Test_01_Cli_Config_Audit(Test):
    uuid = "SOSAIOT-TC-55205"
    description= show_testcase_info(TESTPLAN, '1514955', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514955')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_export_audit_with_name(self):
        cmds = ['config','export audit csv ftp ftp://root:password@192.168.168.200/audit1.csv','commit']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        out2 = PC1.send_command("ls /root/audit1.csv")
        if "audit1.csv" in out2:
            rc &= True
            logger.info("check exported audit success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: export audit with name and check it fail.")

    def test_02_export_audit_with_no_name(self):
        cmds = ['config','export audit csv ftp ftp://root:password@192.168.168.200/','commit']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        out2 = PC1.send_command("ls /root/")
        if re.search(r"audit_log.*\.csv",out2):
            rc &= True
            logger.info("check exported audit success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: export audit with name and check it fail.")


class Test_02_Cli_Config_Audit(Test):
    uuid = "SOSAIOT-TC-55206"
    description= show_testcase_info(TESTPLAN, '1514956', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514956')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_export_audit_txt(self):
        cmds = ['config','export audit txt ftp ftp://root:password@192.168.168.200/auditRecords.txt','commit']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        out2 = PC1.send_command("ls /root/auditRecords.txt")
        if "auditRecords.txt" in out2:
            rc &= True
            logger.info("check exported audit success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: export audit txt and check it fail.")


class Test_03_Cli_Config_Audit(Test):
    uuid = "SOSAIOT-TC-55207"
    description= show_testcase_info(TESTPLAN, '1514957', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514957')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_export_audit_via_scp(self):
        cmds = ['config','export audit csv scp scp://root:password@192.168.168.200/auditRecordsScp.wri','commit']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        out2 = PC1.send_command("ls /root/auditRecordsScp.wri")
        if "auditRecordsScp.wri" in out2:
            rc &= True
            logger.info("check exported audit success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: export audit via scp and check it fail.")


class Test_04_Cli3_Diag(Test):
    uuid = "SOSAIOT-TC-48566"
    description= show_testcase_info(TESTPLAN, '2403290', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2403290')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_diag_show_multicore(self):
        cmds = ['diag show multicore']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        if   "Packet Rate (pps)" in out1 and 'Bit Rate (kbps)' in out1:
            rc &= True
            logger.info("check multicore success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check diag show multicore it fail.")


class Test_05_Cli3_Diag(Test):
    uuid = "SOSAIOT-TC-48567"
    description= show_testcase_info(TESTPLAN, '2403291', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2403291')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_diag_show_cpu(self):
        cmds = ['diag show cpu']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        if   "MultiCore Process History for Last Hour (60 minutes ago --> now, kbps)" in out1 :
            rc &= True
            logger.info("check cpu info success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check diag show cpu it fail.")


class Test_06_Cli3_Diag(Test):
    uuid = "SOSAIOT-TC-48568"
    description= show_testcase_info(TESTPLAN, '3128242', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3128242')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_diag_show_memory(self):
        cmds = ['diag show memory verbose']
        rc,out1 = fw_cli.do_cli_commands(commands=cmds, tag=1)
        if   "Memory Summary" in out1 and 'Total allocated' in out1:
            rc &= True
            logger.info("check memory info success!")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check diag show memory verbose it fail.")


class Test_07_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55266"
    description= show_testcase_info(TESTPLAN, '1526114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526114')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_right_value(self):
        rc = log_automation.email_audit_settings(audit='123456@163.com')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_address']['audit']=='123456@163.com':
            rc &= True
            logger.info('check audit email success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config right value and check it fail.")

    def test_02_config_wrong_value(self):
        res = log_automation.email_audit_settings(audit='12345',msg=True)
        rc = True if not res[0] and 'invalid format' in res[1]['status']['info'][0]['message'] else False
        Assertion.assert_equal(rc, True, f"ERR: config wrong value and check it fail.")


class Test_08_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55269"
    description= show_testcase_info(TESTPLAN, '1526117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526117')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_period_full(self):
        rc = log_automation.email_audit_settings(send_audit='when_full')
        res = log_automation.show_log_automation()
        if res['log']['automation']['send_audit']['when_full']:
            rc &= True
            logger.info('check the period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period full and check it fail.")

    def test_02_config_period_weekly(self):
        rc = log_automation.email_audit_settings(send_audit='weekly',hour=13,minute=33,week='fri')
        res = log_automation.show_log_automation()
        ref = res['log']['automation']['send_audit']['weekly']['fri']
        if ref['hour']==13 and ref['minute']==33:
            rc &= True
            logger.info('check the  period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period weekly and check it fail.")

    def test_03_config_period_daily(self):
        rc = log_automation.email_audit_settings(send_audit='daily',hour=0,minute=0)
        res = log_automation.show_log_automation()
        ref = res['log']['automation']['send_audit']['daily']
        if ref['hour']==0 and ref['minute']==0 :
            rc &= True
            logger.info('check the  period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period weekly and check it fail.")

    def test_04_config_period_wrong_value(self):
        res = log_automation.email_audit_settings(send_audit='daily',hour=24,minute=0,msg=True)
        if not res[0] and 'Value or string length(24) out of bounds (max = 23)' in res[1]['status']['info'][0]['message'] :
            rc = True
            logger.info('check the  period wrong msg success!!')
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: config period wrong value and check msg  fail.")


class Test_09_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55270"
    description= show_testcase_info(TESTPLAN, '1526118', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526118')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_right_value(self):
        rc = log_automation.email_audit_settings(audit='123456@163.com')
        Assertion.assert_equal(rc, True, f"ERR: config right value and check it fail.")

    def test_02_Export_and_Import_Prefs(self):
        logger.info(" {} ".center(20, '-').format('Export and Import Prefs '))
        rc = Lsetting.export_setting_exp(filepath='/tmp/prefs_module')
        time.sleep(5)
        rc &= log_automation.email_audit_settings(audit='112233@163.com')
        rc &= Lsetting.import_setting_exp(filepath='/tmp/prefs_module')
        Assertion.assert_equal(rc, True, "ERR: Export and Import Prefs failed") 

    def test_03_check_audit_config(self):
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_address']['audit']=='123456@163.com':
            rc = True
            logger.info('check audit email success!!')
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:  check audit value fail.")


class Test_10_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55271"
    description= show_testcase_info(TESTPLAN, '1526119', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526119')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_format_audit(self):
        rc = log_automation.email_audit_settings(email_format_audit='plain_text')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['plain_text']:
            rc &= True
            logger.info('check the format audit plain text  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit and check it fail.")

    def test_02_config_format_audit(self):
        rc = log_automation.email_audit_settings(email_format_audit='csv')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['csv']:
            rc &= True
            logger.info('check the  format audit csv  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit and check it fail.")

    def test_03_config_format_audit(self):
        rc = log_automation.email_audit_settings(email_format_audit='html')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['html'] :
            rc &= True
            logger.info('check the  format audit html  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit csv and check it fail.")


class Test_11_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55272"
    description= show_testcase_info(TESTPLAN, '1526120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526120')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_right_value_via_cli(self):
        rc,_ = logAuto_cli.cfg_email_address(type="audit", email ='778899@163.com')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_address']['audit']=='778899@163.com':
            rc &= True
            logger.info('check audit email success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config right value and check it fail.")


class Test_12_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55273"
    description= show_testcase_info(TESTPLAN, '1526121', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526121')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_period_full(self):
        rc,_ = logAuto_cli.cfg_email_period(period='when-full')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        if res['log']['automation']['send_audit']['when_full']:
            rc &= True
            logger.info('check the period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period full and check it fail.")

    def test_02_config_period_weekly(self):
        rc,_ = logAuto_cli.cfg_email_period(period='weekly',hour=23,minute=59,week='sun')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        ref = res['log']['automation']['send_audit']['weekly']['sun']
        if ref['hour']==23 and ref['minute']==59:
            rc &= True
            logger.info('check the  period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period weekly and check it fail.")

    def test_03_config_period_daily(self):
        rc,_ = logAuto_cli.cfg_email_period(period='daily',hour=15,minute=30)
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        ref = res['log']['automation']['send_audit']['daily']
        if ref['hour']==15 and ref['minute']==30 :
            rc &= True
            logger.info('check the  period  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config period weekly and check it fail.")


class Test_13_Email_Audit_Records(Test):
    uuid = "SOSAIOT-TC-55274"
    description= show_testcase_info(TESTPLAN, '1526122', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1526122')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_format_audit(self):
        rc,_ = logAuto_cli.cfg_email_format_audit(format='plain-text')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['plain_text']:
            rc &= True
            logger.info('check the format audit plain text  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit and check it fail.")


    def test_02_config_format_audit(self):
        rc,_ = logAuto_cli.cfg_email_format_audit(format='csv')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['csv']:
            rc &= True
            logger.info('check the  format audit csv  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit and check it fail.")

    def test_03_config_format_audit(self):
        rc,_ = logAuto_cli.cfg_email_format_audit(format='html')
        logger.info(f'------{rc},{_}')
        res = log_automation.show_log_automation()
        if res['log']['automation']['email_format_audit']['html'] :
            rc &= True
            logger.info('check the  format audit html  success!!')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: config format audit csv and check it fail.")
