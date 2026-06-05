import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_using_TLS')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/LDAP_using_TLS/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_using_tls.ldap_config',

        'ldap_using_tls.LDAP_Test_Connection',
        'ldap_using_tls.LDAP_Test_User_Authentication',
        'ldap_using_tls.LDAP_User_Change_Password_Virtual_Office',

# Commenting testcase due to sonicauto topo image issue: AD user 'changepassword3' is set to "Password never expires".
# Manual topo has correct setting ("must change password at next logon"), so test passes there.
        # 'ldap_using_tls.LDAP_User_Change_Password_NX',

        'ldap_using_tls.Import_LDAP_Users_and_Groups',
        'ldap_using_tls.Mirror_LDAP_Groups',
        'ldap_using_tls.LDAP_Test_Connection_User_Authentication_GC_Port_3268',
        'ldap_using_tls.LDAP_Test_Connection_User_Authentication_GC_Port_3269',
        'ldap_using_tls.Use_LDAP_Retrieve_Group_Info_On_RADIUS_Server_Check_ULA'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
