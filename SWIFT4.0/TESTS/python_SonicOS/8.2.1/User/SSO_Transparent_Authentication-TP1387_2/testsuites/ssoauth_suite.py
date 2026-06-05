import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Transparent_Authentication-TP1387_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Transparent_Authentication-TP1387_2/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'definition.conf_pc.TestConfigWorkStationClient',
        'ssoauth.NonTC',
        'ssoauth.TC_01_SSO_Login_With_Local_Config_Mechanism',
        'ssoauth.TC_02_SSO_Login_Only_Local_listed_Users',
        'ssoauth.TC_03_SS0_Login_Ldap_configuration_Allow_Only_Local_Listed_Users',
        'ssoauth.TC_04_Login_Session_Limit_Effect_On_SSO_User',
        'ssoauth.TC_05_Sonicwall_SSO_Agent_Is_Used',
        'ssoauth.TC_06_SSO_User_Activation_With_Previous_SSO_Failure',
        'ssoauth.TC_07_Check_SSO_Authentication_In_TSR',
        'ssoauth.TC_08_SSO_Multiple_Connetions_From_User',
        'ssoauth.TC_09_User_Not_Logged_Into_Network_With_CFS_Enabled',
        'ssoauth.TC_10_IPS_Trigger_SSO_Authentication',
        'ssoauth.TC_11_Show_Unauthenticated_Users',
        'ssoauth.TC_12_Timeout_Field_Boundaries',
        'ssoauth.TC_13_Application_Firewall_Triggers_SSO'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

