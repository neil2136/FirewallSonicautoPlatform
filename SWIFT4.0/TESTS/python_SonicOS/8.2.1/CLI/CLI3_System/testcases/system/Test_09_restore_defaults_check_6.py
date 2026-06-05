from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_09_restore_defaults_check_6:
    uuid = "SOSAIOT-TC-48454"
    description = show_testcase_info(TESTPLAN, "9", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_restore_defaults(self):
        rs = admincli.restore_defaults()
        logger.info('restore defaults result: {}'.format(rs))
        showrs = admincli.show_administration()
        logger.info('show admin setting result: {}'.format(showrs))
        output = True if 'default' in showrs else False
        Assertion.assert_equal(output, True, "ERR: restore defaults failed")