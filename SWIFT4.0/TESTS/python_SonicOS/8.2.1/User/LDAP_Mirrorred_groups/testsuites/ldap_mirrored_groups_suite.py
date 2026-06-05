import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_Mirrorred_groups/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_Mirrorred_groups')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ldap_mirrored_groups.config_ldap',
        'ldap_mirrored_groups.TC01_ldap_mirrored_group',
        'ldap_mirrored_groups.TC02_ldap_mirrored_group',
        'ldap_mirrored_groups.TC03_ldap_mirrored_group',
        'ldap_mirrored_groups.TC04_ldap_mirrored_group',
        'ldap_mirrored_groups.TC05_ldap_mirrored_group',
        'ldap_mirrored_groups.TC06_ldap_mirrored_group',
        'ldap_mirrored_groups.TC07_ldap_mirrored_group',
        'ldap_mirrored_groups.TC08_ldap_mirrored_group',
        'ldap_mirrored_groups.TC09_ldap_mirrored_group',
        'ldap_mirrored_groups.TC10_ldap_mirrored_group',
        'ldap_mirrored_groups.TC11_ldap_mirrored_group',
        'ldap_mirrored_groups.TC12_ldap_mirrored_group', 
        'ldap_mirrored_groups.TC13_ldap_mirrored_group', 
        'ldap_mirrored_groups.TC14_ldap_mirrored_group', 
        'ldap_mirrored_groups.delete_ldap'
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

