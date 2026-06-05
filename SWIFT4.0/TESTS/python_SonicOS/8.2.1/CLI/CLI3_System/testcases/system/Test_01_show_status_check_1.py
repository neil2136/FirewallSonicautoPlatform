from settings import *
from runner.unittest.assertion import Assertion
import logger

class TestSystem01ShowStatusCheck1:
    uuid = "SOSAIOT-TC-48447"
    description = show_testcase_info(TESTPLAN, "1", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_status(self):
        rs = statuscli.show_status()
        logger.info('show status result: {}'.format(rs))
        output = 'System Information' in rs
        Assertion.assert_equal(output, True, "ERR: show status failed")