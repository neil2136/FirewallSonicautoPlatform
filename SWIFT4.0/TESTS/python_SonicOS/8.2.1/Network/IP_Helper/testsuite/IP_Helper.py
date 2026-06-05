import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from testcases.ip_helper import *
from definition.conf_tb import *


def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
        'definition.conf_tb',
        'testcases.ip_helper',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



