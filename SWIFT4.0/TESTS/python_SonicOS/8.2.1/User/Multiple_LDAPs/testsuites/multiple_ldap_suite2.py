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
        'ldap.TC031_Multiple_Ldap',
        'ldap.TC032_Multiple_Ldap',
        'ldap.TC033_Multiple_Ldap',
        'ldap.TC034_Multiple_Ldap',
        'ldap.TC035_Multiple_Ldap',
        'ldap.TC036_Multiple_Ldap',
        'ldap.TC037_Multiple_Ldap',
        'ldap.TC038_Multiple_Ldap',
        'ldap.TC039_Multiple_Ldap',
        'ldap.TC040_Multiple_Ldap',
        'ldap.TC041_Multiple_Ldap',
        'ldap.TC042_Multiple_Ldap',
        'ldap.TC043_Multiple_Ldap',
        'ldap.TC044_Multiple_Ldap',
        'ldap.TC045_Multiple_Ldap',
        'ldap.TC046_Multiple_Ldap',
        'ldap.TC047_Multiple_Ldap',
        'ldap.TC048_Multiple_Ldap',
        'ldap.TC049_Multiple_Ldap',
        'ldap.TC050_Multiple_Ldap',
        'ldap.TC051_Multiple_Ldap',
        'ldap.TC052_Multiple_Ldap',
        'ldap.TC053_Multiple_Ldap',
        'ldap.TC054_Multiple_Ldap',
        'ldap.TC055_Multiple_Ldap',
        'ldap.TC056_Multiple_Ldap',
        'ldap.TC057_Multiple_Ldap',
        'ldap.TC058_Multiple_Ldap',
        'ldap.TC059_Multiple_Ldap',
        'ldap.TC060_Multiple_Ldap',
        'ldap.TC061_Multiple_Ldap',
        'ldap.TC062_Multiple_Ldap',
        'ldap.TC063_Multiple_Ldap',
        'ldap.TC064_Multiple_Ldap',
        'ldap.TC065_Multiple_Ldap',
        'ldap.TC066_Multiple_Ldap',
        'ldap.TC067_Multiple_Ldap',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':

    to_users = 'smaaz@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()

