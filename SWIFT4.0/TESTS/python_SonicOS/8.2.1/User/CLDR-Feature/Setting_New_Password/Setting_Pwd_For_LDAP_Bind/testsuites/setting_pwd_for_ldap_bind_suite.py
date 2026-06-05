import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_LDAP_Bind/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_LDAP_Bind/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_LDAP_Bind/definition/')



def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'setting_pwd_for_ldap_bind.config_ldap_NonTC',
        'setting_pwd_for_ldap_bind.TC01_setting_pwd_for_ldap_bind',
        'setting_pwd_for_ldap_bind.TC02_setting_pwd_for_ldap_bind',
        'setting_pwd_for_ldap_bind.TC03_setting_pwd_for_ldap_bind',
        'setting_pwd_for_ldap_bind.TC04_setting_pwd_for_ldap_bind' ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

