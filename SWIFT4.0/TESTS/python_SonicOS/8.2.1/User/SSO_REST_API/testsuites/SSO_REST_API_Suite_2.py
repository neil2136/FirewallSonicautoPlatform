import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_REST_API')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_REST_API/testcases/SSO_API_TWO')


def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
       'definition.conf_fw.TestConfigTB',
       'SSO_REST_API_TWO.Copy_file',
        'SSO_REST_API_TWO.SSO_REST_API_1',
        'SSO_REST_API_TWO.SSO_REST_API_2',
        'SSO_REST_API_TWO.SSO_REST_API_3',
        'SSO_REST_API_TWO.SSO_REST_API_4',
        'SSO_REST_API_TWO.SSO_REST_API_5',
        'SSO_REST_API_TWO.SSO_REST_API_6',
        'SSO_REST_API_TWO.SSO_REST_API_7',
        'SSO_REST_API_TWO.SSO_REST_API_8',
        'SSO_REST_API_TWO.SSO_REST_API_9',
        'SSO_REST_API_TWO.SSO_REST_API_10'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sbharaj@sonicwall.com'
    # cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
