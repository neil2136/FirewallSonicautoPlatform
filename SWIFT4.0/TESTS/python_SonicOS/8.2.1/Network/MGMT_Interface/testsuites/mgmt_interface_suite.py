import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/MGMT_Interface')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/MGMT_Interface/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/MGMT_Interface/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'mgmt_interface.Test_01_Zone_Check_1',
        'mgmt_interface.Test_02_Static_Mode_Check_2',
        'mgmt_interface.Test_03_MGMT_IP_Check_5',
        'mgmt_interface.Test_MGMT_Route_Check_6'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
