import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_IP_Helper')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_IP_Helper/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_IP_Helper/testcases')
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'initial_config.TestConfigFW',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_01',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_02',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_03',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_04',
        'api_iphelper_smoke.Test_API_IP_helper_Smoke_05',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
