# __author__:qshi
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Debug_Enhancement_User_Auth')
from testcases.Enahncement_User_Auth import *


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.conf_pc',
        'testcases.Enahncement_User_Auth.Test_01_AuthDbgCommand_LogToConsole',
        'testcases.Enahncement_User_Auth.Test_02_UserDbgCommand_AuthLevel',
        'testcases.Enahncement_User_Auth.Test_03_UserDbgCommand_AddedIn_CLI',
        'testcases.Enahncement_User_Auth.Test_04_UserDbgAuthLDAP_AddedIn_CLI',
        'testcases.Enahncement_User_Auth.Test_05_UserDbgCommand_LevelTest_001',
        'testcases.Enahncement_User_Auth.Test_05_UserDbgCommand_LevelTest_002',
        'testcases.Enahncement_User_Auth.Test_05_UserDbgCommand_LevelTest_003',
        'testcases.Enahncement_User_Auth.Test_06_AuthDbgCommand_Cia',
        'testcases.Enahncement_User_Auth.Test_07_Add_LDAPServer',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_001',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_002',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_003',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_004',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_005',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_006',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_007',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_008',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_009',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_010',
        'testcases.Enahncement_User_Auth.Test_08_AuthDbgCommand_LDAP01_011',
        'testcases.Enahncement_User_Auth.Test_09_Add_LDAPServerNotAccess',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_001',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_002',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_003',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_004',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_005',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_006',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_007',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_008',
        'testcases.Enahncement_User_Auth.Test_10_AuthDbgCommand_LDAP02_009',
        'testcases.Enahncement_User_Auth.Test_11_Add_LDAPServerwith_Domain',
        'testcases.Enahncement_User_Auth.Test_12_AuthDbgCommand_LDAP03_001',
        'testcases.Enahncement_User_Auth.Test_13_AuthDbgCommand_LogToSyslog',
        'testcases.Enahncement_User_Auth.Test_14_AuthDbgCommand_LogToAnySyslogServer',
        'testcases.Enahncement_User_Auth.Test_15_AuthDbgCommand_LogToSepecifySyslogServer'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
