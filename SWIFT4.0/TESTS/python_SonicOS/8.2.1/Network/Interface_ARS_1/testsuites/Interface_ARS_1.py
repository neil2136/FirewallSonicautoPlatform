__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Interface_ARS_1')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Interface_ARS_1/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.Test_config_remote',
        'definition.set_env.Test_config_local',
        'definition.set_env.Test_Config_Switch',
        'testcases.Interface_ARS_1.Test_01_Interface_ARS_tc_07'     
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
