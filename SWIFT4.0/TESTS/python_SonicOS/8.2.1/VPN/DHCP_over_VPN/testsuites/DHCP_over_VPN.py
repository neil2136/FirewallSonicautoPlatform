import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/VPN/DHCP_over_VPN")

'''
 ****add single test case to test suite****      
 ****add test cases by module ****
'''
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_env.TestInitConfig',
        'testcases.DHCP_over_VPN.Test_01_External_Server_Replay_on_Remote',
        'testcases.DHCP_over_VPN.Test_21_Static_Devices_on_LAN_Add',
        'testcases.DHCP_over_VPN.Test_27_Excluded_LAN_Devices_Delete',
        'testcases.DHCP_over_VPN.Test_65_DHCP_Lease_Bound_to_X2',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sgao@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
