import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DHCP_Server')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw.TestInitConfig',
        'testcases.dhcp_server.TestDHCPServer_01', 
        'testcases.dhcp_server.TestDHCPServer_18', 
        'testcases.dhcp_server.TestDHCPServer_30', 
        'testcases.dhcp_server.TestDHCPServer_39', 
        'testcases.dhcp_server.TestDHCPServer_38', 
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
