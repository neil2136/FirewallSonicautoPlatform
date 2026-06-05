import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
from runner.settings import Params, logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_Enforcement/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'definition.conf_pc.TestConfigWorkStationClient',
        'sso.NonTC',
        'sso.TC_01_SSO_enforcement_enabled_on_DMZ_zone_access_rule_can_trigger_SSO_authentication_for_DMZ_traffic_partition_in_DMZ_zone',
        'sso.TC_02_SSO_enforcement_disabled_on_DMZ_zone_access_rule_can_trigger_SSO_authentication_for_DMZ_traffic_partition_in_DMZ_zone',
        'sso.TC_03_SSO_enforcement_disabled_on_DMZ_zone_no_access_rule_no_security_service_traffic_from_DMZ_will_not_trigger_SSO_authentication_partition_DMZ_zone',
        'sso.TC_04_SSO_enforcement_disabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_partition_in_LAN_zone',
        'sso.TC_05_SSO_enforcement_disabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_multiple_partition_in_LAN_zone',
        'sso.TC_06_SSO_enforcement_disabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_not_trigger_SSO_authentication_partition_LAN_zone',
        'sso.TC_07_SSO_enforcement_enabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_partition_in_LAN_zone',
        'sso.TC_08_SSO_enforcement_enabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_trigger_SSO_authentication_multiple_partition_LAN_zone',
        'sso.TC_09_SSO_enforcement_enabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_trigger_SSO_authentication_partition_LAN_zone',
        'sso.TC_10_SSO_enforcement_disabled_on_LAN_zone_CFS_IPS_Application_FW_from_LAN_can_trigger_SSO_authentication_partition_in_LAN_zone',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

