# __author__ = 'XZhou'
import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/App_Control_Filename_Logging/")
print(sys.path)
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.SetupMailServer_on_PC2',
        'definition.init_conf_pc',
        'testcases.App_Control_Filename_Logging.TC001_Enable_Filename_Logging',
        'testcases.App_Control_Filename_Logging.TC002_Disable_Filename_Logging',
        'testcases.App_Control_Filename_Logging.TC003_Verify_filename_logging_http_protocol_event_log',
        'testcases.App_Control_Filename_Logging.TC015_Verify_filename_logging_http_protocol_event_log_ipv6',
        'testcases.App_Control_Filename_Logging.TC021_Verify_filename_logging_http_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC009_Verify_filename_logging_http_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC027_Verify_app_control_filename_post_restart',
        'testcases.App_Control_Filename_Logging.TC029_Verify_tsr_Enable_Filename_Logging',
        'testcases.App_Control_Filename_Logging.TC010_Verify_filename_logging_ftp_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC004_Verify_filename_logging_ftp_protocol_event_log',
        'testcases.App_Control_Filename_Logging.TC022_Verify_filename_logging_ftp_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC016_Verify_filename_logging_ftp_protocol_event_log_ipv6',
        'testcases.App_Control_Filename_Logging.TC012_Verify_filename_logging_smtp_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC013_Verify_filename_logging_pop3_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC014_Verify_filename_logging_imap_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC006_Verify_filename_logging_smtp_protocol_eventlog',
        'testcases.App_Control_Filename_Logging.TC007_Verify_filename_logging_pop3_protocol_eventlog',
        'testcases.App_Control_Filename_Logging.TC008_Verify_filename_logging_imap_protocol_eventlog',
        'testcases.App_Control_Filename_Logging.TC018_Verify_filename_logging_smtp_protocol_eventlog_ipv6',
        'testcases.App_Control_Filename_Logging.TC019_Verify_filename_logging_pop3_protocol_eventlog_ipv6',
        'testcases.App_Control_Filename_Logging.TC020_Verify_filename_logging_imap_protocol_eventlog_ipv6',
        'testcases.App_Control_Filename_Logging.TC024_Verify_filename_logging_smtp_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC013_Verify_filename_logging_pop3_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC014_Verify_filename_logging_imap_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC011_Verify_filename_logging_NetBios_protocol_syslog',
        'testcases.App_Control_Filename_Logging.TC017_Verify_filename_logging_NetBios_protocol_event_log_ipv6',
        'testcases.App_Control_Filename_Logging.TC023_Verify_filename_logging_NetBios_protocol_syslog_ipv6',
        'testcases.App_Control_Filename_Logging.TC005_Verify_filename_logging_NetBios_protocol_event_log',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
