import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Transparent_Authentication-TP1387')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Transparent_Authentication-TP1387/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',

        'ssoauth.NonTC',
        'ssoauth.TC01_Enable_User_SSO_Settings',
        'ssoauth.TC02_Incorrectly_Formatted_SSO_User_Agent',
        'ssoauth.TC03_Configure_Button_Not_Dimmed_After_Use_LDAP',
        'ssoauth.TC04_Configure_Button_Dimmed_After_Local_Configurations',
        'ssoauth.TC05_Incorrect_Formatted_Polling_Rate_Value',
        'ssoauth.TC06_Test_SSO_Agent_Connectivity',
        'ssoauth.TC07_Test_Set_Workstation_IP_SSO',
        'ssoauth.TC08_Connectivity_Test',
        'ssoauth.TC09_User_Connectivity_Test',
        'ssoauth.TC10_Using_IP_Address_For_Auth_Agent',
        'ssoauth.TC11_Using_FQDN_For_Auth_Agent',
        'ssoauth.TC12_Timeout_Reply_Agent',
        'ssoauth.TC13_Retry_Timeout_Request_Agent',
        'ssoauth.TC14_SSO_Configure_Enabled',
        'ssoauth.TC15_Shared_Key_MisMatch',
        'ssoauth.TC16_Domain_User_Logged_With_Accessing_Resources',
        'ssoauth.TC17_Local_User_Logged_Not_Accessing_Resources',
        'ssoauth.TC18_FQDN_Auth_Agent_Name_Setup',
        'ssoauth.TC19_Auth_Agent_IP_Address',
        'ssoauth.TC20_User_Name_Window_Services',
        'ssoauth.TC21_Adding_Window_Services_Username',
        'ssoauth.TC22_Updating_Port_Number_SSO_Agent',
        'ssoauth.TC23_Adding_Window_Services_Username_Apply_SSO',
        'ssoauth.TC24_Adding_Special_Window_Services_Username',
        'ssoauth.TC25_Edit_Window_Services_Username',
        'ssoauth.TC26_Edit_SSO_Window_Services_User',
        'ssoauth.TC27_Edit_Special_Window_Services_Username',
        'ssoauth.TC28_Remove_Window_Services_Username',
        'ssoauth.TC29_Remove_And_Verify_Window_Services_User',
        'ssoauth.TC30_Agent_Can_Remove_All_Users',
        'ssoauth.TC31_Setting_SSO_Shared_Key',
        'ssoauth.TC32_Age_Out_Inactivity_Timeout',
        'ssoauth.TC33_Age_Timeout_Field_Boundaries',
        'ssoauth.TC34_User_Listed_Checkbox',
        'ssoauth.TC35_SSO_Configuration_Present_In_Prefs',


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
