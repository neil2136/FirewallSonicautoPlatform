import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_api/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_api')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_api.TC01_LDAP',
        'ldap_api.TC03_LDAP',        
        'ldap_api.TC07_LDAP',                
        'ldap_api.TC05_LDAP',
        'ldap_api.TC06_LDAP',
        'ldap_api.TC15_LDAP',
        'ldap_api.TC08_LDAP',
        
        'ldap_api.TC09_LDAP',
        'ldap_api.TC10_LDAP',
        'ldap_api.TC11_LDAP',
        'ldap_api.TC12_LDAP',
        'ldap_api.TC13_LDAP',
        'ldap_api.TC14_LDAP',
        'ldap_api.TC16_LDAP',
        'ldap_api.TC17_LDAP',
        'ldap_api.TC18_LDAP',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ujkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

