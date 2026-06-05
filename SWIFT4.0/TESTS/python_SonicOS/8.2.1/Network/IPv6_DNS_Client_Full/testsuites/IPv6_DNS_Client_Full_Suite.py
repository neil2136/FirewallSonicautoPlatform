# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DNS_Client_Full')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC03',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC04',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC08',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC09',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC06',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC15',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC13',
        'testcases.IPv6_DNS_Client_Full.TestIPv6DNS_TC14',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
