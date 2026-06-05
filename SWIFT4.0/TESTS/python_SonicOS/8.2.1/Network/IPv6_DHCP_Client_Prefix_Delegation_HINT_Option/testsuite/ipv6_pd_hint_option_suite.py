# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DHCP_Client_Prefix_Delegation_HINT_Option/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC01',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC09',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC10',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC02',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC03',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC04',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC05',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC06',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC07',
        'testcases.ipv6_pd_hint_option.TestV6PD_Hint_Opt_TC08',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
