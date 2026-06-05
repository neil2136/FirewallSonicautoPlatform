# _author_ = Rohit Sahu
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enhancements_new_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enhancements_new_2/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'sso.NonTC',
        'sso.TC_03_Auto_Added_NAT_Policy_And_Access_Rule',
        'sso.TC_06_Auto_Delete_Service_Object_After_Agent_Deletion', 
        'sso.TC_07_Auto_Delete_Access_Rule_After_Agent_Deletion',
        'sso.TC_08_Import_Configuration_File',
        'sso.TC_09_Agents_Configured_In_Diff_Zones'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

