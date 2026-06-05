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
        Assertion.assert_equal(output, True, "ERR: show status failed")from settings import *
from runner.unittest.assertion import Assertion
import logger

# skip because of not environment in openstack.
class Test_03_enable_fips_check_3:
    """
    FIPS can not be used in openstack testbad
    """
    uuid = '906f9e4f-1599-469d-be89-6bddb8bde7cb'
    description = show_testcase_info(TESTPLAN, "3", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: nslookup failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: ping failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: configure schedule failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: traceroute failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: configure time failed")from settings import *
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
        Assertion.assert_equal(output, True, "ERR: restore defaults failed")from settings import *
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