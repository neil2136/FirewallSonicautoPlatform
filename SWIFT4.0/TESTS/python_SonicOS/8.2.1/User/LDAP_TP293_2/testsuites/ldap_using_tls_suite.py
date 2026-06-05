import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_TP293_2')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_TP293_2/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_using_tls.ldap_config',

        'ldap_using_tls.TC01_GUI_Enable_RADIUS_to_LDAP_Relay',
        'ldap_using_tls.TC02_Import_user_from_LDAP_on_the_Local_Users_page',
        'ldap_using_tls.TC03_Import_user_from_LDAP_on_Users_tab_of_the_LDAP_configuration',
        'ldap_using_tls.TC04_LDAP_login_of_Sonicwall_Administrator_using_empty_password',
        'ldap_using_tls.TC05_GUI_LDAP_Configuration_Settings_Login_Password_field',
        'ldap_using_tls.TC06_GEN7_37403_Firewall_is_not_accepting_LDAP_server_name_that_begins_with_a_number',
        'ldap_using_tls.TC07_GUI_LDAP_Configuration_Settings_Use_TLS_SSL',
        'ldap_using_tls.TC08_GUI_LDAP_Configuration_Settings_Require_valid_certificate_from_server',
        'ldap_using_tls.TC09_GUI_LDAP_Configuration_Settings_Local_certificate_for_TLS',
        'ldap_using_tls.TC10_GUI_LDAP_Configuration_Schema_LDAP_Schema_list',
        'ldap_using_tls.TC11_GUI_LDAP_Configuration_Schema_Microsoft_Active_Directory_selected',
        'ldap_using_tls.TC12_GUI_Select_LDAP',
        'ldap_using_tls.TC13_GUI_LDAP_Configuration_Directory_Primary_domain_field',
        'ldap_using_tls.TC14_GUI_LDAP_Configuration_Directory_DNS_for_user_trees_Add',
        'ldap_using_tls.TC15_GUI_LDAP_Configuration_Directory_DNs_for_user_trees_Remove',
        'ldap_using_tls.TC16_GUI_Select_LDAP_Local_Users',
        'ldap_using_tls.TC17_GUI_LDAP_Configuration_LDAP_Users_Default_LDAP_User_Group_Select',
        'ldap_using_tls.TC18_GUI_LDAP_Configuration_LDAP_Users_Default_LDAP_User_Group_Create_a_new_user_group',
        'ldap_using_tls.TC19_GUI_LDAP_Configuration_Settings_Name_or_IP_Address_field_Use_IP_address',
        'ldap_using_tls.TC20_Functional_Connection_to_LDAP_server_TLS_is_used',
        'ldap_using_tls.TC21_LDAP_server_is_successful_when_TLS_is_used_and_a_server_CA_certificate_is_not_required',
        'ldap_using_tls.TC22_Functional_TLS_is_used_sending_Start_TLS_request_is_required',
        'ldap_using_tls.TC23_Functional_Microsoft_Active_Directory_schema_is_used',
        'ldap_using_tls.TC24_GEN8_3585_LDAP_user_with_wrong_domain_should_not_be_authed_successfully',
        'ldap_using_tls.TC25_Correct_user_password_with_the_wrong_domain_should_not_be_authed_successfully',
                  
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
