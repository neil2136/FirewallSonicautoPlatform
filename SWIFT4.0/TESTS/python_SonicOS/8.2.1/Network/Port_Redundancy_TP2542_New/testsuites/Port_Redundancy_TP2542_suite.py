import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Port_Redundancy_TP2542_New')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_env.TestConfigTB1',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_07',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_08',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_09',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_10',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_11',
        'testcases.Port_Redundancy_TP2542.Test_Port_Redundancy_12',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'gkatti@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
