import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ECMP/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ECMP/definition')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigENV',
        'ecmp.Test_38_IPv4_ECMP_PBR_with_4_gw_same_outgoing_physical_interface',
        'ecmp.Test_39_IPv4_ECMP_PBR_with_4_gw_different_outgoing_interface',
        'ecmp.Test_219_TSR',
        'ecmp.Test_147_Add_an_IPv4_ECMP_PBR_in_CLI_with_4_gw_different_interface',
        'ecmp.Test_159_Edit_an_IPv4_ECMP_PBR_in_CLI_which_is_added_on_GUI',
        'ecmp.Test_054_IPv4_ECMP_PBR_src_range_dst_network_4_gw',
        'ecmp.Test_057_IPv4_ECMP_PBR_src_network_dst_network_4_gw',
        'ecmp.Test_179_Delete_an_IPv4_ECMP_PBR_in_CLI_which_is_added_on_GUI',
        'ecmp.Test_096_Function_test_when_has_4_gateways_the_third_one_is_down',
        'ecmp.Test_100_Function_test_when_has_4_gateways_the_third_one_is_back'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ldu@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
