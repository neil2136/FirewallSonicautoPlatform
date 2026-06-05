import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_BVT/testcases')


def suite():
    testcases_list = [
       # 'config.init_testbed.TestRestoreDUT', MOVED ALL CASES TO SMOKE_TEST FOLDER
       # 'config.init_testbed.TestUploadFirmware',
       # 'definition.conf_fw.TestConfigTB',
       #  'SSO_REST_API_BVT.Copy_file',
       #  'SSO_REST_API_BVT.SSO_REST_API_BVT_1',
       #  'SSO_REST_API_BVT.SSO_REST_API_BVT_2',
       #  'SSO_REST_API_BVT.SSO_REST_API_BVT_3',
       #  'SSO_REST_API_BVT.SSO_REST_API_BVT_4',
       #  'SSO_REST_API_BVT.SSO_REST_API_BVT_5',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sbharaj@sonicwall.com'
    # cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
