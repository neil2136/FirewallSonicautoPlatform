__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/DHCP_Multi_Scope_2372')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/DHCP_Multi_Scope_2372/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.DHCP_Multi_Scope_2372.Test_01_DHCP_Multi_Scope_2372_tc_8',
        'testcases.DHCP_Multi_Scope_2372.Test_02_DHCP_Multi_Scope_2372_tc_9',
        'testcases.DHCP_Multi_Scope_2372.Test_03_DHCP_Multi_Scope_2372_tc_10',
        'testcases.DHCP_Multi_Scope_2372.Test_04_DHCP_Multi_Scope_2372_tc_11',
        'testcases.DHCP_Multi_Scope_2372.Test_05_DHCP_Multi_Scope_2372_tc_12',
        'testcases.DHCP_Multi_Scope_2372.Test_06_DHCP_Multi_Scope_2372_tc_13',
        'testcases.DHCP_Multi_Scope_2372.Test_07_DHCP_Multi_Scope_2372_tc_14',
        'testcases.DHCP_Multi_Scope_2372.Test_08_DHCP_Multi_Scope_2372_tc_15',
        'testcases.DHCP_Multi_Scope_2372.Test_09_DHCP_Multi_Scope_2372_tc_16',
        'testcases.DHCP_Multi_Scope_2372.Test_10_DHCP_Multi_Scope_2372_tc_17',
        'testcases.DHCP_Multi_Scope_2372.Test_11_DHCP_Multi_Scope_2372_tc_18',
        'testcases.DHCP_Multi_Scope_2372.Test_12_DHCP_Multi_Scope_2372_tc_19',
        'testcases.DHCP_Multi_Scope_2372.Test_13_DHCP_Multi_Scope_2372_tc_20',
        'testcases.DHCP_Multi_Scope_2372.Test_14_DHCP_Multi_Scope_2372_tc_28',
        'testcases.DHCP_Multi_Scope_2372.Test_15_DHCP_Multi_Scope_2372_tc_32',
        'testcases.DHCP_Multi_Scope_2372.Test_16_DHCP_Multi_Scope_2372_tc_67',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
