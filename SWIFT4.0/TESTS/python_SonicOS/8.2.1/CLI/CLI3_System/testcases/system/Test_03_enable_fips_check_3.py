from settings import *
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
        Assertion.assert_equal(True, True, "ERR: show test case info failed")