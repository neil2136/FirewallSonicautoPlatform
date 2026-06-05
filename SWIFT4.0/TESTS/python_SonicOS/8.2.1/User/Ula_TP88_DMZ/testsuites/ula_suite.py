# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ')


def suite():
    testcases_list = [
        'definition.init_conf_fw.Test_init_RemoteFW',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'testcases.ula.TestConfigureULA',
        'testcases.ula.TC04_Access_the_Internet_from_the_DMZ_allow_a_user',
        'testcases.ula.TC05_Deny_access_to_the_Internet_from_the_DMZ',
        'testcases.ula.TC06_Login_Redirect_upon_the_Internet_access_from_the_DMZ',
        'testcases.ula.TC07_Acceptable_Use_Policy_is_displayed_on_login_from_the_DMZ',
        'testcases.ula.TC01_Access_the_Internet_from_the_DMZ_allow_Everyone',
        'testcases.ula.TC08_Access_the_Internet_from_the_DMZ_allow_All',
        'testcases.ula.TC09_Access_the_Internet_from_the_DMZ_allow_Administrator',
        'testcases.ula.TC03_Access_the_Internet_from_the_DMZ_allow_a_super_group',
        'testcases.ula.TC10_user_authentication_settings_check_default_settings',
        'testcases.ula.TC11_user_authentication_settings_enable_Case_sensitive_user_names',
        'testcases.ula.TC12_user_authentication_settings_disable_enable_Case_sensitive_user_names',
        'testcases.ula.TC13_user_authentication_settings_enable_Enforce_login_uniqueness',
        'testcases.ula.TC14_user_authentication_settings_disable_Enforce_login_uniqueness',
        'testcases.ula.TC15_user_authentication_settings_enable_Force_relogin_after_password_change',
        'testcases.ula.TC02_Access_the_Internet_from_the_DMZ_allow_a_group',
        'testcases.ula.TC16_user_authentication_settings_disable_Force_relogin_after_password_change',
        'testcases.ula.TC17_user_authentication_settings_enable_Display_user_login_info_since_last_login',
         

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreens@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()