import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/SSL_VPN_and_Virtual_Assist')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/SSL_VPN_and_Virtual_Assist/testcases')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'SSL_VPN_and_Virtual_Assist.TC_01_SSL_VPN_and_Virtual_Assist',
        'SSL_VPN_and_Virtual_Assist.TC_02_SSL_VPN_and_Virtual_Assist',
        'SSL_VPN_and_Virtual_Assist.TC_03_SSL_VPN_and_Virtual_Assist',
        'SSL_VPN_and_Virtual_Assist.TC_04_SSL_VPN_and_Virtual_Assist',
        'SSL_VPN_and_Virtual_Assist.TC_05_SSL_VPN_and_Virtual_Assist',
 
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'gkatti@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com' 
    st = UnittestSuite(sys.argv, suite())
    st.run()
