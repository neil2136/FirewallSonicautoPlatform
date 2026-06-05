import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Interfaces/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Interfaces')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'static_interface.Test_01_Static_Interface',
        'static_interface.Test_02_Static_Interface',
        'static_interface.Test_03_Static_Interface',
        'static_interface.Test_04_Static_Interface',
        'static_interface.Test_05_Static_Interface',
        'static_interface.Test_06_Static_Interface',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
