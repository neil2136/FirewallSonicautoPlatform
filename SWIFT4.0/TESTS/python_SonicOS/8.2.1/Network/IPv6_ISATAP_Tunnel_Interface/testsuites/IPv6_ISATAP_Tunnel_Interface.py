__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_ISATAP_Tunnel_Interface')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_ISATAP_Tunnel_Interface/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_01_IPv6_ISATAP_Tunnel_Interface_tc_12',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_02_IPv6_ISATAP_Tunnel_Interface_tc_13',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_03_IPv6_ISATAP_Tunnel_Interface_tc_14',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_04_IPv6_ISATAP_Tunnel_Interface_tc_15',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_05_IPv6_ISATAP_Tunnel_Interface_tc_20',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_06_IPv6_ISATAP_Tunnel_Interface_tc_25',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_07_IPv6_ISATAP_Tunnel_Interface_tc_27',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_08_IPv6_ISATAP_Tunnel_Interface_tc_31',
        'testcases.IPv6_ISATAP_Tunnel_Interface.Test_09_IPv6_ISATAP_Tunnel_Interface_tc_33',        
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
