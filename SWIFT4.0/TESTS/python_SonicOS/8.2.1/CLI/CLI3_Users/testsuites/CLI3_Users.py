import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/CLI/CLI3_Users')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/CLI/CLI3_Users/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
'/CLI/CLI3_Users/testcases')

# __Author__ = 'xzhou'
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw',
        'CLI3_users.Test_01_user_method_list',
        'CLI3_users.Test_10_configure_login_uniqueness',
        'CLI3_users.Test_11_user_method_configure',
        'CLI3_users.Test_12_configure_auth_bypass',
        'CLI3_users.Test_13_show_auth_user_status',
        'CLI3_users.Test_14_configure_status_window_heartbeat',
        'CLI3_users.Test_15_configure_web_login_session_limit',
        'CLI3_users.Test_16_configure_ldap_allow_references',
        'CLI3_users.Test_17_configure_ldap_allow_referrals',
        'CLI3_users.Test_combined_tc_10_11_12_13_15_16_17',
        'CLI3_users.Test_2_configure_auth_acceptable_use_policy',
        'CLI3_users.Test_3_configure_auth_aup_on_zones',
        'CLI3_users.Test_4_configure_auth_page_timeout',
        'CLI3_users.Test_5_configure_auth_case_sensitive_names',
        'CLI3_users.Test_6_list_auth_cli',
        'CLI3_users.Test_7_auth_disconnected_user_detect',
        'CLI3_users.Test_8_auth_http_redirect_after_login',
        'CLI3_users.Test_9_auth_inactivity_timeout',
        'CLI3_users.Test_Combined_tc_18_19_20_22_23_24_25_26_27',
        'CLI3_users.Test_18_ldap_default_user_group',
        'CLI3_users.Test_19_ldap_directory',
        'CLI3_users.Test_20_ldap_local_tls_certificate',
        'CLI3_users.Test_22_ldap_local_user_only',
        'CLI3_users.Test_23_ldap_operation_timeout',
        'CLI3_users.Test_24_ldap_relay',
        'CLI3_users.Test_25_ldap_schema',
        'CLI3_users.Test_26_ldap_server_member',
        'CLI3_users.Test_Combine_tc_28_29_30_31',
        'CLI3_users.Test_28_local_apply_password_constraints',
        'CLI3_users.Test_29_local_group_member',
        'CLI3_users.Test_30_local_prune_on_expiry',
        'CLI3_users.Test_31_local_user_add',
        'CLI3_users.Test_Combine_tc_32_34_35_36_38_39',
        'CLI3_users.Test_32_radius_default_user_group',
        'CLI3_users.Test_34_radius_local_user_only',
        'CLI3_users.Test_35_radius_retries',
        'CLI3_users.Test_36_radius_server_host',
        'CLI3_users.Test_38_radius_timeout',
        'CLI3_users.Test_39_radius_user_group_mechanism',
        "CLI3_users.Test_Combined_TC_40_43_44_46_47_48_49_54_56_57_58",
        'CLI3_users.Test_40_sso_agent_host',
        'CLI3_users.Test_41_sso_list_cli',
        'CLI3_users.Test_43_sso_enforce_on_zone',
        'CLI3_users.Test_44_sso_hold_time_after_failure',
        'CLI3_users.Test_46_sso_local_users_only',
        'CLI3_users.Test_47_sso_method_sso_agent',
        'CLI3_users.Test_48_sso_non_domain_limited_access',
        'CLI3_users.Test_49_sso_poll_rate',
        'CLI3_users.Test_52_sso_security_services_bypass_dns',
        'CLI3_users.Test_54_sso_terminal_services_agent',
        'CLI3_users.Test_56_sso_tsa_services_bypass',
        'CLI3_users.Test_57_sso_user_group_mechanism',
        'CLI3_users.Test_58_sso_windows_service_user_name',
        'CLI3_users.Test_59_check_local_users_groups',
        'CLI3_users.TestErrorLdapServer_TC3937374',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
