__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WireMode2_2617')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WireMode2_2617/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',
        'definition.set_env.TestSetup_Https_Server',
        'testcases.WireMode2_2617.Test_01_WireMode2_2617_tc_1',
        'testcases.WireMode2_2617.Test_02_WireMode2_2617_tc_2',
        'testcases.WireMode2_2617.Test_03_WireMode2_2617_tc_12',
        'testcases.WireMode2_2617.Test_04_WireMode2_2617_tc_16',
        'testcases.WireMode2_2617.Test_05_WireMode2_2617_tc_19',
        'testcases.WireMode2_2617.Test_06_WireMode2_2617_tc_22',
        'testcases.WireMode2_2617.Test_07_WireMode2_2617_tc_27',
        'testcases.WireMode2_2617.Test_08_WireMode2_2617_tc_29',
        'testcases.WireMode2_2617.Test_09_WireMode2_2617_tc_46',
        'testcases.WireMode2_2617.Test_10_WireMode2_2617_tc_47',
        'testcases.WireMode2_2617.Test_11_WireMode2_2617_tc_58',
        'testcases.WireMode2_2617.Test_12_WireMode2_2617_tc_63',
        'testcases.WireMode2_2617.Test_13_WireMode2_2617_tc_65',
        'testcases.WireMode2_2617.Test_14_WireMode2_2617_tc_71',
        'testcases.WireMode2_2617.Test_15_WireMode2_2617_tc_72',
        'testcases.WireMode2_2617.Test_16_WireMode2_2617_tc_75',
        'testcases.WireMode2_2617.Test_17_WireMode2_2617_tc_76',          
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
