import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/local_groups_smoke1/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/local_groups_smoke1')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'local_groups.TC04_delete_group',
        'local_groups.TC08_add_member_to_group',
        'local_groups.TC09_multiple_members_to_group',
        'local_groups.TC10_remove_member_from_group',
        'local_groups.TC11_remove_multiple_members_from_group',
        'local_groups.TC12_add_vpn_access_client',
        'local_groups.TC13_add_multiple_vpn_access_client',
        'local_groups.TC14_remove_vpn_access_client',
        'local_groups.TC15_remove_multiple_vpn_access_client',
        'local_groups.TC26_add_group'
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'kskarkera@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()

