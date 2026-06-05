import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_TP293/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_TP293')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_users.config_ldap',
        'ldap_users.TC003_ldap_user_settings',
        'ldap_users.TC011_ldap_protocol_version',
        'ldap_users.TC038_ldap_use_ip',
        'ldap_users.TC043_ldap_protocol_version3',
        'ldap_users.TC056_ldap_microsoft_ad',
        'ldap_users.TC061_ldap_default_user_group',
        'ldap_users.TC064_ldap_default_user_group',
        'ldap_users.TC065_ldap_default_user_group',
        'ldap_users.TC095_ldap_config_login',
        'ldap_users.TC096_ldap_config_bind',
        'ldap_users.TC133_ldap_user_login',
        'ldap_users.delete_ldap',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()

