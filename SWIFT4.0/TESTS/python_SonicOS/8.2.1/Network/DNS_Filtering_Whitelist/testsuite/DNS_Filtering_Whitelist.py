import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

# sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Whitelist/testcase')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Whitelist')


from testcase.dns_filtering_whitelist import *

def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
       'testcase.dns_filtering_whitelist',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

