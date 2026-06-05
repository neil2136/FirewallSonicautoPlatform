__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Interface_ARS')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Interface_ARS/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.Interface_ARS.Test_01_Interface_ARS_tc_01',
        'testcases.Interface_ARS.Test_02_Interface_ARS_tc_03',
        'testcases.Interface_ARS.Test_03_Interface_ARS_tc_06',
        'testcases.Interface_ARS.Test_04_Interface_ARS_tc_12',
        'testcases.Interface_ARS.Test_05_Interface_ARS_tc_13',
        'testcases.Interface_ARS.Test_06_Interface_ARS_tc_14',
        'testcases.Interface_ARS.Test_07_Interface_ARS_tc_18',
        'testcases.Interface_ARS.Test_08_Interface_ARS_tc_19',
        'testcases.Interface_ARS.Test_09_Interface_ARS_tc_21',      
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
