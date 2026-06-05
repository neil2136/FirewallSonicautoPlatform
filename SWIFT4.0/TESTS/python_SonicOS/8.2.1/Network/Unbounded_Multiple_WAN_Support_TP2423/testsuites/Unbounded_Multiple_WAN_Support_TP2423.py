__author__ = 'tcheng'
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Unbounded_Multiple_WAN_Support_TP2423')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Unbounded_Multiple_WAN_Support_TP2423/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_01_Unbounded_Multiple_WAN_Support_TP2423_tc_1',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_02_Unbounded_Multiple_WAN_Support_TP2423_tc_5',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_03_Unbounded_Multiple_WAN_Support_TP2423_tc_6',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_04_Unbounded_Multiple_WAN_Support_TP2423_tc_9',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_05_Unbounded_Multiple_WAN_Support_TP2423_tc_12',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_06_Unbounded_Multiple_WAN_Support_TP2423_tc_14',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_07_Unbounded_Multiple_WAN_Support_TP2423_tc_16',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_08_Unbounded_Multiple_WAN_Support_TP2423_tc_30',
        'testcases.Unbounded_Multiple_WAN_Support_TP2423.Test_09_Unbounded_Multiple_WAN_Support_TP2423_tc_34',          
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
