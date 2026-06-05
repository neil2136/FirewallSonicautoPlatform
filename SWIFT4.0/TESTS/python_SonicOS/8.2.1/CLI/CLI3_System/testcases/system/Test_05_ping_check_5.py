from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_05_ping_check_5:
    uuid = "SOSAIOT-TC-48450"
    description = show_testcase_info(TESTPLAN, "5", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_ping_check(self):
        rs = pingcli.ping('www.baidu.com')
        logger.info('ping result: {}'.format(rs))
        output = 'www.baidu.com' in rs
        Assertion.assert_equal(output, True, "ERR: ping failed")