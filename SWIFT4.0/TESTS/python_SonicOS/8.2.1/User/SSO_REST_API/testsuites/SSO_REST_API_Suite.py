import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_REST_API/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        
        'SSO_REST_API.Copy_file',
        'SSO_REST_API.SSO_REST_API_1',
        'SSO_REST_API.SSO_REST_API_2',
        'SSO_REST_API.SSO_REST_API_3',
        'SSO_REST_API.SSO_REST_API_4',
        'SSO_REST_API.SSO_REST_API_5',
        'SSO_REST_API.SSO_REST_API_6',
        'SSO_REST_API.SSO_REST_API_7',
        'SSO_REST_API.SSO_REST_API_8',
        'SSO_REST_API.SSO_REST_API_9',
        'SSO_REST_API.SSO_REST_API_10',
        'SSO_REST_API.SSO_REST_API_11',
        'SSO_REST_API.SSO_REST_API_12',
        'SSO_REST_API.SSO_REST_API_13',
        'SSO_REST_API.SSO_REST_API_14',
        'SSO_REST_API.SSO_REST_API_15',
        'SSO_REST_API.SSO_REST_API_16',
        'SSO_REST_API.SSO_REST_API_17',
        'SSO_REST_API.SSO_REST_API_18',
        'SSO_REST_API.SSO_REST_API_19',
        'SSO_REST_API.SSO_REST_API_20',
        'SSO_REST_API.SSO_REST_API_21',
        'SSO_REST_API.SSO_REST_API_22',
        'SSO_REST_API.SSO_REST_API_23',
        'SSO_REST_API.SSO_REST_API_24',
        'SSO_REST_API.SSO_REST_API_25',
        'SSO_REST_API.SSO_REST_API_26',
        'SSO_REST_API.SSO_REST_API_27',
        'SSO_REST_API.SSO_REST_API_28',
        'SSO_REST_API.SSO_REST_API_29'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ujkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
