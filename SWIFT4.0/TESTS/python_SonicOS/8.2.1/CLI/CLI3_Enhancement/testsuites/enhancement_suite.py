# __Author__ = 'xzhan'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Enhancement/')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.enhancement.TestCLI_Enhancement_TC03',
        'testcases.enhancement.TestCLI_Enhancement_TC01',
        'testcases.enhancement.TestCLI_Enhancement_TC02',
        'testcases.enhancement.TestCLI_Enhancement_TC17',
        'testcases.enhancement.TestCLI_Enhancement_TC18',
        'testcases.enhancement.TestCLI_Enhancement_TC06',
        'testcases.enhancement.TestCLI_Enhancement_TC04',
        'testcases.enhancement.TestCLI_Enhancement_TC05',
        'testcases.enhancement.TestCLI_Enhancement_TC19',
        'testcases.enhancement.TestCLI_Enhancement_TC20',
        'testcases.enhancement.Test_NATUUIDTests',
        'testcases.enhancement.TestCLI_Enhancement_TC07',
        'testcases.enhancement.TestCLI_Enhancement_TC08',
        'testcases.enhancement.TestCLI_Enhancement_TC09',
        'testcases.enhancement.TestCLI_Enhancement_TC10',
        'testcases.enhancement.Test_ACLUUIDTests',
        'testcases.enhancement.TestCLI_Enhancement_TC11',
        'testcases.enhancement.TestCLI_Enhancement_TC12',
        'testcases.enhancement.TestCLI_Enhancement_TC13',
        'testcases.enhancement.TestCLI_Enhancement_TC14',
        'testcases.enhancement.TestCLI_Enhancement_TC15',
        'testcases.enhancement.TestCLI_Enhancement_TC16'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
