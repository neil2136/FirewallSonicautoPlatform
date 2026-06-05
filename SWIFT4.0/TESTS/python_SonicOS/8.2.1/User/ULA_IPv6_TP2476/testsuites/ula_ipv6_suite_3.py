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
        'ula_ipv6.TC_15_User_Logout_Login_Session_Limit_Expired',
        'ula_ipv6.TC_16_IPv6_User_Logged_In_Check_TSR',
        'ula_ipv6.TC_17_User_Login_Status',
        'ula_ipv6.TC_18_User_Login_Log'
    ]


    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    to_users = 'rsahu@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
