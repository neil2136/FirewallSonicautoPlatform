import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement_TP2560')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement_TP2560/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'definition.conf_pc.TestConfigWorkStationClient',
        'sso.NonTC',
        'sso.TC_01_SSO_Enforcement_Enabled_On_DMZ_Zone',
        'sso.TC_02_SSO_Enforcement_Disabled_On_DMZ_Zone_With_Access_Rule',
        'sso.TC_03_SSO_Enforcement_Disabled_On_DMZ_Zone_With_Security_Service',
        'sso.TC_04_SSO_Enforcement_Disabled_On_DMZ_Zone',
        'sso.TC_05_SSO_Enforcement_Enabled_On_LAN_Zone_With_Security_Service',
        'sso.TC_06_SSO_Enforcement_Enabled_On_LAN_Zone_With_Access_Rule',
        'sso.TC_07_SSO_Enforcement_Enabled_On_LAN_Zone',
        'sso.TC_08_SSO_Enforcement_Enabled_On_DMZ_Zone_With_Security_Service',
        'sso.TC_09_SSO_Enforcement_Enabled_On_DMZ_Zone_With_Access_Rule',
        'sso.TC_10_SSO_Enforcement_Disabled_On_LAN_Zone',
        'sso.TC_11_SSO_Enforcement_Disabled_On_LAN_Zone_With_Security_Service',
        'sso.TC_12_Check_Log_For_SSO_Enforcement_Any_Zone'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

