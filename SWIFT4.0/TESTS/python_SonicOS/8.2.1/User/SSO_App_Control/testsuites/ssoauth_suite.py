import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_App_Control')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_App_Control/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ssoauth.NonTC',
        'ssoauth.TC_01_Edit_a_category_SSO_enforcement_disabled_set_included_user_with_local_user_group',
        'ssoauth.TC_02_Edit_a_signature_SSO_enforcement_enabled_set_both_included_and_excluded_user_group',
        'ssoauth.TC_03_Edit_an_application_SSO_enforcement_enabled_set_included_user_group',
        'ssoauth.TC_04_Edit_an_application_SSO_enforcement_enabled_set_excluded_user_group',
        'ssoauth.TC_05_Edit_a_signature_then_enable_app_control_verify_that_SSO_enforcement_will_be_enabled_automatically',
        'ssoauth.TC_06_Add_an_app_rule_policy_SSO_enforcement_disabled_set_included_user_group',
        'ssoauth.TC_07_Edit_a_category_SSO_enforcement_disabled_set_excluded_user_group',
        'ssoauth.TC_08_Add_an_app_rule_policy_SSO_enforcement_disabled_set_excluded_user_group',
        'ssoauth.TC_09_Add_an_app_rule_policy_SSO_enforcement_disabled_set_both_included_and_excluded_user_group',
        'ssoauth.TC_10_App_an_app_rule_policy_SSO_enforcement_enabled_set_included_user_group',
        'ssoauth.TC_11_Add_an_app_rule_policy_SSO_enforcement_enabled_set_excluded_user_group',
        'ssoauth.TC_12_Include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication',
        'ssoauth.TC_13_Include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication',
        'ssoauth.TC_14_Category_include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication',
        'ssoauth.TC_15_Application_include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication',
                  
       
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

