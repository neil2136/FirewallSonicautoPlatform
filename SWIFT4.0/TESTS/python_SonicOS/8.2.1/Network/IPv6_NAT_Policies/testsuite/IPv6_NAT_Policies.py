import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_NAT_Policies/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from definition.conf_tb import *
from testcases.ipv6_nat_policies import *


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_tb',
        'testcases.ipv6_nat_policies',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



