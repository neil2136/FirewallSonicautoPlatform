from settings import *
from runner.unittest.assertion import Assertion
import logger

class Test_02_configure_administration_2:
    uuid = "SOSAIOT-TC-48448"
    description = show_testcase_info(TESTPLAN, "2", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_administration_http_port(self):
        rs = admincli.http_port(8888)
        logger.info('config http port result: {}'.format(rs))
        showrs = admincli.show_administration_search('match', '8888')
        logger.info('show admin setting result: {}'.format(showrs))
        output = True if 'http-port 8888' in showrs else False
        logger.info(output)
        if output:
            initrs = admincli.http_port(80)
            logger.info('reset http port result: {}'.format(initrs))
        Assertion.assert_equal(output, True, "ERR: modify administrator http port failed")