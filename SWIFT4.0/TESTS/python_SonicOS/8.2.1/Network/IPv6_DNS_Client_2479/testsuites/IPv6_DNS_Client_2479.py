__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_DNS_Client_2479')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPv6_DNS_Client_2479/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_env.TestConfigTB',
        'testcases.IPv6_DNS_Client_2479.Test_01_IPv6_DNS_Client_2479_tc_2',
        'testcases.IPv6_DNS_Client_2479.Test_02_IPv6_DNS_Client_2479_tc_5',
        'testcases.IPv6_DNS_Client_2479.Test_03_IPv6_DNS_Client_2479_tc_7',
        'testcases.IPv6_DNS_Client_2479.Test_04_IPv6_DNS_Client_2479_tc_10',
        'testcases.IPv6_DNS_Client_2479.Test_05_IPv6_DNS_Client_2479_tc_11',         
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
