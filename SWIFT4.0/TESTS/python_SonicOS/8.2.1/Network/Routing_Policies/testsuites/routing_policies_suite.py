import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Routing_Policies/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Routing_Policies')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'routing_policies.Test_01_Routing_Policies',
        'routing_policies.Test_02_Routing_Policies',
        'routing_policies.Test_03_Routing_Policies',
        'routing_policies.Test_04_Routing_Policies',
        'routing_policies.Test_05_Routing_Policies',
        'routing_policies.Test_06_Routing_Policies',
        'routing_policies.Test_07_Routing_Policies',
        'routing_policies.Test_08_Routing_Policies',
        'routing_policies.Test_09_Routing_Policies',
        'routing_policies.Test_10_Routing_Policies',
        'routing_policies.Test_11_Routing_Policies',
        'routing_policies.Test_12_Routing_Policies',
        'routing_policies.Test_13_Routing_Policies',
        'routing_policies.Test_14_Routing_Policies',
        'routing_policies.Test_15_Routing_Policies',
        'routing_policies.Test_16_Routing_Policies',
        'routing_policies.Test_17_Routing_Policies',
        'routing_policies.Test_18_Routing_Policies',
        'routing_policies.Test_19_Routing_Policies',
        'routing_policies.Test_20_Routing_Policies',
        'routing_policies.Test_21_Routing_Policies',
        'routing_policies.Test_22_Routing_Policies',
        'routing_policies.Test_23_Routing_Policies',
        'routing_policies.Test_24_Routing_Policies',
        'routing_policies.Test_25_Routing_Policies',
        'routing_policies.Test_26_Routing_Policies',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
