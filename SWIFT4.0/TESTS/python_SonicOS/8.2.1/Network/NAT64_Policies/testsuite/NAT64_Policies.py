import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT64_Policies')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT64_Policies/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/NAT64_Policies/testcase')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from definition.config_tb import *
from testcase.nat64_policies import *


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.config_tb',
        'testcase.nat64_policies',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



