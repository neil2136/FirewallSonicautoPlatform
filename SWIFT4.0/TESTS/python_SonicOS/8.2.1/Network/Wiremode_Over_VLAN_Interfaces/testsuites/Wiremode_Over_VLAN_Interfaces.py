__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Wiremode_Over_VLAN_Interfaces')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/Wiremode_Over_VLAN_Interfaces/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.Test_Config_Switch',
        'testcases.Wiremode_Over_VLAN_Interfaces.Test_01_Wiremode_Over_VLAN_Interfaces_tc_022',
        'testcases.Wiremode_Over_VLAN_Interfaces.Test_02_Wiremode_Over_VLAN_Interfaces_tc_031',
        'testcases.Wiremode_Over_VLAN_Interfaces.Test_03_Wiremode_Over_VLAN_Interfaces_tc_035',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
