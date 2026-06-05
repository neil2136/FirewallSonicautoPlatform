# __author__: ldu
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Log/DPI_tag_in_Syslog_Connection_Closed')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC101',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC106',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC111',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC126',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestCFS_TC119',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestCFS_TC120',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC102',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC107',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC103',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC112',
        # 'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC108',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC117',
        # 'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC118',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC104',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC109',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestCFS_TC121',
        # 'testcases.DPI_tag_in_Syslog_Connection_Closed.TestCFS_TC122',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC105',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppRule_TC110',       
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC114',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC113',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestSyslogMode_TC123',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestSyslogMode_TC124',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestSyslogMode_TC125',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestSyslogMode_TC127',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC128',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC129',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC130',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC131',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC132',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC135',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC136',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC141',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC142',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC116',
        'testcases.DPI_tag_in_Syslog_Connection_Closed.TestAppCtrl_TC115',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
