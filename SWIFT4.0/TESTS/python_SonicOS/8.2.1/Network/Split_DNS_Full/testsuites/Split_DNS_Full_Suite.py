# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Split_DNS_Full')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.split_dns.TestSplitDNS_TC067',
        'testcases.split_dns.TestSplitDNS_TC065',
        'testcases.split_dns.TestSplitDNS_TC095',
        'testcases.split_dns.TestSplitDNS_TC105',
        'testcases.split_dns.TestSplitDNS_TC069',
        'testcases.split_dns.TestSplitDNS_TC068',
        'testcases.split_dns.TestSplitDNS_TC079',
        'testcases.split_dns.TestSplitDNS_TC070',
        'testcases.split_dns.TestSplitDNS_TC072',
        'testcases.split_dns.TestSplitDNS_TC076',
        'testcases.split_dns.TestSplitDNS_TC077',
        'testcases.split_dns.TestSplitDNS_TC094',
        'testcases.split_dns.TestSplitDNS_TC110',
   ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
