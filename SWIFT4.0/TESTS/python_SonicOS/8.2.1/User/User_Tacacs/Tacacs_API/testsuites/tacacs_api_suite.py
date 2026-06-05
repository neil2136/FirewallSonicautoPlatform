import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Tacacs/Tacacs_API/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Tacacs/Tacacs_API/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/User_Tacacs/Tacacs_API/definition/')

def suite():
    testcases_list = [

        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'tacacs_api.Test_API_Tacacs_base_01',
        'tacacs_api.Test_API_Tacacs_base_02',
        'tacacs_api.Test_API_Tacacs_base_03',
        'tacacs_api.Test_API_Tacacs_base_04',
        'tacacs_api.Test_API_Tacacs_base_05',
        'tacacs_api.Test_API_Tacacs_base_06',
        'tacacs_api.Test_API_Tacacs_base_07',
        'tacacs_api.Test_API_Tacacs_base_08',
        'tacacs_api.Test_API_Tacacs_base_09',
        'tacacs_api.Test_API_Tacacs_base_10',
        'tacacs_api.Test_API_Tacacs_base_11',
        'tacacs_api.Test_API_Tacacs_base_12',
        'tacacs_api.Test_API_Tacacs_base_13',
        'tacacs_api.Test_API_Tacacs_base_14',
        'tacacs_api.Test_API_Tacacs_base_15',
        'tacacs_api.Test_API_Tacacs_base_16',
        'tacacs_api.Test_API_Tacacs_base_17',
        'tacacs_api.Test_API_Tacacs_base_18',
        'tacacs_api.Test_API_Tacacs_base_19',
        'tacacs_api.Test_API_Tacacs_base_20',
        'tacacs_api.Test_API_Tacacs_base_21',
        'tacacs_api.Test_API_Tacacs_base_22',
        'tacacs_api.Test_API_Tacacs_base_23',
        'tacacs_api.Test_API_Tacacs_base_24',
        'tacacs_api.Test_API_Tacacs_base_25',
        'tacacs_api.Test_API_Tacacs_base_26',
        'tacacs_api.Test_API_Tacacs_base_27',
        'tacacs_api.Test_API_Tacacs_base_28',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'pagarwal@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

