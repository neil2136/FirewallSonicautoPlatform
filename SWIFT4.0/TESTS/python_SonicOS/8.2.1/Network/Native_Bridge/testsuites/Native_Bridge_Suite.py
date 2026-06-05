# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Native_Bridge/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'testcases.Native_Bridge.TestGUI_TC005',
        'testcases.Native_Bridge.TestFunc_TC034',
        'testcases.Native_Bridge.TestFunc_TC063',
        'testcases.Native_Bridge.TestFunc_TC032',
        'testcases.Native_Bridge.TestFunc_TC073',
        'testcases.Native_Bridge.TestGUI_TC011',
        'testcases.Native_Bridge.TestFunc_TC074',
        'testcases.Native_Bridge.TestFunc_TC036',
        'testcases.Native_Bridge.TestFunc_TC039',
        'testcases.Native_Bridge.TestFunc_TC051',
        'testcases.Native_Bridge.TestFunc_TC052',
        'testcases.Native_Bridge.TestFunc_TC053',
        'testcases.Native_Bridge.TestFunc_TC090',
        'testcases.Native_Bridge.TestFunc_TC084',
        'testcases.Native_Bridge.TestFunc_TC048',
        'testcases.Native_Bridge.TestFunc_TC047',
        'testcases.Native_Bridge.TestFunc_TC041',
   ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
