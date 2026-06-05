import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DHCP_Client')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config_pc.TestConfigPC',
        'testcases.DHCP_Client.TestDHCPClient_01', 
        'testcases.DHCP_Client.TestDHCPClient_02', 
        'testcases.DHCP_Client.TestDHCPClient_03', 
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
