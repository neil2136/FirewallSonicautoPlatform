from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_06_configure_schedule_7:
    uuid = "SOSAIOT-TC-48451"
    description = show_testcase_info(TESTPLAN, "6", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_schedule(self):
        rs = schedulecli.configure_schedule('daily', '08:00', 'www.baidu.com')
        logger.info('configure schedule result: {}'.format(rs))
        showrs = schedulecli.show_schedule()
        logger.info('show schedule result: {}'.format(showrs))
        output = True if 'www.baidu.com' in showrs else False
        Assertion.assert_equal(output, True, "ERR: configure schedule failed")