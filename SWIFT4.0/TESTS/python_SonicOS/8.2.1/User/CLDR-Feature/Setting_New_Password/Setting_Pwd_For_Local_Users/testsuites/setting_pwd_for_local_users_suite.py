import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Local_Users/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Local_Users/testcases/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/CLDR-Feature/Setting_New_Password/Setting_Pwd_For_Local_Users/definition/')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'setting_pwd_for_local_users.config_ldap_NonTC',
        'setting_pwd_for_local_users.TC01_setting_pwd_for_local_users',
        'setting_pwd_for_local_users.TC02_setting_pwd_for_local_users',
        'setting_pwd_for_local_users.TC03_setting_pwd_for_local_users',
        'setting_pwd_for_local_users.TC04_setting_pwd_for_local_users'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    to_users = 'snisha@sonicwall.com'
    # cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users)
    st.run()

