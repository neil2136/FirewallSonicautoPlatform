import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/SSO_by_Radius_Accounting')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_05',
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_08', 
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_09', 
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_06',
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_23',  
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_10',
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_14',     
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_17',        
        'testcases.SSO_by_Radius_Accounting.Test_SSO_by_Radius_Accounting_16',         
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
