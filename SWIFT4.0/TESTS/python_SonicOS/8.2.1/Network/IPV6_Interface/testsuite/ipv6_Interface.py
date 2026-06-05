import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from testcases.ipv6_Interface import *


def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
       'testcases.ipv6_Interface',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

