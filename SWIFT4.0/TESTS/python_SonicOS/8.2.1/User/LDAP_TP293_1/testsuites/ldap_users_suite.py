import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_TP293_1/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_TP293_1')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_users.config_ldap',
        'ldap_users.TC01_GUI_LDAP_is_included_in_Authentication_Method_list',
        'ldap_users.TC02_LDAP_Users_Import_user_groups',
        'ldap_users.TC03_Import_user_All_selected_users',
        'ldap_users.TC04_Import_user_select_specific_user_at_under_from_the_LDAP_server_path',
        'ldap_users.TC05_Functional_LDAP_Configuration_Test_LDAP_user_for_valid_name_password',
        'ldap_users.TC06_Functional_LDAP_Configuration_Test_LDAP_User_with_invalid_name_password',
        'ldap_users.TC07_Functional_LDAP_version_2_is_used',
        'ldap_users.TC08_Functional_Login_password_is_using_incorrect_value',
        'ldap_users.TC09_Functional_Connection_to_LDAP_server_TLS_is_not_used',
        'ldap_users.TC10_Functional_Default_user_group_is_Everyone',
        'ldap_users.TC11_Functional_Default_user_group_is_a_custom_group',
        'ldap_users.TC12_Functional_Allow_only_users_listed_locally',
        'ldap_users.TC13_Functional_LDAP_Local_Users_authentication',
        'ldap_users.TC14_Functional_Use_LDAP_Name',
        'ldap_users.delete_ldap',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users)
    st.run()

