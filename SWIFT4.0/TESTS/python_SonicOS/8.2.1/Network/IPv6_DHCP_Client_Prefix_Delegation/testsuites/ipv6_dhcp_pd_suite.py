import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_DHCP_Client_Prefix_Delegation/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_env.TestConfigENV',
        'ipv6_dhcp_pd.Test_009_Check_Route',
        'ipv6_dhcp_pd.Test_010_Add_Address',
        'ipv6_dhcp_pd.Test_019_Check_AO',
        'ipv6_dhcp_pd.Test_020_Check_Address_Update',
        'ipv6_dhcp_pd.Test_021_Check_Route_Update',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()