import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2/testcase')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'Guest_Users_TP349_2.sslvpn_config',
        'Guest_Users_TP349_2.create_guest_user',
        'Guest_Users_TP349_2.Guest_UserEdit',
        'Guest_Users_TP349_2.delete_all_guest_user',
        'Guest_Users_TP349_2.local_user_guest_service_WGS',
        'Guest_Users_TP349_2.edit_local_user_guest_service',
        'Guest_Users_TP349_2.guest_user_in_prefs_file',
        'Guest_Users_TP349_2.guest_user_session',
        'Guest_Users_TP349_2.guest_user_session_after_reboot',
        'Guest_Users_TP349_2.check_login_with_remaining_session_expiration_time',
        'Guest_Users_TP349_2.login_after_account_timeout_remaining',
        'Guest_Users_TP349_2.login_after_account_timeout',
        'Guest_Users_TP349_2.user_with_guest_service_limited_administrators',
        'Guest_Users_TP349_2.user_with_guest_service_read_only_administrators',
        'Guest_Users_TP349_2.user_with_guest_service_administrators',
        'Guest_Users_TP349_2.export_guest_account',
        'Guest_Users_TP349_2.export_guest_account_validation',

    ]

    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()