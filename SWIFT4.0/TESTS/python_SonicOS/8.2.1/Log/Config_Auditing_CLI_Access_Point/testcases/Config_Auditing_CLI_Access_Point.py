from settings import *
from utils import *
from case_details import *


@paramunittest.parametrized(
    {'uuid': 'SOSAIOT-TC-54871'},
    {'uuid': 'SOSAIOT-TC-54872'},
    {'uuid': 'SOSAIOT-TC-54873'},
    {'uuid': 'SOSAIOT-TC-54874'},
    {'uuid': 'SOSAIOT-TC-54875'},
    {'uuid': 'SOSAIOT-TC-54876'},
    {'uuid': 'SOSAIOT-TC-54877'},
    {'uuid': 'SOSAIOT-TC-54878'},
    {'uuid': 'SOSAIOT-TC-54887'},
    {'uuid': 'SOSAIOT-TC-54888'},
    {'uuid': 'SOSAIOT-TC-54889'},
    {'uuid': 'SOSAIOT-TC-54891'},
    {'uuid': 'SOSAIOT-TC-54892'},
    {'uuid': 'SOSAIOT-TC-54893'},
    {'uuid': 'SOSAIOT-TC-54894'},
    # {'uuid': 'SOSAIOT-TC-54895'},
    # {'uuid': 'SOSAIOT-TC-54896'},
    # {'uuid': 'SOSAIOT-TC-54897'},
    # {'uuid': 'SOSAIOT-TC-54898'},
    # {'uuid': 'SOSAIOT-TC-54899'},
)
class TestConfig_Auditing_CLI_Selected_TC01(Test):
    def setParameters(self, uuid):
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Configure_Via_CLI(self):
        logger.info('Clear related logs')
        clear_log_message()
        rs = send_cli_command(case_dict[self.uuid]['cli'])
        Assertion.assert_equal(rs, True, f"ERR: CLI configure failed,CLI is {case_dict[self.uuid]['cli']}")

    @repeat_method(5)
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=case_dict[self.uuid]['syslog_check'], output=syslog, mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: test_02_verify_syslog_on_PC1 failed")

    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', case_dict[self.uuid]['auditlog_check'])
        Assertion.assert_equal(rc, True, "ERR: test_03_verify_auditing_log failed")

    def test_04_verify_log(self):
        rc = verify_result('log', case_dict[self.uuid]['log_check'])
        Assertion.assert_equal(rc, True, "ERR: test_04_verify_log failed")

    def test_05_verify_snmp(self):
        rc = verify_result('snmp', case_dict[self.uuid]['snmplog_check'])
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")
