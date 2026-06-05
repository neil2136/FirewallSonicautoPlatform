import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.setup_mail_server',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Export_CSV',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Export_TXT',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Rules_name_should_contain_policy_ID_and_name_for_Access_and_NAT_in_System_Logs_page',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Clear_Log',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Log_Monitor_fw_reboot',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Import_from_template_Minimal',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Send_log_to_email',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Reset_category_event_count',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Edit_category_entry_GUI',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Edit_category_entry_Syslog',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Edit_category_entry_email',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Name_Resolution',
        # 'testcases.Log_Monitor_TP2582.TestLog_Monitor_Select_Columns_to_Display',
        # 'testcases.Log_Monitor_TP2582.TestLog_Monitor_Refresh_every_amount_seconds',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Syslog_format',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Import_from_template_Default',
        'testcases.Log_Monitor_TP2582.TestLog_Monitor_Log_Monitor_preference_file',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'gkatti@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
