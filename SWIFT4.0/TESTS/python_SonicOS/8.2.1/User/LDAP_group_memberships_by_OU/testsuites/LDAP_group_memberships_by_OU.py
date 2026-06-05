import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_group_memberships_by_OU')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_group_memberships_by_OU/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.LDAP_group_memberships_by_OU.ldap_config',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_TSR_support',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_Restart_FW',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_export_import_pref',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_memberships_set_by_OU_Can_be_enable_and_Disable',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_different_format_to_set_location',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_For_users_at_or_under_the_given_location',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_For_users_at_given_location',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_For_users_access_rules',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_For_logs_support',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_App_rules',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_SSO',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_CFS',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_GAV',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_SSLVPN',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_DPI_SSL',
        'testcases.LDAP_group_memberships_by_OU.Test_LDAP_locations_configured_used_in_Radius',
        'testcases.LDAP_group_memberships_by_OU.TC_imported_groups_auto_filled',
         'testcases.LDAP_group_memberships_by_OU.TC_AA_support',


        
        


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    # to_users = 'sbharaj@sonicwall.com'
    # cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
