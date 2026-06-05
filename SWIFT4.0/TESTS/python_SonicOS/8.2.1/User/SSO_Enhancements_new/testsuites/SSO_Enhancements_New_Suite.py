import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/SSO_Enhancements_new')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_1',
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_13', 
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_12', 
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_14',
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_15',        
        'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_8', 
        # 'testcases.SSO_Enhancements_new.Test_SSO_Enhancements_new_22',  
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
