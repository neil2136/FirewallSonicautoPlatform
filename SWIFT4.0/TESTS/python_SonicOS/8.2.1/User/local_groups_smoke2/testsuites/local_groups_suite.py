import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/local_groups_smoke2/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/local_groups_smoke2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'local_groups.TC28_add_full_management_capabilities',
        'local_groups.TC29_remove_full_management_capabilities',
        'local_groups.TC30_add_read_only_management_capabilities',
        'local_groups.TC31_remove_read_only_management_capabilities',
        'local_groups.TC63_add_bookmark',
        'local_groups.TC66_delete_bookmark',
        'local_groups.TC72_enable_to_management_on_login',
        'local_groups.TC73_disable_to_management_on_login',
        'local_groups.TC85_group_settings_in_TSR',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

