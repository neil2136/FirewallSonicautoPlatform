# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/TOS_in_Route_Policies')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.register_fw',
        'definition.init_conf_fw',
        'testcases.tos.TestTOS_TC01',
        'testcases.tos.TestTOS_TC31',
        'testcases.tos.TestTOS_TC02',
        'testcases.tos.TestTOS_TC05',
        'testcases.tos.TestTOS_TC28'


   ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
