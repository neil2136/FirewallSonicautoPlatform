import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Password_Ldap_LAN/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Password_Ldap_LAN/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Password_Ldap_LAN/definition/')



def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'compromised_pswd.config_ldap_radius_tacacs',
        'compromised_pswd.TC01_compromised_pswd_lan',
        'compromised_pswd.TC02_compromised_pswd_lan',
        'compromised_pswd.TC03_compromised_pswd_lan',
        'compromised_pswd.TC04_compromised_pswd_lan',
        'compromised_pswd.TC05_compromised_pswd_lan',
        'compromised_pswd.TC06_compromised_pswd_lan',
        'compromised_pswd.TC07_compromised_pswd_lan',
        'compromised_pswd.TC08_compromised_pswd_lan',
        'compromised_pswd.TC09_compromised_pswd_lan',
        'compromised_pswd.TC10_compromised_pswd_lan',
        'compromised_pswd.TC11_compromised_pswd_lan',
        'compromised_pswd.TC12_compromised_pswd_lan'

        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

