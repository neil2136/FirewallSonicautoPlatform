__author__ = 'tcheng'
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite



sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Multiple_WAN_Phase_1_Smoke')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Multiple_WAN_Phase_1_Smoke/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',    
        'definition.set_env.TestConfigTB_03',    
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_01_Multiple_WAN_Phase_1_Smoke_tc_01',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_02_Multiple_WAN_Phase_1_Smoke_tc_24',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_03_Multiple_WAN_Phase_1_Smoke_tc_25',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_04_Multiple_WAN_Phase_1_Smoke_tc_26',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_05_Multiple_WAN_Phase_1_Smoke_tc_27',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_06_Multiple_WAN_Phase_1_Smoke_tc_28',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_07_Multiple_WAN_Phase_1_Smoke_tc_29',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_08_Multiple_WAN_Phase_1_Smoke_tc_30',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_09_Multiple_WAN_Phase_1_Smoke_tc_34',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_10_Multiple_WAN_Phase_1_Smoke_tc_54',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_11_Multiple_WAN_Phase_1_Smoke_tc_8',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_12_Multiple_WAN_Phase_1_Smoke_tc_80',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_13_Multiple_WAN_Phase_1_Smoke_tc_84',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_14_Multiple_WAN_Phase_1_Smoke_tc_88',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_15_Multiple_WAN_Phase_1_Smoke_tc_125',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_16_Multiple_WAN_Phase_1_Smoke_tc_126',
        'testcases.Multiple_WAN_Phase_1_Smoke.Test_17_Multiple_WAN_Phase_1_Smoke_tc_131',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
