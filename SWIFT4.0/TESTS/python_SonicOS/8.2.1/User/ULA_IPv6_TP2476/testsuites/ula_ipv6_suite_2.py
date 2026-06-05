import sys
import os
import unittest

from runner.unittest.suite import UnittestSuite
from runner.settings import logger
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/ULA_IPv6_TP2476/testcases')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/ULA_IPv6_TP2476')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigFw',
        'definition.init_conf_pc.TestSetup_PCs',
        'ula_ipv6.TC_00_ULA_Config',
        'ula_ipv6.TC_08_User_Lockout_From_IPv6_Address_Then_Login_Via_IPv4_Address',
        'ula_ipv6.TC_09_User_Lockout_From_IPv4_Address_Then_Login_Via_IPv6_Address',
        'ula_ipv6.TC_10_Admin_Permission_With_IPv6_Address_Then_Try_Permission_Via_IPv4_Address',
        'ula_ipv6.TC_11_Admin_Permission_With_IPv4_Address_Then_Try_Permission_Via_IPv6_Address',
        'ula_ipv6.TC_12_Verify_User_Session_Logout_Limit_Expired_Log',
        'ula_ipv6.TC_13_Login_As_Built_Admin',
        'ula_ipv6.TC_14_User_Unlocked_By_Admin'
    ]


    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    to_users = 'rsahu@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
