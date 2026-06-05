__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_Port_Scanning_TP766')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_Port_Scanning_TP766/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',
        'testcases.IPv6_Port_Scanning_TP766.Test_01_IPv6_Port_Scanning_TP766_tc_1529658',
        'testcases.IPv6_Port_Scanning_TP766.Test_02_IPv6_Port_Scanning_TP766_tc_1529663',
        'testcases.IPv6_Port_Scanning_TP766.Test_03_IPv6_Port_Scanning_TP766_tc_1529664',
        'testcases.IPv6_Port_Scanning_TP766.Test_04_IPv6_Port_Scanning_TP766_tc_1529665',
        'testcases.IPv6_Port_Scanning_TP766.Test_05_IPv6_Port_Scanning_TP766_tc_1529666',
        'testcases.IPv6_Port_Scanning_TP766.Test_06_IPv6_Port_Scanning_TP766_tc_1529659',
        'testcases.IPv6_Port_Scanning_TP766.Test_07_IPv6_Port_Scanning_TP766_tc_1529660',
        'testcases.IPv6_Port_Scanning_TP766.Test_08_IPv6_Port_Scanning_TP766_tc_1529661',
        'testcases.IPv6_Port_Scanning_TP766.Test_09_IPv6_Port_Scanning_TP766_tc_1529662',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
