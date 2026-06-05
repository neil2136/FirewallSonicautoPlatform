RESOURCE = "WRLG7"

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+ "/Network/L2_Bridge_Mode_1257")

from runner.unittest.setup import Test
from config.init_testbed import *
from definitions.settings import *
from testcases.L2_Bridge_Mode_1257 import *
print(sys.path)

###to run this suite,we must disable spanning tree on static testbed switch##############

def suite():
    suites = unittest.TestSuite()
    suites.addTest(Test.parametrize(TestAddTopology, **my_topo))
    suites.addTest(TestRestoreDUTByUI('test_00_restore_dut'))
    suites.addTest(TestUploadFirmware('test_00_upload_firmware'))
    suites.addTest(TestUploadFirmware('test_03_offline_register'))
    suites.addTest(TestUploadFirmware('test_04_get_coredump'))
    suites.addTest(TestUploadFirmware('test_05_add_security_policy'))
    suites.addTest(Test_01_L2_Bridge_Mode_1257('test_00_show_testcase_info'))
    suites.addTest(Test_01_L2_Bridge_Mode_1257('test_01_config_L2_bridge_pair'))
    suites.addTest(Test_01_L2_Bridge_Mode_1257('test_02_check_interface_status'))

    suites.addTest(Test_33_L2_Bridge_Mode_1257('test_00_show_testcase_info'))
    suites.addTest(Test_33_L2_Bridge_Mode_1257('test_01_config_L2_bridge_pair'))
    suites.addTest(Test_33_L2_Bridge_Mode_1257('test_02_add_route_on_PC2_and_PC3'))
    suites.addTest(Test_33_L2_Bridge_Mode_1257('test_03_send_traffic_from_LAN_to_WAN'))

    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_00_show_testcase_info'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_01_config_L2_bridge_pair'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_02_config_LAN_WAN_access_rule_everyone'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_03_config_users_settings_radius'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_04_start_radius_server_on_PC3'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_05_logout_DUT'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_06_send_traffic_from_LAN_to_WAN'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_07_radius_login_DUT_via_PC2'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_08_send_traffic_from_LAN_to_WAN'))
    suites.addTest(Test_35_L2_Bridge_Mode_1257('test_09_Restore_environment_on_PC'))

    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_00_show_testcase_info'))
    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_01_configure_X2_staic_mode'))
    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_02_Export_Perference'))
    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_03_config_L2_bridge_pair'))
    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_04_Import_Prefs'))
    suites.addTest(Test_44_L2_Bridge_Mode_1257('test_05_check_interface_status'))

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



