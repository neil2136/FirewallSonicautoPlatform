# __Author__: Neil Zhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Upgrade/Platform_Upgrade_Via_UI')
from definition.settings import platform_name, uuid_dict


def suite():
    if platform_name not in uuid_dict.keys():
        testcases_list = ['testcases.platform_upgrade.Test_03_platform_not_in_test_list']
    else:
        testcases_list = [
            'config.init_testbed.TestRestoreDUT',
            'config.init_testbed.TestUploadFirmware',   # Avoid from 7.1.1 downgraded to The lower 7.0.1 version failed
            'definition.conf_pc',
            'definition.conf_fw',
            'testcases.platform_upgrade.Test_upgrade_previous_firmware_via_UI',
            'testcases.platform_upgrade.Test_check_configure_and_traffic_in_previous_firmware',
            'testcases.platform_upgrade.Test_01_upgrade_current_firmware_via_UI',
            'testcases.platform_upgrade.Test_02_traffic_check_from_lan_to_wan',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
