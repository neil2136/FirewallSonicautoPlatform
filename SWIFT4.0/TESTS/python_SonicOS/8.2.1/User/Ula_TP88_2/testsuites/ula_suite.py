import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2')


def suite():
    testcases_list = [
       
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'definition.init_conf_fw.Test_init_RemoteFW',
        'testcases.ula.TestConfigureULA',
        'testcases.ula.TC01_Access_the_Internet_from_the_Custom_Zone_allow_All',
        'testcases.ula.TC02_Access_the_Internet_from_the_Custom_Zone_allow_Administrator',
        'testcases.ula.TC03_Access_the_Internet_from_the_Custom_Zone_allow_Everyone',
        'testcases.ula.TC14_Acceptable_Use_Policy_is_displayed_on_login_from_the_Custom_Zone',
        'testcases.ula.TC07_Access_the_Internet_from_the_Custom_Zone_allow_a_user',
        'testcases.ula.TC04_Access_the_Internet_from_the_Custom_Zone_allow_a_group',
        'testcases.ula.TC05_Access_the_Internet_from_the_Custom_Zone_allow_a_supergroup',
        'testcases.ula.TC08_Deny_access_to_the_Internet_from_the_Custom_Zone',
        'testcases.ula.TC06_Access_the_Internet_from_the_LAN_allow_Administrator',
        'testcases.ula.TC12_Acceptable_Use_Policy_is_displayed_on_login_from_the_LAN',
        'testcases.ula.TC13_Acceptable_Use_Policy_is_displayed_on_login_from_the_WAN',
        'testcases.ula.TC09_Access_the_Internet_from_the_LAN_allow_Everyone',
        'testcases.ula.TC10_Access_the_Internet_from_the_LAN_allow_a_group',
        'testcases.ula.TC11_Access_the_Internet_from_the_LAN_allow_a_supergroup',
        'testcases.ula.TC15_User_attempts_to_bypass_Acceptable_Use_Policy',
        'testcases.ula.TC16_Acceptable_Use_Policy_preview',
        'testcases.ula.TC17_Login_session_limit_changed_by_administrator',
        'testcases.ula.TC18_User_Logout_select_the_Logout_button',
        'testcases.ula.TC19_User_Logout_check_logs',
        'testcases.ula.TC20_Cancel_logout',
        'testcases.ula.TC21_User_logout_by_administrator',
        'testcases.ula.TC22_Cancel_logout',
        'testcases.ula.TC23_Relogin_after_logout',
        'testcases.ula.TC24_User_Logout_Inactivity_timer_expired',
        'testcases.ula.TC25_Inactivity_timer_is_reset_by_selecting_click_here_in_the_warning_message',
        'testcases.ula.TC26_Inactivity_timer_is_reset_by_generating_traffic',
        'testcases.ula.TC27_Login_session_limit_changed_by_user',
        'testcases.ula.TC28_Login_session_unlimited_by_administrator',
        'testcases.ula.TC29_Deny_access_to_the_Internet_from_the_LAN',
        'testcases.ula.TC30_Login_session_limited_by_user',
        'testcases.ula.TC31_user_status_page_logout_selected_users',


         

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()