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
        'ula_ipv6.TC_01_User_Has_Read_Only_privilege',
        'ula_ipv6.TC_02_User_Has_Limited_Admin_Privilege',
        'ula_ipv6.TC_03_User_Lockout_From_IPv6_Address',
        'ula_ipv6.TC_04_User_Logout_Using_Logout_Button',
        'ula_ipv6.TC_05_User_Logout_Log',
        'ula_ipv6.TC_06_User_Logout_By_Administrator',
        'ula_ipv6.TC_07_User_Logout_By_Administrator_Log'
    ]


    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    to_users = 'rsahu@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
