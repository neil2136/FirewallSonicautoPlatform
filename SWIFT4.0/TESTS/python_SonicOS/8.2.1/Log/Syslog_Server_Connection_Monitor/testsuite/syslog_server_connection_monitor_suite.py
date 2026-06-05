# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Log/Syslog_Server_Connection_Monitor')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC01",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC02",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC03",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC04",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC07",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC08",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC11",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC12",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC13",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC14",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC15",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC16",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC22",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC25",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC26",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC27",
        "testcases.syslog_server_connection_monitor.Test_Syslog_Monitor_TC29",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
