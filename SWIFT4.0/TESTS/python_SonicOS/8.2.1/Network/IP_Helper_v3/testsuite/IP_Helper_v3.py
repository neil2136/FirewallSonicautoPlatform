import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_v3/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from definition.conf_tb import *
from testcases.ip_helper_v3 import *



def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
        'definition.conf_tb',
       'testcases.ip_helper_v3',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



