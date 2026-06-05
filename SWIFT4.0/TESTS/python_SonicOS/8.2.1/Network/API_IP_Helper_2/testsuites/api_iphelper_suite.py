import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/API_IP_Helper_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/API_IP_Helper_2/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/API_IP_Helper_2/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/API_IP_Helper_2/definition/')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config.TestConfigFW',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_01',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_02',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_03',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_04',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_05',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_06'
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()