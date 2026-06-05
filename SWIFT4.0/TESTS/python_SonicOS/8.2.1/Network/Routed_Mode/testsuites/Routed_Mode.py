import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Routed_Mode')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Routed_Mode/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB',
        'testcases.Routed_Mode.Test_01_Routed_Mode_tc_66',
        'testcases.Routed_Mode.Test_02_Routed_Mode_tc_67',
        'testcases.Routed_Mode.Test_03_Routed_Mode_tc_68',
        'testcases.Routed_Mode.Test_04_Routed_Mode_tc_69',
        'testcases.Routed_Mode.Test_05_Routed_Mode_tc_70',
        'testcases.Routed_Mode.Test_06_Routed_Mode_tc_71',        
        'testcases.Routed_Mode.Test_07_Routed_Mode_tc_72',        
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
