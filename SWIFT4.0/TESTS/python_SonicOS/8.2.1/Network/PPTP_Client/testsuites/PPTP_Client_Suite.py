import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/PPTP_Client/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config_pc.TestConfigPC',
         'testcases.PPTP_Client.TestPPTPClient_01',  
         'testcases.PPTP_Client.TestPPTPClient_02', 
         'testcases.PPTP_Client.TestPPTPClient_03',  
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
