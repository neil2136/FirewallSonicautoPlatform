__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Port_Scanning')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Port_Scanning/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'testcases.Port_Scanning.Test_01_Port_Scanning_tc_1',
        'testcases.Port_Scanning.Test_02_Port_Scanning_tc_2',
        'testcases.Port_Scanning.Test_03_Port_Scanning_tc_5',
        'testcases.Port_Scanning.Test_04_Port_Scanning_tc_7',
        'testcases.Port_Scanning.Test_05_Port_Scanning_tc_9',
        'testcases.Port_Scanning.Test_06_Port_Scanning_tc_12',
        'testcases.Port_Scanning.Test_07_Port_Scanning_tc_15',
        'testcases.Port_Scanning.Test_08_Port_Scanning_tc_16',
        'testcases.Port_Scanning.Test_09_Port_Scanning_tc_18',        
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
