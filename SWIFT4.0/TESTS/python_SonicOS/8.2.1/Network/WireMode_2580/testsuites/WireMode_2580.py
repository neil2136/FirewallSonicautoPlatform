__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WireMode_2580')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WireMode_2580/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',
        'testcases.WireMode_2580.Test_01_WireMode_2580_tc_1511478',
        'testcases.WireMode_2580.Test_02_WireMode_2580_tc_1511479',
        'testcases.WireMode_2580.Test_03_WireMode_2580_tc_1511450',
        'testcases.WireMode_2580.Test_04_WireMode_2580_tc_1511456',
        'testcases.WireMode_2580.Test_05_WireMode_2580_tc_1511457',
        'testcases.WireMode_2580.Test_06_WireMode_2580_tc_1511459',
        'testcases.WireMode_2580.Test_07_WireMode_2580_tc_1511461',
        'testcases.WireMode_2580.Test_08_WireMode_2580_tc_1511462',
        'testcases.WireMode_2580.Test_09_WireMode_2580_tc_1511463',
        'testcases.WireMode_2580.Test_10_WireMode_2580_tc_1511490',
        'testcases.WireMode_2580.Test_11_WireMode_2580_tc_1511465',
        'testcases.WireMode_2580.Test_12_WireMode_2580_tc_1511466',
        'testcases.WireMode_2580.Test_13_WireMode_2580_tc_1511467',
        'testcases.WireMode_2580.Test_14_WireMode_2580_tc_1511474',
        'testcases.WireMode_2580.Test_15_WireMode_2580_tc_1511489',
        # # full testcase
        'testcases.WireMode_2580.Test_16_WireMode_2580_tc_1511442',
        'testcases.WireMode_2580.Test_17_WireMode_2580_tc_1511448',
        'testcases.WireMode_2580.Test_18_WireMode_2580_tc_1511449',
        'testcases.WireMode_2580.Test_19_WireMode_2580_tc_1511451',
        'testcases.WireMode_2580.Test_20_WireMode_2580_tc_1511452',
        'testcases.WireMode_2580.Test_21_WireMode_2580_tc_1511453',
        'testcases.WireMode_2580.Test_22_WireMode_2580_tc_1511455',
        'testcases.WireMode_2580.Test_23_WireMode_2580_tc_1511458',
        'testcases.WireMode_2580.Test_24_WireMode_2580_tc_1511472',
        'testcases.WireMode_2580.Test_25_WireMode_2580_tc_1511473',
        'testcases.WireMode_2580.Test_26_WireMode_2580_tc_1511476',
        'testcases.WireMode_2580.Test_27_WireMode_2580_tc_1511482',
        'testcases.WireMode_2580.Test_28_WireMode_2580_tc_1511487',
        'testcases.WireMode_2580.Test_29_WireMode_2580_tc_1511488',
        'testcases.WireMode_2580.Test_30_WireMode_2580_tc_1511491',
        'testcases.WireMode_2580.Test_31_WireMode_2580_tc_1511499',
        'testcases.WireMode_2580.Test_32_WireMode_2580_tc_1511500',

        
     
      
              
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
