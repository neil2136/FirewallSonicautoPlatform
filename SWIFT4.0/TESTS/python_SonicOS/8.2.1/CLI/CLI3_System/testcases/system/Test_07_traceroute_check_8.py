from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_07_traceroute_check_8:
    uuid = "SOSAIOT-TC-48452"
    description = show_testcase_info(TESTPLAN, "7", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_traceroute_check(self):
        rs = traceroutecli.traceroute('www.baidu.com')
        logger.info('traceroute result: {}'.format(rs))
        output = 'www.baidu.com' in rs
        Assertion.assert_equal(output, True, "ERR: traceroute failed")