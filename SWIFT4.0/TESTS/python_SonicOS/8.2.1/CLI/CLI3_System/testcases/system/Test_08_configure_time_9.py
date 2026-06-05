from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_08_configure_time_9:
    uuid = "SOSAIOT-TC-48453"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_time(self):
        rs = timecli.configure_time('Asia/Shanghai')
        logger.info('configure time result: {}'.format(rs))
        showrs = timecli.show_time()
        logger.info('show time result: {}'.format(showrs))
        output = 'Asia/Shanghai' in showrs
        Assertion.assert_equal(output, True, "ERR: configure time failed")