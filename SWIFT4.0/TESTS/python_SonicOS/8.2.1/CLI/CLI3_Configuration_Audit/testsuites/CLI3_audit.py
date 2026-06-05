# __author__: xzhou
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Configuration_Audit')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                '/CLI/CLI3_Configuration_Audit/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/CLI/CLI3_Configuration_Audit/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw',
        'configuration_audit.Test_01_check_audit_display_on_console',
        'configuration_audit.Test_02_check_audit_no_display_on_console',
        'configuration_audit.Test_03_check_audit_supplemental_changes',
        'configuration_audit.Test_04_check_audit_no_supplemental_changes',
        'configuration_audit.Test_05_check_log_auto_eaddr',
        'configuration_audit.Test_06_check_log_auto_eformat_csv',
        'configuration_audit.Test_07_check_log_auto_eformat_html',
        'configuration_audit.Test_08_check_log_auto_eformat_pt',
        'configuration_audit.Test_09_check_log_auto_period_daily',
        'configuration_audit.Test_10_check_log_auto_period_weekly',
        'configuration_audit.Test_11_check_log_auto_period_full',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
    