import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.config_fw.TestConfigFW',
        'ldap.TC001_Multiple_Ldap',
        'ldap.TC002_Multiple_Ldap',
        'ldap.TC003_Multiple_Ldap',
        'ldap.TC004_Multiple_Ldap',
        'ldap.TC005_Multiple_Ldap',
        'ldap.TC006_Multiple_Ldap',
        'ldap.TC007_Multiple_Ldap',
        'ldap.TC008_Multiple_Ldap',
        'ldap.TC009_Multiple_Ldap',
        'ldap.TC010_Multiple_Ldap',
        'ldap.TC011_Multiple_Ldap',
        'ldap.TC012_Multiple_Ldap',
        'ldap.TC013_Multiple_Ldap',
        'ldap.TC014_Multiple_Ldap',
        'ldap.TC015_Multiple_Ldap',
        'ldap.TC016_Multiple_Ldap',
        'ldap.TC017_Multiple_Ldap',
        'ldap.TC018_Multiple_Ldap',
        'ldap.TC019_Multiple_Ldap',
        'ldap.TC020_Multiple_Ldap',
        'ldap.TC021_Multiple_Ldap',
        'ldap.TC022_Multiple_Ldap',
        'ldap.TC023_Multiple_Ldap',
        'ldap.TC024_Multiple_Ldap',
        'ldap.TC025_Multiple_Ldap',
        'ldap.TC026_Multiple_Ldap',
        'ldap.TC027_Multiple_Ldap',
        'ldap.TC028_Multiple_Ldap',
        'ldap.TC029_Multiple_Ldap',
        'ldap.TC030_Multiple_Ldap'
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':

    to_users = 'smaaz@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()

