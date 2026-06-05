import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Built_in_Admin/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Built_in_Admin/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Built_in_Admin/definition/')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'setting_pwd_for_built_in_admin.config_ldap_NonTC',
        'setting_pwd_for_built_in_admin.TC01_setting_pwd_for_built_in_admin',
        'setting_pwd_for_built_in_admin.TC02_setting_pwd_for_built_in_admin',
        'setting_pwd_for_built_in_admin.TC03_setting_pwd_for_built_in_admin',
        'setting_pwd_for_built_in_admin.TC04_setting_pwd_for_built_in_admin'
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

