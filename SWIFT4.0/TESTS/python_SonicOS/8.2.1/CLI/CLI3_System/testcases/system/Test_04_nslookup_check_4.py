from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_04_nslookup_check_4:
    uuid = "SOSAIOT-TC-48449"
    description = show_testcase_info(TESTPLAN, "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_nslookup_check(self):
        rs = nslookupcli.nslookup('www.baidu.com')
        logger.info('nslookup result: {}'.format(rs))
        output = 'www.baidu.com' in rs
        Assertion.assert_equal(output, True, "ERR: nslookup failed")