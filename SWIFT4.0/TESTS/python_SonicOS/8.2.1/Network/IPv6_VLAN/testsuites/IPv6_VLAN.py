import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_VLAN/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigENV',
        'ipv6_vlan.Test_00_Config_Switch',
        'ipv6_vlan.Test_17_management_https',
        'ipv6_vlan.Test_13_Static_IPv6_Assignment',
        'ipv6_vlan.Test_14_Dynamic_IPv6_Assignment',
        'ipv6_vlan.Test_24_passing_traffic',
        'ipv6_vlan.Test_100_Config_Switch',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()