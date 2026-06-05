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
        'definition.vpn_conf_fw.TestConfigTB',
        'definition.vpn_conf_pc.TestConfigWorkStationClient',
        'vpn_sso.NonTC',
        'vpn_sso.TC_13_SSO_Enforcement_Enabled_On_VPN_Zone_With_Security_Service',
        'vpn_sso.TC_14_SSO_Enforcement_Enabled_On_VPN_Zone',
        'vpn_sso.TC_15_SSO_Enforcement_Disabled_On_VPN_Zone',
        'vpn_sso.TC_16_SSO_Enforcement_Disabled_On_VPN_Zone_With_Security_Service',
        'vpn_sso.TC_17_SSO_Enforcement_Disabled_On_VPN_Zone_With_Access_Rule'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

