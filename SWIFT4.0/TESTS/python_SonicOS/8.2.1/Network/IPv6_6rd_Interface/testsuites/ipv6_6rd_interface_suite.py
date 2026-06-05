import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_6rd_Interface/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_env.TestConfigENV',
        'ipv6_6rd_interface.Test_05_Config_for_6rdPrefix',
        'ipv6_6rd_interface.Test_08_Config_for_6rdBRIPv4',
        'ipv6_6rd_interface.Test_09_Config_for_6rdPrefix',
        'ipv6_6rd_interface.Test_15_6rd_Elements_When_DHCP',
        'ipv6_6rd_interface.Test_16_6rd_Elements_When_DHCP',
        'ipv6_6rd_interface.Test_20_Route_Policy_Check',
        'ipv6_6rd_interface.Test_26_AO_Check',
        'ipv6_6rd_interface.Test_29_Check_AO',
        'ipv6_6rd_interface.Test_31_Detect_AO',
        'ipv6_6rd_interface.Test_33_Check_OPTION_6RD_In_DHCP_Request',
        'ipv6_6rd_interface.Test_40_Check_6over4_packets',
        'ipv6_6rd_interface.Test_44_Check_dest_addr',
        'conf_env.TestUnconfigENV',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()