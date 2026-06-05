import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Session_Settings/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Session_Settings')


def suite():
	testcases_list = [
		'config.init_testbed.TestRestoreDUT',
		'config.init_testbed.TestUploadFirmware',
		'definition.conf_fw',
		'definition.conf_fw.TestConfigTB',
		"definition.conf_pc.TestConfigWorkStationClient",
		"User_session_Settings_cases.NonTC",
		"User_session_Settings_cases.sso_lan_only",
		"User_session_Settings_cases.unidentified_login",
		"User_session_Settings_cases.unknow_sso",
		"User_session_Settings_cases.sso_bypass",
		"User_session_Settings_cases.user_connection_logout",
		"User_session_Settings_cases.user_connection_logout_others",
		"User_session_Settings_cases.inactive_timeout",
		"User_session_Settings_cases.validate_user_session_inTSR",
		"User_session_Settings_cases.empty_text_error",
		"User_session_Settings_cases.prevent_connection_logout"
]

	suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
	return suites


if __name__ == '__main__':
	st = UnittestSuite(sys.argv, suite())
	st.run()
