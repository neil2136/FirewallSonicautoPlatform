import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/definition/')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'compromised_pwd.config_ldap_radius_tacacs',

        'compromised_pwd.TC01_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC02_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC03_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC04_compromised_pwd_check_in_dmz',
        
        'compromised_pwd.TC05_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC06_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC07_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC08_compromised_pwd_check_in_dmz',

        'compromised_pwd.TC09_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC10_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC11_compromised_pwd_check_in_dmz',
        'compromised_pwd.TC12_compromised_pwd_check_in_dmz'
 ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

