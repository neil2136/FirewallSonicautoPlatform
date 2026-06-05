from settings import *
from utils import *


class Test_01_check_audit_display_on_console(Test):
    uuid = "SOSAIOT-TC-55202"
    description = show_testcase_info(TESTPLAN,
                                     "01", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_display_on_console(self):
        cfg = auditlogcli.enable_display_on_console()
        logger.info(
            'enable audit log display on console result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[0], output, 1)

        res = True if cfg and auditlog else False
        Assertion.assert_equal(
            res, True, "error: cannot enable display on console."
        )


class Test_02_check_audit_no_display_on_console(Test):
    uuid = "SOSAIOT-TC-55208"
    description = show_testcase_info(TESTPLAN,
                                     "02", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_no_display_on_console(self):
        cfg = auditlogcli.disable_display_on_console()
        logger.info(
            'disable audit log display on console result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[0], output, 0)
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot disable display on console."
        )


class Test_03_check_audit_supplemental_changes(Test):
    uuid = "SOSAIOT-TC-55209"
    description = show_testcase_info(TESTPLAN,
                                     "03", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_supplemental_changes(self):
        cfg = auditlogcli.enable_supplemental_changes()
        logger.info(
            'enable audit log supplemental changes result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[2], output, 1)
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot enable supplemental changes."
        )


class Test_04_check_audit_no_supplemental_changes(Test):
    uuid = "SOSAIOT-TC-55210"
    description = show_testcase_info(TESTPLAN,
                                     "04", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_supplemental_changes(self):
        cfg = auditlogcli.disable_supplemental_changes()
        logger.info(
            'disable audit log supplemental changes result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[2], output, 0)
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot disable supplemental changes."
        )


class Test_16_check_audit_enable(Test):
    uuid = 'C94CC006-5BE3-11EC-9F4D-ACA9928F55E4'
    description = show_testcase_info(TESTPLAN,
                                     "16", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable(self):
        cfg = auditlogcli.enable_audit_log()
        logger.info('enable audit log result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[1], output, 1)
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot disable audit log."
        )


class Test_17_check_audit_no_enable(Test):
    uuid = '0FF0F6DA-5BE4-11EC-82A7-9FA9928F55E4'
    description = show_testcase_info(TESTPLAN,
                                     "17", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_no_enable(self):
        cfg = auditlogcli.disable_audit_log()
        logger.info('disable audit log result: {}'.format(cfg))

        output = auditlogcli.show_audit_logs()
        auditlog = check_show_audit_log_result(audit_log_list[1], output, 0)
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot disable audit log."
        )


class Test_05_check_log_auto_eaddr(Test):
    uuid = "SOSAIOT-TC-55211"
    description = show_testcase_info(TESTPLAN,
                                     "05", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_email_address(self):
        (cfg, cmd) = auditautocli.cfg_email_address(**log_auto_eaddr)
        logger.info(
            'configure email-address audit email result: {}'.format(cfg))

        output = auditautocli.show_log_automation()
        auditauto = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditauto else False

        Assertion.assert_equal(
            res,
            True,
            "error: cannot configure log automation email address.")


class Test_06_check_log_auto_eformat_csv(Test):
    uuid = "SOSAIOT-TC-55212"
    description = show_testcase_info(TESTPLAN,
                                     "06", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_email_address_csv(self):
        (cfg, cmd) = auditautocli.cfg_email_format_audit(
            e_au_format_list[0])
        logger.info('configure email-format-audit csv result: {}'.format(cfg))

        output = auditautocli.show_log_automation()
        auditlog = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot configure email-format-audit csv."
        )


class Test_07_check_log_auto_eformat_html(Test):
    uuid = "SOSAIOT-TC-55213"
    description = show_testcase_info(TESTPLAN,
                                     "07", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_email_address_html(self):
        (cfg, cmd) = auditautocli.cfg_email_format_audit(
            e_au_format_list[1])
        logger.info('configure email-format-audit html result: {}'.format(cfg))

        output = auditautocli.show_log_automation()
        auditlog = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditlog else False

        Assertion.assert_equal(
            res, True, "error: cannot configure email-format-audit html."
        )
    

class Test_08_check_log_auto_eformat_pt(Test):
    uuid = "SOSAIOT-TC-55214"
    description = show_testcase_info(TESTPLAN,
                                     "08", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_email_address_html(self):
        (cfg, cmd) = auditautocli.cfg_email_format_audit(e_au_format_list[2])
        logger.info(
            'configure email-format-audit plain text result: {}'.format(cfg))

        output = auditautocli.show_log_automation()
        auditauto = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditauto else False

        Assertion.assert_equal(
            res, True, "error: cannot configure email-format-audit plain text.")


class Test_09_check_log_auto_period_daily(Test):
    uuid = "SOSAIOT-TC-55215"
    description = show_testcase_info(TESTPLAN,
                                     "09", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '09')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_period_daily(self):
        log_auto_period['period'] = 'daily'
        (cfg, cmd) = auditautocli.cfg_email_period(**log_auto_period)
        logger.info('configure send-audit daily result: {}'.format(cfg))

        output = auditautocli.show_log_automation()
        auditauto = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditauto else False

        Assertion.assert_equal(
            res, True, "error: cannot configure send-audit daily."
        )


class Test_10_check_log_auto_period_weekly(Test):
    uuid = "SOSAIOT-TC-55203"
    description = show_testcase_info(TESTPLAN,
                                     "10", description=True)['title']
 
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_period_weekly(self):
        log_auto_period['period'] = 'weekly'
        (cfg, cmd) = auditautocli.cfg_email_period(**log_auto_period)
        logger.info('configure send-audit weekly result: {}'.format(cfg))


        output = auditautocli.show_log_automation()
        auditauto = check_log_automation_result(cmd, output) if cmd and cfg else False
        res = True if cfg and auditauto else False

        Assertion.assert_equal(
            res, True, "error: cannot configure send-audit weekly."
        )


class Test_11_check_log_auto_period_full(Test):
    uuid = "SOSAIOT-TC-55204"
    description = show_testcase_info(TESTPLAN,
                                     "11", description=True)['title']

    def test_00_show_testcase_info(self):  
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_period_full(self):
        log_auto_period['period'] = 'when-full'
        (cfg, cmd) = auditautocli.cfg_email_period(**log_auto_period)
        logger.info(f'configure send-audit when-full result: {cfg}, {cmd}')
        output = auditautocli.show_log_automation()
        Assertion.assert_regular(str(output),
                                 'send-audit when-full',
                                 "error: cannot configure send-audit when-full.")

