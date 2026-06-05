import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'definition.init_conf_fw.Test_init_RemoteFW',
        'testcases.ula.TestConfigureULA',
        'testcases.ula.TC01_Access_the_Internet_from_the_LAN_allow_All',
        'testcases.ula.TC02_User_authentication_settings_disable_Display_user_login_info_since_last_login',
        'testcases.ula.TC03_User_Web_Login_Settings_check_default_settings',
        'testcases.ula.TC04_User_Web_Login_Settings_Boundry_and_negative_test_for_Show_authentication_pag_input',
        'testcases.ula.TC05_User_Web_Login_Settings_set_show_authentication_page_for_different_minutes_and_test_function',
        'testcases.ula.TC06_User_Web_Login_Settings_redirect_the_browser',
        'testcases.ula.TC08_User_Web_Login_Settings_Policy_Banner_content_preview',
        'testcases.ula.TC09_User_Web_Login_Settings_enable_Start_With_Policy_Banner_Before_Login_Window',
        'testcases.ula.TC10_User_Web_Login_Settings_disable_Start_With_Policy_Banner_Before_Login_Window',
        'testcases.ula.TC11_User_Web_Login_Settings_Policy_Banner_content_edit',
        'testcases.ula.TC12_User_Web_Login_Settings_Policy_Banner_content_example_template',
        'testcases.ula.TC13_User_Session_Settings_for_Web_Login_disable_Enable_login_session_limit_for_web_logins',
        'testcases.ula.TC14_User_Session_Settings_for_Web_Login_enable_Enable_login_session_limit_for_web_logins',
        'testcases.ula.TC15_User_Session_Settings_for_Web_Login_Boundary_negative_test_for_Login_session_limit',
        'testcases.ula.TC16_User_Session_Settings_for_Web_Login_function_test_for_Login_session_limit',
        'testcases.ula.TC17_User_Session_Settings_for_Web_Login_disable_Show_user_login_status_window',
        'testcases.ula.TC18_User_Session_Settings_for_Web_Login_Show_user_login_status_window',
        'testcases.ula.TC19_Session_Settings_for_Web_Login_Enable_disconnected_user_detection',
        'testcases.ula.TC20_User_Session_Settings_for_Web_Login_disable_disconnected_user_detection',
        'testcases.ula.TC21_User_status_page_check_default_settings',
        'testcases.ula.TC22_User_status_page_enable_include_inactive_users',
        'testcases.ula.TC23_User_status_page_enable_show_unauthenticated_users',
        'testcases.ula.TC24_User_status_page_set_different_start_value_for_items_to_view',
        'testcases.ula.TC25_User_status_page_check_user_status_for_logged_in_users',
        'testcases.ula.TC26_User_status_page_logout_selected_users',
        'testcases.ula.TC27_User_status_page_user_counts_button',
        'testcases.ula.TC29_User_Logout_Login_session_limit_expired',
        'testcases.ula.TC30_Relogin_after_Login_session_limit_expired',

]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    
    st = UnittestSuite(sys.argv, suite())
    st.run()
