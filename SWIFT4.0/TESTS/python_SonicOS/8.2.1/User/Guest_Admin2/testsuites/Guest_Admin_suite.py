import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'Guest_admin.Guest_admin_001',
        'Guest_admin.Guest_admin_002',
        'Guest_admin.Guest_admin_003',
        'Guest_admin.Guest_admin_004',
        'Guest_admin.Guest_admin_005'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
