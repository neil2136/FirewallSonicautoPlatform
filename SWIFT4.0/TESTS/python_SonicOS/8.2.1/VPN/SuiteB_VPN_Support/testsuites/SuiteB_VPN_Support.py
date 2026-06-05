import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/SuiteB_VPN_Support')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.SuiteB_VPN_Support_TC1_3_5_31',
        'testcases.SuiteB_VPN_Support_TC2_4_6_8',
        'testcases.SuiteB_VPN_Support_TC9_11_13',
        'testcases.SuiteB_VPN_Support_TC10_12_14_16',
        'testcases.SuiteB_VPN_Support_TC20_21_23',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
